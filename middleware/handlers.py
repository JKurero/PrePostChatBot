import logging
from entities.dbconnection import addUserToGame, createNewGame, createNewGameAndAddUser, updateGameRoundCount
from entities.ensureUserExists import ensureUserExists
from entities.getLatestGame import getLatestGame

from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from .router import GameState, router

"""

@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(GameState.name)

    await message.answer(
        "Hi there! What's your name?",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:

    # Allow user to cancel any action


    current_state = await state.get_state()

    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)

    await state.clear()

    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(GameState.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)

    await state.set_state(GameState.like_bots)

    await message.answer(
        f"Nice to meet you, {html.quote(message.text)}!\nDid you like to write bots?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(GameState.like_bots, F.text.casefold() == "no")
async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    await state.clear()

    await message.answer(
        "Not bad not terrible.\nSee you soon.",
        reply_markup=ReplyKeyboardRemove(),
    )

    await show_summary(message=message, data=data, positive=False)


@router.message(GameState.like_bots, F.text.casefold() == "yes")
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.set_state(GameState.language)

    await message.reply(
        "Cool! I'm too!\nWhat programming language did you use for it?",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(GameState.like_bots)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("I don't understand you :(")


@router.message(GameState.language)
async def process_language(message: Message, state: FSMContext) -> None:
    data = await state.update_data(language=message.text)

    await state.clear()

    if message.text.casefold() == "python":
        await message.reply(
            "Python, you say? That's the language that makes my circuits light up! 😉"
        )

    await show_summary(message=message, data=data)


async def show_summary(
    message: Message, data: Dict[str, Any], positive: bool = True
) -> None:
    name = data["name"]

    language = data.get("language", "<something unexpected>")

    text = f"I'll keep in mind that, {html.quote(name)}, "

    text += (
        f"you like to write bots with {html.quote(language)}."
        if positive
        else "you don't like to write bots, so sad..."
    )

    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
"""

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(GameState.Start)
    ensureUserExists(message.from_user.full_name, message.from_user.id)
    
    await message.answer(
        "Hi there! Welcome to the game!",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("quit"))
async def quit_handler(message: Message, state: FSMContext) -> None:
    # Allow user to cancel any action

    current_state = await state.get_state()

    if current_state is None:
        return

    logger.info("Cancelling state %r", current_state)

    await state.clear()

    await message.answer(
        "Goodbye!",
        reply_markup=ReplyKeyboardRemove(),
    )

# 1) дізнатися останню гру getLatestGame
# 2) якщо остання гра завершена або її немає:
# 2.1) стейт=починаю гру await state.set_state
# 2.2) запитати кількість раундів await message.answer
# 3) інакше, якщо гра вже йде: сказати юзеру, щоб почекав await message.answer
# 4) інакше, якщо гра набирає нових юзерів — додати гравця до гри *addUserToGame
async def begin_game_handler(message: Message, state: FSMContext) -> None:
 # Дізнатися поточний стан гри
    current_state = await state.get_state()
    latestGame = getLatestGame()
    if current_state.gameState == GameState.BeginGame:
        # Створити нову гру і доєднати користувача до нової гри
        # TODO: Some logic...

        userText = message.md_text
        if not userText.isdigit():
            await message.answer(
                "Введи число!",
                reply_markup=ReplyKeyboardRemove(),
            )
        numberOfRounds=int(userText)
        updateGameRoundCount(latestGame.id, numberOfRounds)

        await message.answer(
            f"Створюю нову гру на {numberOfRounds} раундів.",
            reply_markup=ReplyKeyboardRemove(),
        )

        current_state = GameState.BeginGame
        await state.set_state(current_state)
        return

async def lobby_handler(message: Message, state: FSMContext) -> None:
    pass


async def game_create_handler(message: Message, state: FSMContext) -> None:
    latestGame = getLatestGame()
    current_state = await state.get_state()
    if current_state.gameState == GameState.NotStarted:
        current_state = await state.set_state(GameState.BeginGame)
        createNewGameAndAddUser(message.from_user.id)
    
        await message.answer(
        "Скільки буде раундів?",
        reply_markup=ReplyKeyboardRemove(),    
        )

    # Перевірити, чи є вже гра
    #if fake_games:
        # Доєднати користувача до існуючої гри
        # TODO: Some logic...
    if current_state.gameState in [GameState.InRound, GameState.RoundResult, GameState.GameResult]:  
        await message.answer(
        "Зачекай, поки почнеться нова гра",
        reply_markup=ReplyKeyboardRemove(),    
        )
        return
    if current_state.gameState == GameState.Lobby:
        await message.answer(
            "Доєдную тебе до існуючої гри.",
            reply_markup=ReplyKeyboardRemove()),
        addUserToGame(message.from_user.id, latestGame.id)
        
#        await state.set_state(current_state)
        return

def in_round_handler(message: Message, state: FSMContext) -> None:
    pass


def round_result_handler(message: Message, state: FSMContext) -> None:
    pass


def game_result_handler(message: Message, state: FSMContext) -> None:
    pass
