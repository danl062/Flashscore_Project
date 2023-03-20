import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import os
import re

def get_match_all_games(url):
    """ This function gives all the teams urls"""
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
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

    return team_links

def get_match_page(list_urls):
    """ This function gives the 20 last games  per team"""

    for url in list_urls:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        match_game = []
        info = soup.find_all(class_=["event__match event__match--static event__match--last event__match--twoLine", "event__match event__match--static event__match--twoLine"])
        for cell in info:
            match_id = cell.get('id')
            if match_id is not None:
                link = "https://www.flashscore.com/match/" + match_id[4:] + "/#/match-summary/match-statistics/0"
                match_game.append(link)
        driver.quit()
    return match_game[:20]

def get_match_data(url):
    """This function takes all stats and info per game"""
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
    stat_data = []
    for row in stat_rows:
        home_value = row.find(class_="stat__homeValue")
        category_name = row.find(class_="stat__categoryName")
        away_value = row.find(class_="stat__awayValue")

        if category_name:
            # Extraire le nom de la statistique en supprimant les caractères spéciaux
            category_name_text = re.sub(r'[^\w\s]', '', category_name.text.strip())

            home_value_text = home_value.text.strip() if home_value else None
            away_value_text = away_value.text.strip() if away_value else None

            stat_data.append((home_value_text, category_name_text, away_value_text))

    driver.quit()
    return team1_name, competition_info, match_date, team2_name, score1, score2, bet_winner_home, bet_draw, bet_winner_away, stat_data

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
    #url = "https://www.flashscore.com/football/europe/champions-league/standings/#/ULMctLS6/table/home"
    #get_match_all_games(url)

    #with open("team_urls.txt", "r") as file:
        #team_urls = [line.strip() for line in file]

    url = ["https://www.flashscore.com/team/fc-porto/S2NmScGp/results/"]
    my_url = "https://www.flashscore.com/team/fc-porto/S2NmScGp/results/"
    #for index, team_url in enumerate(team_urls):
    match_links = get_match_page(url)
    team_name = re.search(r'team/(.*?)/', my_url).group(1)
    print(team_name)
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



