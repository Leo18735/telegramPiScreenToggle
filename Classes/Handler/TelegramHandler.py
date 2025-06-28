import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from Classes.Handler.Handler import Handler
from Classes.Screen.PiScreen import PiScreen
from Classes.Fan.Temperature import Temperature
from Classes.State import State
from Classes.Fan.Fan import Fan


class TelegramHandler(Handler):
    _help_message: str = "/screen_on\n/screen_off\n/fan_on\n/fan_off\n/fan_block\n/fan_unblock\n/temp\n/help"

    def __init__(self, temperature: Temperature, fan: Fan, pi_screen: PiScreen, token: str, *_, **__):
        self._temperature: Temperature = temperature
        self._fan: Fan = fan
        self._pi_screen: PiScreen = pi_screen
        self._token: str = token

    async def _screen_on_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._change_screen_state(update, State.ON)

    async def _screen_off_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._change_screen_state(update, State.OFF)

    async def _fan_on_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, State.ON)

    async def _fan_off_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, State.OFF)

    async def _fan_block_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, State.BLOCK)

    async def _fan_unblock_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, State.OFF)

    async def _temp_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await self._reply(update, str(self._temperature.get()))

    @classmethod
    async def _help_command(cls, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await cls._reply(update, cls._help_message)

    async def _change_fan_state(self, update: Update, desired_state: State):
        state = self._fan.set(desired_state)
        if state == State.NO_CHANGE:
            return await self._reply(update, "Fan already in correct state")
        if state == desired_state:
            return await self._reply(update, "Ok")
        if state == State.BLOCK and desired_state != State.BLOCK:
            return await self._reply(update, "Fan is blocked")
        return await self._reply(update, "Unknown error")

    async def _change_screen_state(self, update: Update, state: State):
        state: State = self._pi_screen.set(state)
        if state == State.NO_CHANGE:
            return await self._reply(update, "Screen already in correct state")
        if state == State.ERROR:
            return await self._reply(update, "Error changing screen state")
        if state == state:
            return await self._reply(update, "Ok")
        return await self._reply(update, "Unknown error")

    @staticmethod
    async def _reply(update: Update, msg: str):
        await update.message.reply_text(msg)

    def run(self):
        app = ApplicationBuilder().token(self._token).build()

        app.add_handler(CommandHandler("screen_on", self._screen_on_command))
        app.add_handler(CommandHandler("screen_off", self._screen_off_command))
        app.add_handler(CommandHandler("fan_on", self._fan_on_command))
        app.add_handler(CommandHandler("fan_off", self._fan_off_command))
        app.add_handler(CommandHandler("fan_block", self._fan_block_command))
        app.add_handler(CommandHandler("fan_unblock", self._fan_unblock_command))
        app.add_handler(CommandHandler("temp", self._temp_command))
        app.add_handler(CommandHandler("help", self._help_command))

        app.run_polling()
