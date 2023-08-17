from helpers.shared import context
from helpers.messenger import send_message, update_last_message


from enum import Enum, auto

import handlers  # імпорт повністю


class GameState(Enum):
    NotStarted = auto()
    Start = auto()
    BeginGame = auto()
    Lobby = auto()
    GameCreate = auto()
    InRound = auto()
    RoundResult = auto()
    GameResult = auto()


ROUTER = {
    GameState.NotStarted: handlers.start_handler,
    GameState.Start: handlers.start_handler,
    GameState.BeginGame: handlers.begin_game_handler,
    GameState.GameCreate: handlers.game_create_handler,
    GameState.Lobby: handlers.lobby_handler,
    GameState.InRound: handlers.in_round_handler,
    GameState.RoundResult: handlers.round_result_handler,
    GameState.GameResult: handlers.game_result_handler,
}


async def router(chat_id, user_message, context):
    game_state = context["game_state"]
    # if user_message == '/start'

    # buttons1 = [
    #     {"text": "BTN", "command": "btn"},
    #     {"text": "BUTTON", "command": "button"},
    #     {"text": "BUTTON 2", "command": "button3"},
    # ]
    # buttons2 = [
    #     {"text": "BTN 5", "command": "btn"},
    #     {"text": "BUTTON 6", "command": "button"},
    #     {"text": "BUTTON 7", "command": "button3"},
    # ]
    # order = [1, 2]

    # await send_message("test 2", chat_id, buttons1, order)
    # await update_last_message("test 5", chat_id, buttons2, order)
    return
