import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import re
import json
import argparse
from datetime import datetime
import pymysql
import random
import pymysql


conn = pymysql.connect(
 host="localhost",
 user="root",
 password="raphaeld17",
 database="Flashscore"
)

cursor = conn.cursor()

link = "https://www.flashscore.com/match/ziIMHEan/#/match-summary/match-statistics/0"

def beautiful_soup(url):
    """
    Parse the url on beautiful soup
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def read_config(config_file):
    """
    Read the configuration from a JSON file and return the configuration as
    a dictionary.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


config = read_config('/Users/raphaeldelouya/Desktop/WebScrapping/my_json.json')

def competition_name(soup):
    """
    Gives the competition name
    """
    competition_element = soup.find(class_=config["COMPETITION"])
    competition_info = competition_element.text.strip() if competition_element else None
    return competition_info

def bet_winner_home(soup):
    """
    Finds the win bet for the home player
    """
    odds_elements = soup.find_all(class_=config["ODDS"])
    bet_winner_home = odds_elements[0].text.strip() if odds_elements else None
    return bet_winner_home


def bet_draw(soup):
    """
    Finds the draw bet
    """
    odds_elements = soup.find_all(class_=config["ODDS"])
    bet_draw = odds_elements[1].text.strip() if odds_elements else None
    return bet_draw


def bet_winner_away(soup):
    """
    Finds the win bet for the away player
    """
    odds_elements = soup.find_all(class_=config["ODDS"])
    bet_winner_away = odds_elements[2].text.strip() if odds_elements else None
    return bet_winner_away

def team_1(soup):
    """
    Finds the team name 1
    """
    team_elements = soup.find_all(config["DIV"], class_=[config["PARTICIPANT"], config["OVERFLOW"]])
    team1_name = team_elements[0].text.strip() if team_elements else None
    return team1_name


def team_2(soup):
    """
    Finds the team name 2
    """
    team_elements = soup.find_all(config["DIV"], class_=[config["PARTICIPANT"], config["OVERFLOW"]])
    team2_name = team_elements[1].text.strip() if team_elements else None
    return team2_name

def score_a(soup):
    """
    Finds score_a

    """

    score_element = soup.find(class_=config["SCORE"])
    score_text = score_element.text.strip() if score_element else None
    score1, score2 = score_text.split('-') if score_text else (None, None)
    return score1


def score_b(soup):
    """
    Finds score_b
    """
    score_element = soup.find(class_=config["SCORE"])
    score_text = score_element.text.strip() if score_element else None
    score1, score2 = score_text.split('-') if score_text else (None, None)
    return score2


def stat(soup):
    """
    Finds all the stats of the game
    """
    stat_rows = soup.find_all(class_=config["STAT_CATEGORY"])
    stat_data = []
    for row in stat_rows:
        home_value = row.find(class_=config["HOME_VALUE"])
        category_name = row.find(class_=config["CATEGORY_NAME"])
        away_value = row.find(class_=config["AWAY_VALUE"])

        if category_name:
            category_name_text = re.sub(r'[^\w\s]', '', category_name.text.strip())

            home_value_text = home_value.text.strip() if home_value else None
            away_value_text = away_value.text.strip() if away_value else None

            stat_data.append((home_value_text, category_name_text, away_value_text))
    return stat_data


def stat_arrange(stat_data):
    desired_stats = config["DESIRED_STATS"]
    stats_dict = {}
    new_list = []
    for home, cat_name, away in stat_data:
        category_name = re.sub(r'[^\w\s]', '', cat_name.strip())

        for stat_name in desired_stats:
            if stat_name in category_name:
                stats_dict[stat_name] = {'Home': home, 'Away': away}
                break

    for stat_name in desired_stats:
        if stat_name in stats_dict:
            home_value = stats_dict[stat_name]['Home']
            away_value = stats_dict[stat_name]['Away']
        else:
            home_value = '0'
            away_value = '0'

        new_list.append(home_value if home_value else '0')
        new_list.append(away_value if away_value else '0')

    return new_list

def date_element(soup):
    """
    Gives the date of the game
    """
    date_element = soup.find(class_=config["DATE"])
    match_date = date_element.text.strip() if date_element else None
    return match_date

