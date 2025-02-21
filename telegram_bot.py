from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


class TelegramBot:
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            rf"Hello {user.mention_html()}!", reply_markup=ForceReply(selective=True)
        )

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_text("Available commands: /start, /help")

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user_text = update.message.text
        response = self.bot_instance.process_message(user_text)
        await update.message.reply_text(response)

    def run(self):
        app = Application.builder().token(self.bot_instance.bot_token).build()
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        app.run_polling(allowed_updates=Update.ALL_TYPES)
