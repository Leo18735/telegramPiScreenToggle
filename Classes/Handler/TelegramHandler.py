import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from Classes.Handler.Handler import Handler
from Classes.Screen.PiScreen import PiScreen
from Classes.Fan.Temperature import Temperature
from Classes.Fan.Fan import Fan
from Classes.State.StateIn import StateIn
from Classes.State.StateOut import StateOut


class TelegramHandler(Handler):
    _help_message: str = "/screen_on\n/screen_off\n/fan_on\n/fan_off\n/fan_block\n/fan_unblock\n/temp\n/state\n/help"

    def __init__(self, temperature: Temperature, fan: Fan, pi_screen: PiScreen, token: str, *_, **__):
        self._temperature: Temperature = temperature
        self._fan: Fan = fan
        self._pi_screen: PiScreen = pi_screen
        self._token: str = token

    async def _screen_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._change_screen_state(update, context, StateIn.ON)

    async def _screen_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._change_screen_state(update, context, StateIn.OFF)

    async def _fan_on_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, context, StateIn.ON)

    async def _fan_off_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, context, StateIn.OFF)

    async def _fan_block_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, context, StateIn.BLOCK)

    async def _fan_unblock_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._change_fan_state(update, context, StateIn.UNBLOCK)

    async def _temp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._reply(update, context, str(self._temperature.get()))

    async def _state_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._reply(update, context, json.dumps({
            "screen": self._pi_screen.get().name,
            "fan": self._fan.get().name
        }, indent=2))

    @classmethod
    async def _help_command(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await cls._reply(update, context, cls._help_message, False)

    async def _change_fan_state(self, update: Update, context: ContextTypes.DEFAULT_TYPE, desired_state: StateIn):
        state = self._fan.set(desired_state)
        if state == StateOut.BLOCK:
            await self._reply(update, context, "Fan is blocked")
            return
        if state != desired_state and state != StateOut.OFF and desired_state != StateIn.BLOCK:
            await self._reply(update, context, "Error setting")
            return
        await self._reply(update, context, "Ok")

    async def _change_screen_state(self, update: Update, context: ContextTypes.DEFAULT_TYPE, desired_state: StateIn):
        state: StateOut = self._pi_screen.set(desired_state)
        if state != desired_state:
            await self._reply(update, context, "Error setting")
            return
        await self._reply(update, context, "Ok")

    @staticmethod
    async def _reply(update: Update, context: ContextTypes.DEFAULT_TYPE, msg: str, erase: bool = True):
        sent_message = await update.message.reply_text(msg)
        if not erase:
            return
        await asyncio.sleep(10)
        try:
            await context.bot.delete_message(
                chat_id=sent_message.chat_id,
                message_id=sent_message.message_id
            )
        except Exception as e:
            print(f"Could not delete message: {e}")

    def run(self):
        app = ApplicationBuilder().token(self._token).build()

        app.add_handler(CommandHandler("screen_on", self._screen_on_command))
        app.add_handler(CommandHandler("screen_off", self._screen_off_command))
        app.add_handler(CommandHandler("fan_on", self._fan_on_command))
        app.add_handler(CommandHandler("fan_off", self._fan_off_command))
        app.add_handler(CommandHandler("fan_block", self._fan_block_command))
        app.add_handler(CommandHandler("fan_unblock", self._fan_unblock_command))
        app.add_handler(CommandHandler("state", self._state_command))
        app.add_handler(CommandHandler("temp", self._temp_command))
        app.add_handler(CommandHandler("help", self._help_command))

        app.run_polling()
