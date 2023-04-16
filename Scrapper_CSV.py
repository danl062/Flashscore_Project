import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import re
import json
import argparse
from datetime import datetime

config = {}


def read_config(config_file):
    """
    Read the configuration from a JSON file and return the configuration as
    a dictionary.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


config = read_config('my_json.json')


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


def competition_name(soup):
    """
    Gives the competition name
    """
    competition_element = soup.find(class_=config["COMPETITION"])
    competition_info = competition_element.text.strip() if competition_element else None
    return competition_info


def date_element(soup):
    """
    Gives the date of the game
    """
    date_element = soup.find(class_=config["DATE"])
    match_date = date_element.text.strip() if date_element else None
    return match_date


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


def get_match_all_games(my_url):
    """
    Finds all the result URLs and returns it as a list
    """
    try:
        team_links = []
        soup = beautiful_soup(my_url)
        image_cells = soup.find_all(class_=config["ALL_GAMES"])
        for cell in image_cells:
            href = cell.get('href')
            team_links.append('https://www.flashscore.com' + href + "results/")

        with open("team_urls.txt", "w") as file:
            for link in team_links:
                file.write(link + "\n")

    except Exception as e:
        print(f"Error in get_match_all_games: {e}")
        team_links = []

    return team_links


def get_match_data(url):
    """
    Returns all the information of a game
    """
    parse = beautiful_soup(url)
    team1_name = team_1(parse)
    competition_info = competition_name(parse)
    match_date = date_element(parse)
    team2_name = team_2(parse)
    score1 = score_a(parse)
    score2 = score_b(parse)
    bet_home = bet_winner_home(parse)
    bet_draw_value = bet_draw(parse)
    bet_away = bet_winner_away(parse)
    stat_data = stat(parse)
    return team1_name, competition_info, match_date, team2_name, score1, score2, bet_home, \
        bet_draw_value, bet_away, stat_data


def get_match_page(list_urls):
    """
    Find the list of the last 20 games of a team
    """
    match_game = []

    for url_ele in list_urls:
        try:
            soup = beautiful_soup(url_ele)
            info = soup.find_all(class_=[config["GET_MATCH_PAGE"],
                                         config["GET_MATCH_PAGE_2"]])
            for cell in info:
                match_id = cell.get('id')
                if match_id is not None:
                    link = "https://www.flashscore.com/match/" + match_id[4:] + "/#/match-summary/match-statistics/0"
                    match_game.append(link)
        except Exception as e:
            print(f"Error in get_match_page: {e}")

    return match_game[:20]


def write_to_csv(my_file, match_data, stat_data):
    try:
        desired_stats = config["DESIRED_STATS"]

        with open(my_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                header = config["HEADER"]
                for stat_name in desired_stats:
                    header.append(stat_name + ' Home')
                    header.append(stat_name + ' Away')
                writer.writerow(header)

            row_data = list(match_data)

            stats_dict = {}
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

                row_data.append(home_value if home_value else '0')
                row_data.append(away_value if away_value else '0')

            writer.writerow(row_data)

    except Exception as e:
        print(f"Error in write_to_csv: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrape football match data from flashscore.com. "
                                                 "By default, it will scrape all matches. "
                                                 "Use the appropriate arguments to customize the scraping process.")
    parser.add_argument('--url', type=str,
                        default="https://www.flashscore.com/football/europe/champions-league/standings/#/ULMctLS6"
                                "/table/home",
                        help="URL of the football league standings page (default: %(default)s)")
    parser.add_argument('--mode', choices=['all', 'date_range'], default='all',
                        help="Choose scraping mode: 'all' to scrape everything or 'date_range' to scrape matches "
                             "within a specific date range (default: %(default)s)")
    parser.add_argument('--date-range', nargs=2, metavar=("START_DATE", "END_DATE"),
                        help="Scrape only matches played between START_DATE and END_DATE, in format YYYY-MM-DD ("
                             "requires '--mode date_range')")

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        url = args.url
        team_links = get_match_all_games(url)

        for index, team_url in enumerate(team_links):
            try:
                match_links = get_match_page([team_url])
                team_name = re.search(r'team/(.*?)/', team_url).group(1)
                file_name = f"{team_name}.csv"
                print("file created")

                for match_url in match_links:
                    match_data_all = get_match_data(match_url)
                    game_match_data = match_data_all[:9]
                    game_stat_data = match_data_all[9]

                    # Check if the match is within the specified date range, if required
                    if args.mode == 'date_range' and args.date_range:
                        start_date, end_date = args.date_range
                        start_date = datetime.strptime(start_date, config["DATE_FORMAT"])
                        end_date = datetime.strptime(end_date, config["DATE_FORMAT"])
                        match_date = datetime.strptime(game_match_data[2], config["DATE_FORMAT"])
                        if not (start_date <= match_date <= end_date):
                            continue

                    write_to_csv(file_name, game_match_data, game_stat_data)
            except Exception as e:
                print(f"Error in main (processing team {index}): {e}")

    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
