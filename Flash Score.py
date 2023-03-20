import time
from selenium import webdriver
from bs4 import BeautifulSoup


def get_match_all_games(url):
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
    driver.quit()
    return team_links


def get_match_page(list_urls):
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
                link = "https://www.flashscore.com/match/" + match_id[4:] + "/#/match-summary/match-summary"
                match_game.append(link)
        driver.quit()
    return match_game


if __name__ == "__main__":
    url = "https://www.flashscore.com/football/europe/champions-league/standings/#/ULMctLS6/table/home"
    teams_link = ['https://www.flashscore.com/team/napoli/69Dxbc61/results/',
                  'https://www.flashscore.com/team/liverpool/lId4TMwf/results/',
                  'https://www.flashscore.com/team/ajax/8UOvIwnb/results/',
                  'https://www.flashscore.com/team/rangers/8vAWQXNS/results/',
                  'https://www.flashscore.com/team/fc-porto/S2NmScGp/results/',
                  'https://www.flashscore.com/team/club-brugge/rgTHIK74/results/',
                  'https://www.flashscore.com/team/atl-madrid/jaarqpLQ/results/',
                  'https://www.flashscore.com/team/bayer-leverkusen/4jcj2zMd/results/',
                  'https://www.flashscore.com/team/bayern-munich/nVp0wiqd/results/',
                  'https://www.flashscore.com/team/inter/Iw7eKK25/results/',
                  'https://www.flashscore.com/team/barcelona/SKbpVP5K/results/',
                  'https://www.flashscore.com/team/plzen/2LA0e86b/results/',
                  'https://www.flashscore.com/team/tottenham/UDg08Ohm/results/',
                  'https://www.flashscore.com/team/eintracht-frankfurt/8vndvXTk/results/',
                  'https://www.flashscore.com/team/marseille/SblU3Hee/results/',
                  'https://www.flashscore.com/team/sporting-lisbon/tljXuHBC/results/',
                  'https://www.flashscore.com/team/chelsea/4fGZN2oK/results/',
                  'https://www.flashscore.com/team/ac-milan/8Sa8HInO/results/',
                  'https://www.flashscore.com/team/salzburg/Olvehxrl/results/',
                  'https://www.flashscore.com/team/din-zagreb/8G5ufQTg/results/',
                  'https://www.flashscore.com/team/real-madrid/W8mj7MDD/results/',
                  'https://www.flashscore.com/team/rb-leipzig/KbS1suSm/results/',
                  'https://www.flashscore.com/team/shakhtar/4ENWX2OA/results/',
                  'https://www.flashscore.com/team/celtic/QFKRRD8M/results/',
                  'https://www.flashscore.com/team/manchester-city/Wtn9Stg0/results/',
                  'https://www.flashscore.com/team/dortmund/nP1i5US1/results/',
                  'https://www.flashscore.com/team/fc-copenhagen/hSPZwbEh/results/',
                  'https://www.flashscore.com/team/sevilla/h8oAv4Ts/results/',
                  'https://www.flashscore.com/team/paris-sg/CjhkPw0k/results/',
                  'https://www.flashscore.com/team/benfica/zBkyuyRI/results/',
                  'https://www.flashscore.com/team/juventus/C06aJvIB/results/',
                  'https://www.flashscore.com/team/maccabi-haifa/zVucZzyE/results/']


    reduce_teams_link = ['https://www.flashscore.com/team/napoli/69Dxbc61/results/']
    #print(get_match_all_games(url))
    print(get_match_page(reduce_teams_link))
