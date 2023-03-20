import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os
from Exercice1 import get_match_page
import re

def extract_and_clean_category(row):
    category_name = row.find(class_="stat__categoryName")
    if category_name:
        info_text_element = category_name.find(class_="stat__infoText")
        if info_text_element:
            info_text_element.extract()
        return category_name.text.strip()
    return None

def get_match_data(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(10)  # attendre que la page se charge
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # ajoute le nom de la compétition en question
    competition_element = soup.find(class_="tournamentHeader__country")
    competition_info = competition_element.text.strip() if competition_element else None

    # Récupérer la date
    date_element = soup.find(class_="duelParticipant__startTime")
    match_date = date_element.text.strip() if date_element else None

    # Récupérer les noms des équipes
    team_elements = soup.find_all("div", class_=["participant__participantName", "participant__overflow"])
    team1_name = team_elements[0].text.strip() if team_elements else None
    team2_name = team_elements[1].text.strip() if team_elements else None

    # Récupérer le score
    score_element = soup.find(class_="detailScore__wrapper")
    score_text = score_element.text.strip() if score_element else None
    score1, score2 = score_text.split('-') if score_text else (None, None)

    # Récupérer les cotes des paris
    odds_elements = soup.find_all(class_="oddsValueInner")
    bet_winner_home = odds_elements[0].text.strip() if odds_elements else None
    bet_draw = odds_elements[1].text.strip() if odds_elements else None
    bet_winner_away = odds_elements[2].text.strip() if odds_elements else None

    # Liste des catégories attendues
    expected_categories = [
        "Expected Goals (xG)",
        "Ball Possession",
        "Goal Attempts",
        "Shots on Goal",
        "Shots off Goal",
        "Blocked Shots",
        "Free Kicks",
        "Corner Kicks",
        "Offsides",
        "Throw-in",
        "Goalkeeper Saves",
        "Fouls",
        "Red Cards",
        "Yellow Cards",
        "Total Passes",
        "Completed Passes",
        "Tackles",
        "Attacks",
        "Dangerous Attacks"
    ]

    # Récupérer le reste des stats
    stat_rows = soup.find_all(class_="stat__category")
    stat_data = {}

    for category in expected_categories:
        category_found = False
        for row in stat_rows:
            current_category = extract_and_clean_category(row)
            if current_category == category:
                category_found = True
                home_value = row.find(class_="stat__homeValue")
                away_value = row.find(class_="stat__awayValue")
                home_value_text = home_value.text.strip() if home_value else "0"
                away_value_text = away_value.text.strip() if away_value else "0"
                stat_data[current_category] = (home_value_text, away_value_text)
                break
        if not category_found:
            stat_data[category] = ("0", "0")

    driver.quit()

    return team1_name, competition_info, match_date, team2_name, score1, score2, bet_winner_home, bet_draw, bet_winner_away, stat_data


def save_to_csv(match_data, stat_data):
    # Vérifie si le fichier existe et s'il a un en-tête
    file_exists = os.path.isfile('match_data.csv')

    with open('match_data.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not file_exists:
            # Créer l'en-tête du fichier CSV
            header = ['Team 1', 'Competition info', 'Date', 'Team 2', 'Score 1', 'Score 2', 'Bet Winner Home',
                      'Bet Draw', 'Bet Winner Away']
            for category_name in stat_data:
                header.append(category_name + ' Home')
                header.append(category_name + ' Away')
            print(header)
            writer.writerow(header)

        # Ajouter les données du match et les données stat_data
        row_data = list(match_data)
        for category_name in stat_data:
            home_value, away_value = stat_data[category_name]
            row_data.append(home_value)
            row_data.append(away_value)

        writer.writerow(row_data)

def write_to_csv(file_name, match_data, stat_data):
    # Liste des statistiques que vous voulez inclure dans le CSV
    desired_stats = ["Expected Goals xG", "Ball Possession", "Goal Attempts", "Shots on Goal", "Shots off Goal",
                     "Blocked Shots",
                     "Free Kicks", "Corner Kicks", "Offsides", "Throwin", "Goalkeeper Saves", "Fouls",
                     "Red Cards", "Yellow Cards", "Total Passes", "Completed Passes", "Tackles", "Attacks"]

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Créer l'en-tête du fichier CSV s'il n'existe pas encore
        if file.tell() == 0:
            header = ['Team 1', 'Competition info', 'Date', 'Team 2', 'Score 1', 'Score 2', 'Bet Winner Home',
                      'Bet Draw', 'Bet Winner Away']
            for stat_name in desired_stats:
                header.append(stat_name + ' Home')
                header.append(stat_name + ' Away')
            writer.writerow(header)

        # Récupérer les données de match
        row_data = list(match_data)

        # Créer un dictionnaire pour stocker les valeurs de statistiques
        stats_dict = {}
        for home, cat_name, away in stat_data:
            # Extraire le nom de la statistique en supprimant les caractères spéciaux
            category_name = re.sub(r'[^\w\s]', '', cat_name.strip())

            for stat_name in desired_stats:
                if stat_name in category_name:
                    stats_dict[stat_name] = {'Home': home, 'Away': away}
                    print(stats_dict[stat_name])
                    break

        # Ajouter les valeurs de statistiques à la ligne de CSV
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

if __name__ == "__main__":
    reduce_teams_link = ['https://www.flashscore.com/team/fc-porto/S2NmScGp/results/']
    match_links = get_match_page(reduce_teams_link)
    with open("team_urls.txt", "r") as file:
        team_urls = [line.strip() for line in file]

    for index, team_url in enumerate(team_urls):
        match_links = get_match_page([team_url])
        pattern = r"(?<=team\/)[a-z]+(?=\/)"
        match = re.search(pattern, team_url)
        team_name = match.group().capitalize()
        file_name = f"{team_name}.csv"
        print("file created")
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
        file_exists = os.path.isfile(file_name)


        for match_url in match_links:
            match_data_all = get_match_data(match_url)
            match_data = match_data_all[:9]
            stat_data = match_data_all[9]
            write_to_csv(file_name, match_data, stat_data)

