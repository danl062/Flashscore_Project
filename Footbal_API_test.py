import requests
import pymysql


def get_team_id(team_name, api_key):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"name": team_name}

    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    if 'results' in data and data["results"] > 0:
        team_data = data["response"][0]
        team_id = team_data["team"]["id"]
        return team_id
    else:
        print(f"No result for team {team_name}")
        return None


def get_coach_name(team_id, api_key):
    url = "https://api-football-v1.p.rapidapi.com/v3/coachs"

    querystring = {"team": team_id}

    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    if 'results' in data and data["results"] > 0:
        coach_data = data["response"][0]
        coach_name = coach_data["name"]
        return coach_name
    else:
        print(f"Can't find coach for this team using team ID: {team_id}")
        return None


def check_team_name(api_key, team_name):
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"name": team_name}
    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    if 'results' in data and data["results"] > 0:
        print(f"Found team {team_name} in the API")
    else:
        print(f"Team {team_name} not found in the API")


api_key = "c3d583b8e9mshf46699e3f97cf89p1a6541jsnf4d28c806dc8"

# Vérifier les noms d'équipe
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="30030705EasG:",
    database="Flashscore"
)

cursor = conn.cursor()

cursor.execute("SELECT name FROM Team")
team_names = [row[0] for row in cursor.fetchall()]

for team in team_names:
    team_id = get_team_id(team, api_key)
    if team_id:
        coach_name = get_coach_name(team_id, api_key)
        if coach_name:
            print(f"Coach found for team {team}: {coach_name}")
            cursor.execute("UPDATE Team SET coach = %s WHERE name = %s", (coach_name, team))
        else:
            print(f"Can't find coach for this team {team}")
    else:
        print(f"Can't find ID for this team {team}")

cursor.execute("SELECT name, coach FROM Team")

# We check if the result is on the DB
results = cursor.fetchall()
print("Équipe\t\tEntraîneur")
print("-------------------------------")
for row in results:
    team_name, coach_name = row
    print(f"{team_name}\t\t{coach_name}")

conn.commit()
conn.close()