def insert_competition_name(competition_info, cursor):
    """
    Inserts the competition name into the 'competition' table in the database
    """
    cursor.execute("SELECT id FROM Competition WHERE name = %s", (competition_info,))
    existing_competition = cursor.fetchone()
    if existing_competition is None:
        query = "INSERT INTO Competition (name) VALUES (%s)"
        values = (competition_info,)
        cursor.execute(query, values)
        conn.commit()
        existing_competition = cursor.lastrowid
    return existing_competition[0] if existing_competition else None

def insert_odds(odds,cursor):
    cursor.execute("SELECT id FROM Odds WHERE home_win_odds = %s AND draw_odds = %s AND away_win_odds = %s", odds)
    existing_odds = cursor.fetchone()
    if existing_odds is None:
        query = "INSERT INTO Odds (home_win_odds, draw_odds, away_win_odds) VALUES (%s, %s, %s)"
        values = (odds[0], odds[1], odds[2])
        cursor.execute(query, values)
        conn.commit()
        last_row = cursor.lastrowid
        return last_row
    else:
        return existing_odds[0]

def insert_name(name,cursor):
    cursor.execute("SELECT id FROM Team WHERE name = %s", name)
    existing_name = cursor.fetchone()
    if existing_name is None:
        query = "INSERT INTO Team (name) VALUES (%s)"
        values = name
        cursor.execute(query, values)
        conn.commit()
        last_row = cursor.lastrowid
        return last_row
    else:
        return existing_name[0]

def insert_stats(stats, cursor):
    cursor.execute("SELECT id FROM Stat WHERE expected_goals_home = %s", stats[0])
    existing_id = cursor.fetchone()
    if existing_id is None:
        query = "INSERT INTO Stat2 (expected_goals_home, expected_goals_away, ball_possession_home, ball_possession_away, goal_attempts_home, goal_attempts_away,shots_on_goal_home,shots_on_goal_away,shots_off_goal_home,shots_off_goal_away) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        values = (stats[0],stats[1],stats[2],stats[3], int(stats[4]), int(stats[5]), int(stats[6]), int(stats[7]), int(stats[8]), int(stats[9]))
        cursor.execute(query, values)
        conn.commit()
        last_row = cursor.lastrowid
        return last_row
    else:
        return existing_id[0]

def insert_match(match_info, cursor):
    query = "SELECT id FROM Game WHERE date=%s AND competition_id=%s AND odds_id=%s AND team1_id=%s AND team2_id=%s AND stat_id=%s AND score1=%s AND score2=%s"
    values = (match_info[0],match_info[1],match_info[2],match_info[3],match_info[4],match_info[5],match_info[6],match_info[7])
    cursor.execute(query, values)
    existing_match = cursor.fetchone()

    if existing_match is None:
        query = "INSERT INTO Game (date, competition_id, odds_id, team1_id, team2_id, stat_id, score1, score2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (match_info[0],match_info[1],match_info[2], match_info[3],match_info[4],match_info[5],match_info[6],match_info[7])
        cursor.execute(query, values)


def main():
    url = beautiful_soup("https://www.flashscore.com/match/Y5C9gS5P/#/match-summary/match-statistics/0")

    date = date_element(url)

    competition_1 = competition_name(url)
    comp_id = insert_competition_name(competition_1, cursor)
    print(comp_id)

    odds_1 = [bet_winner_home(url), bet_draw(url), bet_winner_away(url)]
    odds_id = insert_odds(odds_1, cursor)
    print(odds_id)

    team_a = team_1(url)
    team_b = team_2(url)

    team_a_id = insert_name(team_a, cursor)
    team_b_id = insert_name(team_b, cursor)
    print(team_a_id)
    print(team_b_id)

    my_stat = stat(url)
    test = stat_arrange(my_stat)

    stat_id = insert_stats(test, cursor)
    print(stat_id)

    score_1 = score_a(url)
    score_2 = score_b(url)

    #match_info = [date, comp_id, odds_id, team_a_id, team_b_id, stat_id, score_1, score_2]
    #print(match_info)
    #insert_match(match_info, cursor) (TOO LONG TO RUN - WE DIDN'T SUCCEED YET)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
