import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import matplotlib.pyplot as plt
import datetime
from colorama import init
from colorama import Fore, Back, Style



"""

Script is used to retrieve the Nuclear Throne daily scores for a specified user. The program will load up the scores
for the player ID specified in the config.txt file.


User can type "graph" to display a graph of all of their Thronebutt Ranks. 
Config file can be changed to display a different user by default.


"""





def loadConfig():
	fname = "config.txt"

	if not os.path.isfile(fname): 
		defaultID = "76561198041990816"
		file = open(fname, "w")
		file.write( defaultID + "\n")
		file.close()
		return defaultID

	else:
		file = open(fname,"r")
		playerID = file.read()
		return playerID

def getUserName(profileNumber):

	page = requests.get("http://thronebutt.com/player/" + str(profileNumber) ).content

	soup = BeautifulSoup(page)

	playerZone = soup.find("h3",{"class":"title stroke-hard player-title"})


	for node in playerZone.findAll('a'):
		userName =  (''.join(node.findAll(text=True)))

	return userName


def stripTD(row):

	row = row.replace("<td>","")
	row = row.replace("</td>","")
	row = row.replace("<b>","")
	row = row.replace("</b>","")
	row = row.replace("%","")
	row = row.replace("#","")
	return row


def getStats(currentRow):

	dataNo = 0
	for rowData in currentRow:
		
		if dataNo == 1:
			date = stripTD( str(rowData) )

		elif dataNo ==3:
			top = stripTD( str(rowData) )

		elif dataNo == 5:
			rank = stripTD( str(rowData) )

		dataNo += 1

	try:
		current = (date,top,rank)
		return(current)
	except:
		return("")
	


def getProfile(playerNo):

	page = requests.get("http://thronebutt.com/player/" + str(playerNo) ).content

	#Creates a 'soup' object from the page
	soup = BeautifulSoup(page)

	#Searches the soup object for a div tag that contains an id with a value of "comic"
	scoreTable = soup.find("tbody",{"id":"latest_score_table"})
	return scoreTable

def printScore(tupleScore):
	
	today = str( datetime.date.today() )

	if today == str(tupleScore[0]):
		print(Fore.YELLOW)

	else:
		print(Fore.MAGENTA)

	print("\t\t" + str(tupleScore[0]) )
	print("\t\tRank: #" + str(tupleScore[2]) )
	print("\t\tTop: " + str(tupleScore[1]) + "%")
	print(Fore.RESET)


def addScores(scoreTable,allScores):

	for row in scoreTable:
		currentStat = getStats(row)
		allScores.append(currentStat)

def cleanList(allScores):

	for score in allScores:
		if score == "":
			allScores.remove(score)

def printScores(allScores,scoresToPrint):
	for num in scoresToPrint:
		printScore(allScores[num])


def printMostRecent(allScores,xMostRecent=3):
	print("Most Recent: \n")
	while xMostRecent > 0:
		printScore(allScores[xMostRecent-1])
		xMostRecent -= 1

def printBest(allScores):
	tupNo = 0
	highest = 100000

	for score in allScores:
		current = int( score[1] )

		

		if current <= highest:
			highest = current
			highestTup = tupNo

		tupNo += 1
	print(Fore.CYAN + "Best Score: \n")
	printScore(allScores[highestTup])



def createListOfScores(profileNumber):

	profileNumber = str(profileNumber)

	allScores = []

	scoreTable = getProfile(profileNumber)
	
	addScores(scoreTable,allScores)
		
	cleanList(allScores)
	return allScores



def plotGraph(allScores):
	scoreNo = 1
	xplot = []
	yplot = []
	for score in allScores:
		#plt.scatter(scoreNo,score[2])
		xplot.append(scoreNo)
		yplot.append(score[1])
		#plt.plot(scoreNo,score[2],'bo-')
		scoreNo += 1
	
	grap =  plt.plot(xplot,yplot,'bo-')
	plt.ylabel('Percentage')
	plt.xlabel('Run No.')
	plt.show()


def main():


	init()

	playerID = loadConfig()


	userName = getUserName(playerID)
	allScores = createListOfScores(playerID)

	print(Fore.CYAN)
	print("Scores for user: " + str(userName) + "\n")
	#Print a specific set of scores:
	#printScores(allScores, [0,1,2])

	today = str( datetime.date.today() )

	#Print most recent scores:
	printMostRecent(allScores,2)

	printBest(allScores)

	#Format of scores:
	#(Date,Percentage,Rank)

	#print("Enter a player Number to view their stats: ")
	while True:
		chosenID = input("\n>")
		try:
			if chosenID == "graph":
				plotGraph(allScores)
			else:
				allScores = createListOfScores(chosenID)
				userName = getUserName(chosenID)
				print("Scores for user: " + str(userName) + "\n")
				printMostRecent(allScores,3)
				printBest(allScores)
		except:
			print("Invalid User ID")
		



	

if __name__ == "__main__":
	main()

