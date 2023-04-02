# Web Scraper for Flashscore.com
This web scraper extracts data on football games from Flashscore.com. Specifically, it collects information on team names, competition names, match dates, scores, betting odds, and statistics for a given game.
## Part A:
### Requirements
This code was written in Python 3.8.5 and uses the following libraries:

* selenium
* beautifulsoup4
* csv
* re
* json
* argparse

You can install these packages using pip:

##### Copy code
#### 'pip install selenium beautifulsoup4 csv re json argparse'

Additionally, you will need to download the ChromeDriver executable and add it to your system path. This is necessary for the selenium library to work properly.

#### Usage
To use the scraper, you will need to provide a JSON file that contains the configuration for the specific website you want to scrape. An example configuration file my_json.json is included in this repository. You can modify this file to fit your needs.

Once you have set up your configuration file, you can run the scraper with the following command


##### Copy code
#### python scraper.py --url <match_url> --output <output_file>
Replace <match_url> with the URL of the match you want to scrape, and <output_file> with the name of the output file you want to create.

The scraper will extract the relevant data from the match page and write it to a CSV file with the given name. The CSV file will be saved in the same directory as the scraper.py script.

If you want to scrape data for multiple matches, you can use the get_match_all_games function to retrieve a list of URLs for all the matches. You can then loop through the URLs and call the get_match_data function to extract the data for each match.

## Part B:
Web Scraping and Database Insertion
This is a Python script that extracts data from a website using web scraping techniques and saves it into a MySQL database. The script is designed to work with Flashscore website, but can be modified to work with other websites as well.

### Requirements

* Python 3.x
* Selenium
* Beautiful Soup 4
* MySQL

### Usage:
The script uses the pymysql library to establish a connection with the MySQL server and creates five tables in the "Flashscore" database. The tables created are "Team", "Competition", "Stat", "Odds", and "Game". The "Team" and "Competition" tables have two columns each for the team and competition names, respectively. The "Stat" table has ten columns for storing various statistics of the game. The "Odds" table has three columns for storing the betting odds for the game. Finally, the "Game" table has eight columns for storing the date, competition ID, odds ID, team 1 ID, team 2 ID, stat ID, score 1, and score 2 of each game.


### Installation
Clone the repository to your local machine using git clone.
Install the required dependencies using pip install -r requirements.txt.
Create a MySQL database and update the database connection details in the main() function of the web_scraping.py file.
Update the configuration details in the my_json.json file to match the structure of the webpage you are scraping.
Run the script using python web_scraping.py.
Usage
The script uses the Selenium library to interact with the website and the Beautiful Soup library to parse the HTML code. The configuration data is stored in a JSON file, which is read by the script to identify the location of the data on the webpage. The MySQL database connection details are also stored in the script.

The script defines several functions to extract specific pieces of information from the webpage, such as the competition name, the betting odds, the team names, the score, and the statistics of the game. Finally, the extracted data is inserted into the database using SQL queries.