import os
import linecache
import chess
import chess.pgn
import pyodbc
import firebase_admin
from firebase_admin import credentials, firestore
PGN_DIRECTORY = "ChessPGNS"
EloAlwaysOnSameLine = True

def connectToDB():
	# Specify the LocalDB instance name or connection string
	localdb_instance = r"(localdb)\ChessTheElo"

	# Specify the database name
	database = "ChessTheElo"

	# Create a connection string
	conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={localdb_instance};Database={database};Trusted_Connection=yes;"

	# Connect to the LocalDB instance
	conn = pyodbc.connect(conn_str)

	# Create a cursor object to execute queries
	return conn, conn.cursor()

	# Example: Execute a query
	#cursor.execute("SELECT * FROM Games")
	#rows = cursor.fetchall()

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
	#print("White elo: " + str(whiteElo))
	myLine = pgn.readline()
	blackElo = getElo(myLine)
	#print("Black elo: " + str(blackElo))
	return whiteElo, blackElo

def findNextTimeControl(pgn):
	myLine = pgn.readline()
	while myLine[1:12] != "TimeControl":
		myLine = pgn.readline()
	if myLine != "[TimeControl \"300+0\"]\n":
		return False
	return True

def main():
	#conn, cursor = connectToDB()
	cred = credentials.Certificate("chessguesstheelo-firebase-adminsdk-17z5u-2ece44e9df.json")

	firebase_admin.initialize_app(cred, 
	{
	'databaseURL': 'https://ChessGuessTheElo.firebaseio.com/'
	})
	db = firestore.client()
	doc_ref = db.collection(u'Games')
	count = 0
	pgn = open("lichess_db_standard_rated_2023-04.1.994.pgn", "r")
	game = ""
	while game != None:
		#keep reading games!
		shouldUpload = False
		whiteElo, blackElo = findNextElo(pgn)
		if abs(whiteElo - blackElo) <= 250:
			if findNextTimeControl(pgn):
				shouldUpload = True
		game = chess.pgn.read_game(pgn)
		if shouldUpload:
			print("White elo: " + str(whiteElo))
			print("Black elo: " + str(blackElo))
			moveList = []
			for move in game.mainline_moves():
				print(str(move))
				moveList.append(str(move))
			moveString = ",".join(moveList)
			#temporary
			if whiteElo == 779 and blackElo == 859:
				exit()
			print("Uploading to the database!")
			#time to upload to firebase
			myDict = { 'WhiteElo' : whiteElo,
						'BlackElo' : blackElo,
						'GameString' : moveString,
						'GameID' : count

			}

			doc_ref.add(myDict)




			#sql = "INSERT INTO Games (GameID, WhiteElo, BlackElo, GameString) VALUES (?, ?, ?, ?)"
			#cursor.execute(sql, count, whiteElo, blackElo, moveString)
			#conn.commit()
			count += 1
	cursor.close()
	conn.close()

if __name__ == "__main__":
	main()