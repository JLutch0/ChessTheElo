import os
import linecache
import chess
import chess.pgn
import pyodbc
PGN_DIRECTORY = "ChessPGNS"
EloAlwaysOnSameLine = True

count = 0

def connectToDB():
	server = 'LOCALDB#B957F537'  # Replace with your server name
	database = 'ChessTheElo'  # Replace with your database name
	driver = '{SQL Server}'  # Use the appropriate driver for your SQL Server version

	conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
	conn = pyodbc.connect(conn_str)
	cursor = conn.cursor()

def getElo(myLine):
	elo = 0
	modifier = 1
	i = -4
	while myLine[i] != "\"":
		elo += int(myLine[i]) * modifier
		modifier *= 10
		i -= 1
	return elo

def findNextElo(pgn):
	myLine = pgn.readline()
	while myLine[1:9] != "WhiteElo":
		myLine = pgn.readline()
	
	whiteElo = getElo(myLine)
	print("White elo: " + str(whiteElo))
	myLine = pgn.readline()
	blackElo = getElo(myLine)
	print("Black elo: " + str(blackElo))
	return whiteElo, blackElo

def main():
	#connectToDB()

	pgn = open("lichess_db_standard_rated_2023-04.1.994.pgn", "r")
	


	shouldUpload = True

	whiteElo, blackElo = findNextElo(pgn)

	if abs(whiteElo - blackElo) > 250:
		shouldUpload = False

	myLine = pgn.readline()
	while myLine[1:12] != "TimeControl":
		myLine = pgn.readline()
	if myLine != "[TimeControl \"300+0\"]\n":
		shouldUpload = False
	

	game = chess.pgn.read_game(pgn)
	
	while game != None:

		moveList = []
		for move in game.mainline_moves():
			print(str(move))
			moveList.append(str(move))
		moveString = ",".join(moveList)

		#input elos and moves into database!


		print("NEW GAME")
		shouldUpload = True
		#first we have to get the elos of the players
		whiteElo = -1
		blackElo = -1
	
		#looping through the lines until we get the elo
		myLine = pgn.readline()
		while myLine[1:9] != "WhiteElo":
			myLine = pgn.readline()
	
		whiteElo = getElo(myLine)
		print("White elo: " + str(whiteElo))
		myLine = pgn.readline()
		blackElo = getElo(myLine)
		print("Black elo: " + str(blackElo))

		if abs(whiteElo - blackElo) > 250:
			shouldUpload = False

		myLine = pgn.readline()
		while myLine[1:12] != "TimeControl":
			myLine = pgn.readline()
		if myLine != "[TimeControl \"300+0\"]\n":
			shouldUpload = False

		game = chess.pgn.read_game(pgn)
		


if __name__ == "__main__":
	main()