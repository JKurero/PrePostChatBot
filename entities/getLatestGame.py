from dbconnection import queryToDatabase
from entities.entities import Game, Round, User, UserToTeam

def createRoundFromRawData(raw):
    return Round(raw['Id'], raw['QuestionId'], None, raw['GameId'], None, raw['Time'])

def createUserFromRawData(raw):
    user = User(raw['UserId'], raw['TelegramUserId'], raw['Name'])
    return UserToTeam(user.id, user, raw['TeamId'], None)

def getLatestGame():
    rawData = queryToDatabase("""SELECT
        Id,
        InitiatingUserId,
        Time,
        GameState,
        NumberOfRounds,
        IsTest
        FROM Game ORDER BY Time DESC LIMIT(1)""")
    if len(rawData) == 0:
        return None
    x = rawData[0]
    game = Game(x['Id'], x['Time'], x['InitiatingUserId'], None, x['GameState'], x['NumberOfRounds'], bool(x['IsTest']))
    rawData = queryToDatabase(f"""
        SELECT Id, QuestionId, GameId, Time
        FROM Round WHERE GameId={game.id}
    """)
    rounds = list(map(createRoundFromRawData, rawData))
    rawData = queryToDatabase(f"""
        SELECT
            U.Id AS UserId,
            U.Name,
            U.TelegramUserId,
            T.Id AS TeamId
        FROM Team T WHERE GameId={game.id}
        JOIN UserToTeam UT ON UT.TeamId = T.Id
        JOIN User U ON U.Id = UT.UserId
    """)
    users = list(map(createUserFromRawData, rawData))
    game.rounds = rounds
    game.users = users
    return game
