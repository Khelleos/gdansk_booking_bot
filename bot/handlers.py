"""Telegram command and button handlers.

Shared objects come from application.bot_data: "store" (SubscriberStore),
"client" (QmaticClient) and "monitor" (Monitor), set up in bot.main.
"""
import logging
from datetime import datetime

from telegram import BotCommandScopeChat, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from bot.i18n import messages
from bot.i18n.translations import LANGUAGES
from bot.keyboards import (
    CHECK_CALLBACK,
    LANGUAGE_CALLBACK_PREFIX,
    LANGUAGE_KEYBOARD,
    bot_commands,
    check_again_button,
    open_site_button,
)

logger = logging.getLogger(__name__)


def chat_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Saved subscriber language, then a choice made while unsubscribed, then the Telegram app language."""
    store = context.bot_data['store']
    lang = store.get_language(update.effective_chat.id) or context.chat_data.get('language')
    if lang:
        return lang
    user = update.effective_user
    return messages.detect_language(user.language_code if user else None)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = chat_language(update, context)
    context.bot_data['store'].add(chat_id, lang)
    await update.message.reply_text(messages.welcome(lang))


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = chat_language(update, context)
    # Remember the language until restart in case the chat subscribes again
    context.chat_data['language'] = lang
    if context.bot_data['store'].remove(chat_id):
        await update.message.reply_text(messages.unsubscribed(lang))
    else:
        await update.message.reply_text(messages.not_subscribed(lang))


async def show_check_result(message, lang, client):
    """Run a manual check and edit `message` to show the result."""
    try:
        slots = await client.fetch_slots()
    except Exception as e:
        logger.error(f"Error in manual check: {e}")
        await message.edit_text(
            messages.check_error(lang, str(e) or type(e).__name__),
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[check_again_button(lang)]])
        )
        return

    if slots:
        keyboard = [[open_site_button(lang)], [check_again_button(lang)]]
    else:
        keyboard = [[check_again_button(lang)]]
    await message.edit_text(
        messages.check_result(lang, slots, datetime.now()),
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = chat_language(update, context)
    message = await update.message.reply_text(messages.checking(lang))
    await show_check_result(message, lang, context.bot_data['client'])


async def check_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = chat_language(update, context)
    message = await query.edit_message_text(messages.checking(lang))
    await show_check_result(message, lang, context.bot_data['client'])


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    store = context.bot_data['store']
    monitor = context.bot_data['monitor']
    lang = chat_language(update, context)
    status_text = messages.status(
        lang,
        is_subscribed=store.is_subscriber(update.effective_chat.id),
        total=store.count(),
        last_check_at=monitor.last_check_at,
        last_result=monitor.last_result,
        next_check_at=monitor.next_check_at,
        now=datetime.now(),
    )
    await update.message.reply_text(status_text, parse_mode='HTML')


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = chat_language(update, context)
    await update.message.reply_text(messages.choose_language(lang), reply_markup=LANGUAGE_KEYBOARD)


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.removeprefix(LANGUAGE_CALLBACK_PREFIX)
    if lang not in LANGUAGES:
        return
    chat_id = update.effective_chat.id
    context.bot_data['store'].set_language(chat_id, lang)
    context.chat_data['language'] = lang
    # Show this chat's menu in the chosen language instead of the Telegram app language
    await context.bot.set_my_commands(bot_commands(lang), scope=BotCommandScopeChat(chat_id))
    await query.edit_message_text(messages.language_set(lang))


def register(application: Application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("check", check_now))
    application.add_handler(CallbackQueryHandler(check_again, pattern=f"^{CHECK_CALLBACK}$"))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("language", language))
    application.add_handler(CallbackQueryHandler(language_chosen, pattern=f"^{LANGUAGE_CALLBACK_PREFIX}"))
