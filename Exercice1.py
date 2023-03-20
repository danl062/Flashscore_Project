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
                link = "https://www.flashscore.com/match/" + match_id[4:] + "/#/match-summary/match-statistics/0"
                match_game.append(link)
        driver.quit()
    return match_game[:20]


if __name__ == "__main__":
    url = "https://www.flashscore.com/football/europe/champions-league/standings/#/ULMctLS6/table/home"

    print(get_match_all_games(url))
