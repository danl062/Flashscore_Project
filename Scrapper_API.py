import requests
import pymysql
from difflib import SequenceMatcher
import re
from fuzzywuzzy import process

api_key = "bf15cd0eb6msh5495d524da55f3bp17ca13jsna6b806cbacfe"

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="PASSWORD",
    database="Flashscore"
)

cursor = conn.cursor()

cursor.execute("SHOW COLUMNS FROM Team LIKE 'venue'")
result = cursor.fetchone()

if not result:
    cursor.execute("ALTER TABLE Team ADD COLUMN venue VARCHAR(255)")

cursor.execute("SHOW COLUMNS FROM Team LIKE 'country'")
result = cursor.fetchone()

if not result:
    cursor.execute("ALTER TABLE Team ADD COLUMN country VARCHAR(255)")

cursor.execute("SELECT name FROM Team")
team_names = [row[0] for row in cursor.fetchall()]


def venue_exists_in_db(team_name, cursor_db):
    cursor_db.execute("SELECT venue FROM Team WHERE name = %s", (team_name,))
    result_venue = cursor_db.fetchone()

    return result_venue is not None and result_venue[0] is not None


def country_exists_in_db(team_name, cursor_db):
    cursor_db.execute("SELECT country FROM Team WHERE name = %s", (team_name,))
    result_country = cursor_db.fetchone()

    return result_country is not None and result_country[0] is not None


def remove_parentheses_info(name):
    """
    Removes any substring in the form of parentheses and its contents from a given string.
    """
    return re.sub(r'\s*\([^)]*\)', '', name)


def similar(a, b):
    """
    Returns a similarity score between two strings using the SequenceMatcher algorithm.
    """
    return SequenceMatcher(None, a, b).ratio()


def extracts_api_name(team_name, football_api_key):
    """
    Extracts information about a football team from the API-Football API.
    """
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"name": team_name}
    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": football_api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


def extracts_api_id(team_id, football_api_key):
    """
    Extracts information about a football team from the API-Football API.
    """
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    querystring = {"id": team_id}
    headers = {
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
        "x-rapidapi-key": football_api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data


def get_team_id(team_name, football_api_key):
    """
    Retrieves the ID of a football team from the API-Football API.
    """
    data = extracts_api_name(team_name, football_api_key)
    if 'results' in data and data["results"] > 0:
        team_data = data["response"][0]
        team_id = team_data["team"]["id"]
        return team_id
    else:
        print(f"No result for team {team_name}")
        return None


def get_venue_name(team_id, football_api_key):
    """
    Retrieves the name of the venue associated with a football team from the API-Football API.
    """
    data = extracts_api_id(team_id, football_api_key)
    if 'results' in data and data["results"] > 0:
        venue_data = data["response"][0]
        venue_name = venue_data["venue"]['name']
        return venue_name
    else:
        print(f"Can't find venue for this team using team ID: {team_id}")
        return None


def get_country(team_id, football_api_key):
    """
    Retrieves the country associated with a football team from the API-Football API.
    """
    data = extracts_api_id(team_id, football_api_key)
    if 'results' in data and data["results"] > 0:
        country_data = data["response"][0]
        country = country_data["team"]['country']
        return country
    else:
        print(f"Can't find country for this team using team ID: {team_id}")
        return None


def check_team_name(football_api_key, team_name):
    """
    Checks if a football team with the given name exists in the API-Football API.
    """
    data = extracts_api_name(team_name, football_api_key)
    if 'results' in data and data["results"] > 0:
        team_data = data["response"]
        football_team_names = [team["team"]["name"] for team in team_data]
        team_api_name, score = process.extractOne(team_name, football_team_names)
        if score >= 30:
            print(f"Found team {team_api_name} in the API")
            return team_api_name
        else:
            print(f"Team {team_name} not found in the API")
            return None
    else:
        print(f"Team {team_name} not found in the API")
        return None


def update_venue(venue_name, team):
    """
    Updates the venue for a given football team in the database.
    """
    if venue_name:
        cursor.execute("UPDATE Team SET venue = %s WHERE name = %s", (venue_name, team))
    else:
        print(f"Can't find venue for this team {team}")


def update_country(country_name, team):
    """
    Updates the country for a given football team in the database.
    """
    if country_name:
        cursor.execute("UPDATE Team SET country = %s WHERE name = %s", (country_name, team))
    else:
        print(f"Can't find country for this team {team}")


def update_tables(football_team_names):
    """
    Update columns venue and country of table Team
    """
    for team in football_team_names:
        try:
            if not venue_exists_in_db(team, cursor) or not country_exists_in_db(team, cursor):
                team_db_name = remove_parentheses_info(team)
                team_api_name = check_team_name(api_key, team_db_name)
                if team_api_name:
                    team_id = get_team_id(team_api_name, api_key)
                    if team_id:
                        venue_name = get_venue_name(team_id, api_key)
                        update_venue(venue_name, team)
                        country_name = get_country(team_id, api_key)
                        update_country(country_name, team)
                    else:
                        print(f"Can't find ID for this team {team}")
                else:
                    print(f"Team {team} not found in the API")
            else:
                print(f"Venue or country for team {team} already exists in the database")
        except Exception as e:
            print(f"Error processing team {team}: {e}")
            pass
    conn.commit()
    conn.close()


if __name__ == '__main__':
    update_tables(team_names)
