import requests
import csv
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# pylint: disable=W0312,C0325,C0103,C0301,C0330

team_names = {}
abilities = {}
trueskills = {}

with open('Calgary_Scouting.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		abilities[row["Team number"]] = row["What can it do?"].split(";")
		abilities[row["Team number"]].append(row["Does it have auto?"])

print ("Enter Event Key:")
event_key = input().lower()
event_key = "2017"+event_key
if event_key == 'q':
	quit()

rankings = requests.get("https://www.thebluealliance.com/api/v2/event/"+event_key+"/rankings", headers={"X-TBA-App-Id":"frc-4774:FRC_auto_scouter:1.0"})
rankings = rankings.json()
if len(rankings) == 0:
	print("No information")
	quit()
try:
	rankings["404"]
except:
	pass
else:
	print(rankings["404"])
	quit()

teams = requests.get("https://www.thebluealliance.com/api/v2/event/"+event_key+"/teams", headers={"X-TBA-App-Id":"frc-4774:FRC_auto_scouter:1.0"})
teams = teams.json()
for team in teams:
	team_names[team["team_number"]] = team["nickname"]

# create lists of stats
auto = []
climb = []
gear = []
balls = []

trueskill_score = requests.get("http://trueskill-trueskill-4774.44fs.preview.openshiftapps.com/api/trueskills/"+event_key).json()
for team in trueskill_score:
	trueskills[team[1]] = team[0]

for item in rankings:
	can_climb = False
	can_gear = False
	can_balls = False
	can_auto = False

	if item[0] == 'Rank':
		continue

	try:
		for skill in abilities[str(item[1])]:
			if skill == "Gear":
				can_gear = True
			elif skill == "Climber":
				can_climb = True
			elif skill == "Shooter" or skill == "Loader":
				can_balls = True
			elif skill == 'Yes':
				can_auto = True
	except KeyError:
		print("Missing info for "+ str(item[1]))

	if can_auto:
		auto.append(item[4])
	else:
		item[4] = ""
	if can_climb:
		climb.append(item[6])
	else:
		item[6] = ""
	if can_gear:
		gear.append(item[5])
	else:
		item[5] = ""
	if can_balls:
		balls.append(item[7])
	else:
		item[7] = ""

while True:
	print ("Enter Team Number or ENTER for all:")
	team_key = input()
	if team_key == "q":
		break

	for item in rankings:
		if item[0] == 'Rank':
			continue
		if len(team_key) > 0:
			if team_key != str(item[1]):
				continue
		print ("")
		print ("%s. %s - %s (%s) \nAuto: %s \nClimb: %s \nGear: %s \nBalls: %s" %(item[0], item[1], team_names[item[1]], (round(trueskills[item[1]]*100)/100),
		stats.percentileofscore(auto, item[4]), stats.percentileofscore(climb, item[6]),
		stats.percentileofscore(gear, item[5]), stats.percentileofscore(balls, item[7])))

quit()
