import logging
import ssl

import aiohttp

logger = logging.getLogger(__name__)


class QmaticClient:
    """REST client for the Qmatic web booking schedule of one branch and service."""

    def __init__(self, base_url: str, branch_id: str, service_id: str, slot_length: int, timeout: float):
        self._schedule_url = f"{base_url}/rest/schedule/branches/{branch_id}"
        self._params = f"servicePublicId={service_id};customSlotLength={slot_length}"
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session = None

    def _url(self, path: str) -> str:
        return f"{self._schedule_url}/{path};{self._params}"

    def _get_session(self) -> aiohttp.ClientSession:
        # Created on first use, because a session needs a running event loop
        if self._session is None or self._session.closed:
            # The booking server's certificate doesn't validate
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=ssl_context),
                timeout=self._timeout,
            )
        return self._session

    async def fetch_dates(self) -> list:
        """Dates that have free slots. Raises on network errors and non-200 responses."""
        async with self._get_session().get(self._url("dates")) as response:
            if response.status != 200:
                raise RuntimeError(f"API returned status code {response.status}")
            data = await response.json()
        if not isinstance(data, list):
            return []
        return [item['date'] for item in data if item.get('date')]

    async def fetch_times(self, date: str) -> list:
        """Free times on `date`; an empty list if they can't be fetched."""
        try:
            async with self._get_session().get(self._url(f"dates/{date}/times")) as response:
                if response.status == 200:
                    data = await response.json()
                    return [t['time'] for t in data if t.get('time')]
        except Exception as e:
            logger.warning(f"Error fetching times for date {date}: {e}")
        return []

    async def fetch_slots(self) -> dict:
        """Return {date: [times]} for every available date; empty dict if there are none.

        Raises on network errors and non-200 responses.
        """
        return {date: await self.fetch_times(date) for date in await self.fetch_dates()}

    async def close(self):
        if self._session is not None:
            await self._session.close()
