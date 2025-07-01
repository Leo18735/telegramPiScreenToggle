import json
import typing
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from Classes.Handler.Handler import Handler
from Classes.Screen.PiScreen import PiScreen
from Classes.Fan.Temperature import Temperature
from Classes.Fan.Fan import Fan
from Classes.State import State


class TelegramHandler(Handler):
    _help_message: str = "/screen_on\n/screen_off\n/fan_on\n/fan_off\n/fan_block\n/fan_unblock\n/state\n/help"

    def __init__(self, temperature: Temperature, fan: Fan, pi_screen: PiScreen, token: str, *_, **__):
        self._temperature: Temperature = temperature
        self._fan: Fan = fan
        self._pi_screen: PiScreen = pi_screen
        self._token: str = token

    async def _screen_on_command(self, _: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._change_screen_state(State.ON)

    async def _screen_off_command(self, _: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._change_screen_state(State.OFF)

    async def _fan_on_command(self, _: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(State.ON)

    async def _fan_off_command(self, _: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(State.OFF)

    async def _fan_block_command(self, _: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(State.OFF, True)

    async def _fan_unblock_command(self, _: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(State.OFF, False)

    async def _state_command(self, update: Update, __: ContextTypes.DEFAULT_TYPE):
        await self._reply(update, f"Screen\n{self._pi_screen.get_text()}\n"
                                  f"Fan\n{self._fan.get_text()}\n"
                                  f"Temp\n{self._temperature.get_text()}")

    @classmethod
    async def _help_command(cls, update: Update, __: ContextTypes.DEFAULT_TYPE):
        await cls._reply(update, cls._help_message)

    async def _change_fan_state(self, state: State, block: typing.Optional[bool] = None):
        self._fan.set(state, block)

    async def _change_screen_state(self, state: State):
        self._pi_screen.set(state)

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
        app.add_handler(CommandHandler("state", self._state_command))
        app.add_handler(CommandHandler("help", self._help_command))

        app.run_polling()
