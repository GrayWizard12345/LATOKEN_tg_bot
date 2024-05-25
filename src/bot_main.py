import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dbutils import write_one_entry, get_secret
from test_open_ai import MESSAGES, get_gpt_answer

# Bot token can be obtained via https://t.me/BotFather
TOKEN = get_secret("TELEGRAM_BOT_KEY")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

    user_name = await get_user_name(message)

    await record_context(content=message.text, name=user_name, role="user")

    gpt_answer = get_gpt_answer()

    await record_context(content=gpt_answer, name="latoken_test_chat_bot", role="assistant")

    if isinstance(gpt_answer, list):
        for part in gpt_answer:
            await message.answer(part)
    else:
        await message.answer(gpt_answer)


async def record_context(content: str, name: str, role: str):
    """
    Writes one entry to database and updates global context of the bot
    :param content: text of the message
    :param name:
    :param role:
    :return: None
    """
    MESSAGES.append({"role": role, "content": content, "name": name})
    write_one_entry(role=role, content=content, name=name)


@dp.message()
async def message_handler(message: Message) -> None:
    """
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """

    user_name = await get_user_name(message)
    logging.info(f"User {user_name} sent a message: {message.text}")
    if not message.text:
        message.text = " "

    # Currently bot records all messages sent to the group as context.
    # This can be changed to only messages to bot by placing the following line under return statement
    await record_context(content=message.text, name=user_name, role="user")
    logging.info("Recorded context")
    if message.chat.type == "group":
        logging.info("Message was sent in a group")
        if "LABOT" not in message.text:
            return

    gpt_answer = get_gpt_answer()
    logging.info(f"GPT answer: {gpt_answer}")

    await record_context(content=gpt_answer, name="latoken_test_chat_bot", role="assistant")
    logging.info("Recorded context")

    if isinstance(gpt_answer, list):
        for part in gpt_answer:
            await message.answer(part)
    else:
        await message.answer(gpt_answer)


async def get_user_name(message: Message) -> str:
    """
    Gets a user name from message and converts it to a machine-readable format
    :param message: message object
    :return: username in machine-readable format
    """
    user_name = message.from_user.full_name if message.from_user.full_name else message.from_user.username
    user_name = user_name.replace("@", "").replace(" ", "_")
    return user_name


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
