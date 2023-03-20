import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os
from Exercice1 import get_match_page


def get_match_data(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(10)  # attendre que la page se charge
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #ajoute le nom de la compétition en question
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

    #récupère le reste des stats
    stat_rows = soup.find_all(class_="stat__category")
    print(stat_rows)
    stat_data = []
    for row in stat_rows:
        home_value = row.find(class_="stat__homeValue")
        category_name = row.find(class_="stat__categoryName")
        away_value = row.find(class_="stat__awayValue")

        # Exclure le texte indésirable
        info_text_element = category_name.find(class_="stat__infoText")
        if info_text_element:
            info_text_element.extract()

        home_value_text = home_value.text.strip() if home_value else None
        category_name_text = category_name.text.strip() if category_name else None
        away_value_text = away_value.text.strip() if away_value else None

        # Exclure Expected Goals (xG) de la liste stat_data
        if "Expected Goals (xG)" in category_name_text:
            continue
        else:
            stat_data.append((home_value_text, category_name_text, away_value_text))

        #stat_data.append((home_value_text, category_name_text, away_value_text))

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
            for _, category_name, _ in stat_data:
                header.append(category_name + ' Home')
                header.append(category_name + ' Away')
            print(header)
            writer.writerow(header)

        # Ajouter les données du match et les données stat__row
        row_data = list(match_data)
        for home_value, _, away_value in stat_data:
            row_data.append(home_value)
            row_data.append(away_value)

        writer.writerow(row_data)


if __name__ == "__main__":
    reduce_teams_link = ['https://www.flashscore.com/team/napoli/69Dxbc61/results/']
    match_links = get_match_page(reduce_teams_link)

    for match_url in match_links:
        match_data_all = get_match_data(match_url)
        match_data = match_data_all[:9]
        stat_data = match_data_all[9]

        print(match_data)
        save_to_csv(match_data, stat_data)
