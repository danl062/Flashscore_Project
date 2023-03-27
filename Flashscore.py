import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import re
import argparse
from datetime import datetime


def get_match_all_games(my_url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.get(my_url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        team_links = []
        image_cells = soup.find_all(class_="tableCellParticipant__image")
        for cell in image_cells:
            href = cell.get('href')
            team_links.append('https://www.flashscore.com' + href + "results/")

        with open("team_urls.txt", "w") as file:
            for link in team_links:
                file.write(link + "\n")
        driver.quit()

    except Exception as e:
        print(f"Error in get_match_all_games: {e}")
        team_links = []

    return team_links


def get_match_page(list_urls):
    match_game = []

    for url_ele in list_urls:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome(options=options)
            driver.get(url_ele)
            time.sleep(10)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            info = soup.find_all(class_=["event__match event__match--static event__match--last event__match--twoLine",
                                         "event__match event__match--static event__match--twoLine"])
            for cell in info:
                match_id = cell.get('id')
                if match_id is not None:
                    link = "https://www.flashscore.com/match/" + match_id[4:] + "/#/match-summary/match-statistics/0"
                    match_game.append(link)
            driver.quit()
        except Exception as e:
            print(f"Error in get_match_page: {e}")

    return match_game[:20]


def get_match_data(url):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"Error in get_match_data (loading page): {e}")
        return None, None, None, None, None, None, None, None, None, []

    try:
        competition_element = soup.find(class_="tournamentHeader__country")
        competition_info = competition_element.text.strip() if competition_element else None

        date_element = soup.find(class_="duelParticipant__startTime")
        match_date = date_element.text.strip() if date_element else None

        team_elements = soup.find_all("div", class_=["participant__participantName", "participant__overflow"])
        team1_name = team_elements[0].text.strip() if team_elements else None
        team2_name = team_elements[1].text.strip() if team_elements else None

        score_element = soup.find(class_="detailScore__wrapper")
        score_text = score_element.text.strip() if score_element else None
        score1, score2 = score_text.split('-') if score_text else (None, None)

        odds_elements = soup.find_all(class_="oddsValueInner")
        bet_winner_home = odds_elements[0].text.strip() if odds_elements else None
        bet_draw = odds_elements[1].text.strip() if odds_elements else None
        bet_winner_away = odds_elements[2].text.strip() if odds_elements else None

        stat_rows = soup.find_all(class_="stat__category")
        stat_data = []
        for row in stat_rows:
            home_value = row.find(class_="stat__homeValue")
            category_name = row.find(class_="stat__categoryName")
            away_value = row.find(class_="stat__awayValue")

            if category_name:
                category_name_text = re.sub(r'[^\w\s]', '', category_name.text.strip())

                home_value_text = home_value.text.strip() if home_value else None
                away_value_text = away_value.text.strip() if away_value else None

                stat_data.append((home_value_text, category_name_text, away_value_text))

        driver.quit()

    except Exception as e:
        print(f"Error in get_match_data (parsing data): {e}")
        return None, None, None, None, None, None, None, None, None, []

    return team1_name, competition_info, match_date, team2_name, score1, score2, bet_winner_home, bet_draw, bet_winner_away, stat_data


def write_to_csv(my_file, match_data, stat_data):
    try:
        desired_stats = ["Expected Goals xG", "Ball Possession", "Goal Attempts", "Shots on Goal", "Shots off Goal",
                         "Blocked Shots",
                         "Free Kicks", "Corner Kicks", "Offsides", "Throwin", "Goalkeeper Saves", "Fouls",
                         "Red Cards", "Yellow Cards", "Total Passes", "Completed Passes", "Tackles", "Attacks"]

        with open(my_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if file.tell() == 0:
                header = ['Team 1', 'Competition info', 'Date', 'Team 2', 'Score 1', 'Score 2', 'Bet Winner Home',
                          'Bet Draw', 'Bet Winner Away']
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
    parser.add_argument('--url', type=str, default="https://www.flashscore.com/football/europe/champions-league/standings/#/ULMctLS6/table/home",
                        help="URL of the football league standings page (default: %(default)s)")
    parser.add_argument('--mode', choices=['all', 'date_range'], default='all',
                        help="Choose scraping mode: 'all' to scrape everything or 'date_range' to scrape matches within a specific date range (default: %(default)s)")
    parser.add_argument('--date-range', nargs=2, metavar=("START_DATE", "END_DATE"), help="Scrape only matches played between START_DATE and END_DATE, in format YYYY-MM-DD (requires '--mode date_range')")

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
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date, "%Y-%m-%d")
                        match_date = datetime.strptime(game_match_data[2], "%Y-%m-%d")
                        if not (start_date <= match_date <= end_date):
                            continue

                    write_to_csv(file_name, game_match_data, game_stat_data)
            except Exception as e:
                print(f"Error in main (processing team {index}): {e}")

    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()