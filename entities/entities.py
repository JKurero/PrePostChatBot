from datetime import datetime

from middleware.router import GameState

def StateToInt(state):
    if state == GameState.NotStarted:
        return 1
    elif state == GameState.GameCreate:
        return 2
    elif state == GameState.BeginGame:
        return 3
    elif state == GameState.Lobby:
        return 4
    elif state == GameState.Start:
        return 5
    elif state == GameState.InRound:
        return 6
    elif state == GameState.RoundResult:
        return 7
    elif state == GameState.GameResult:
        return 8
    return 0

def IntToState(index):
    if index == 1:
        return GameState.NotStarted
    elif index == 2:
        return GameState.GameCreate
    elif index == 3:
        return GameState.BeginGame
    elif index == 4:
        return GameState.Lobby
    elif index == 5:
        return GameState.Start
    elif index == 6:
        return GameState.InRound
    elif index == 7:
        return GameState.RoundResult
    elif index == 8:
        return GameState.GameResult
    return None

# користувач бота (гравець)
class User:    
    def __init__(self, id: int, telegramUserId: int, name: str):
        self.id = id
        self.telegramUserId = telegramUserId
        self.name = name

# Запитання в грі
class Question:
    # correctAnswer має бути типу Answer, але Python не дозволяє циркулярних залежностей, тому тип цього параметра непідписаний
    def __init__(self, id: int, text: str, isTest: bool, hasBeenPlayed: bool, authorId: int, author: User, correctAnswerId: int, correctAnswer):
        self.id = id
        self.text = text
        self.isTest = isTest
        self.hasBeenPlayed = hasBeenPlayed
        self.authorId = authorId
        self.author = author
        self.correctAnswerId = correctAnswerId
        self.correctAnswer = correctAnswer
        self.answers = []
    
    def __repr__(self):
        return f'text="{self.text}", answers=[' + ', '.join(map(lambda x: repr(x), self.answers)) + ']'

# варіант відповіді на запитання
class Answer:
    def __init__(self, id: int, questionId: int, question: Question, text: str, isCorrect: bool):
        self.id = id
        self.questionId = questionId
        self.question = question
        self.text = text
        self.isCorrect = isCorrect
    def __repr__(self):
        return f'"{self.text}"'

# гра (серія раундів)
class Game:
    def __init__(self, id: int, time: datetime, initiatingUserId: int, initiatingUser: User, gameState: int, numberOfRounds: int, isTest: bool):
        self.id = id
        self.time = time
        self.initiatingUserId = initiatingUserId
        self.initiatingUser = initiatingUser
        self.gameState = IntToState(gameState)
        self.numberOfRounds = numberOfRounds
        self.isTest = isTest
        self.rounds = []
        self.users = []

# раунд гри (одне запитання, зігране в певний момент часу)
class Round:
    def __init__(self, id: int, questionId: int, question: Question, gameId: int, game: Game, time: datetime):
        self.id = id
        self.questionId = questionId
        self.question = question
        self.gameId = gameId
        self.game = game
        self.time = time

# команда гравців
class Team:
    def __init__(self, id: int, gameId: int, game: Game, playersCount: int):
        self.id = id
        self.gameId = gameId
        self.game = game
        self.playersCount = playersCount

# користувач-запитання - запис, який показує, що цей користувач уже зіграв це запитання (щоб не показувати йому те саме запитання знову)
# необов’язково
class UserToQuestion:
    def __init__(self, userId: int, user: User, questionId: int, question: Question, gameId: int, game: Game):
        self.userId = userId
        self.user = user
        self.questionId = questionId
        self.question = question
        self.gameId = gameId 
        self.game = game

# користувач-раунд - інформація про ставку, яку зробив цей користувач у цьому раунді, і про виграні бали
class UserToRound:
    def __init__(self, userId: int, user: User, roundId: int, round: Round, answerId: int, answer: Answer, bet: int, score: int):
        self.userId = userId
        self.user = user
        self.roundId = roundId
        self.round = round
        self.answerId = answerId
        self.answer = answer
        self.bet = bet
        self.score = score
    
# користувач-гра - інформація про те, скільки балів заробив цей гравець у цій грі і яке місце посів
class UserToGame:
    def __init__(self, userId: int, user: User, gameId: int, game: Game, score: int, place: int):
        self.userId = userId
        self.user = user
        self.gameId = gameId 
        self.game = game
        self.score = score
        self.place = place

# користувач-команда - хто до якої команди належить у кожній грі
class UserToTeam:
    def __init__(self, userId: int, user: User, teamId: int, team: Team):
        self.userId = userId
        self.user = user
        self.teamId = teamId
        self.team = team