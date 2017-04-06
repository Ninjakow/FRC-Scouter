import requests
from scipy import stats

team_names = {}

print "Enter Event Key:"
event_key = raw_input()
event_key = "2017"+event_key


rankings = requests.get("https://www.thebluealliance.com/api/v2/event/"+event_key+"/rankings", headers={"X-TBA-App-Id":"frc-4774:Scouting_percentiles:1.0"})
rankings = rankings.json()

teams = requests.get("https://www.thebluealliance.com/api/v2/event/"+event_key+"/teams", headers={"X-TBA-App-Id":"frc-4774:Scouting_percentiles:1.0"})
teams = teams.json()
for team in teams:
    team_names[team["team_number"]] = team["nickname"]

# create lists of stats
auto = []
climb = []
gear = []
balls = []
while True:
	print "Enter Team Number or ENTER for all:"
	team_key = raw_input()
	if team_key == "q":
	    break
	for item in rankings:
	    if item[0] == 'Rank':
		continue

	    auto.append(item[4])
	    climb.append(item[6])
	    gear.append(item[5])
	    balls.append(item[7])

	print ""
	print len(team_key)
	for item in rankings:
	    if item[0] == 'Rank':
		continue
	    if len(team_key) > 0:
		if team_key != str(item[1]):
		    continue

	    print ""
	    print "%s. %s - %s \nAuto: %s \nClimb: %s \nGear: %s \nShooting: %s" %(item[0], item[1], team_names[item[1]],
		     stats.percentileofscore(auto, auto[item[0]-1]), stats.percentileofscore(climb, climb[item[0]-1]),
		     stats.percentileofscore(gear, gear[item[0]-1]), stats.percentileofscore(balls, balls[item[0]-1]))


quit()
