# Web Scraper for Flashscore.com
This web scraper extracts data on football games from Flashscore.com. Specifically, it collects information on team names, competition names, match dates, scores, betting odds, and statistics for a given game.
To run the main script, execute `main_scrapper.py`. This script will prompt you to choose which of the following scripts to run:

1. SCRAPPER_CSV.py
2. SCRAPPER_SQL.py
3. SCRAPPER_API.py

## Warning:
You might need to press "2" in order to get more data in the database before using the option "3". The more data you have, the better the experience is ;)

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

## Part C:
This script updates the coach column in a MySQL database table named Team. It fetches coach information for each team using the API-Football API and then updates the database.

##### Imports:

* requests: For making HTTP requests to the API.
* pymysql: For interacting with a MySQL database.
* difflib.SequenceMatcher: For comparing the similarity of two strings.
* re: For using regular expressions to remove text inside parentheses.
* fuzzywuzzy.fuzz and fuzzywuzzy.process: For fuzzy string matching.

##### Functions:

1. coach_exists_in_db(team_name, cursor): Checks if a coach exists for the given team in the database.
2. update_coach_in_db(team_name, coach_name, cursor): Updates the coach name for the given team in the database.
3. remove_parentheses_info(name): Removes text inside parentheses from a string.
4. similar(a, b): Calculates the similarity ratio of two strings using SequenceMatcher.
5. get_team_id(team_name, api_key): Retrieves the team ID from API-Football using the team name.
6. get_coach_name(team_id, api_key): Retrieves the coach name for a team using the team ID from API-Football.
7. check_team_name(api_key, team_name): Checks if the team name exists in API-Football and returns the most similar name if found.

#### Main script:

1. Sets the API key and database connection details.
2. Connects to the MySQL database and creates a cursor object. 
3. Checks if the coach column exists in the Team table, if not, adds the column. 
4. Retrieves a list of team names from the Team table. 
5. Iterates through each team name and checks if a coach already exists in the database. If not:
   * Removes text inside parentheses from the team name. 
   * Checks if the team name exists in API-Football using fuzzy matching. 
   * If found, retrieves the team ID, coach name and country from API-Football. 
   * Updates the coach name in the database. 
6. Closes the cursor and database connection.

#### Output:

The script prints the status of each team as it processes them. After updating the coaches, it prints a table with each team's name and coach name.

#### Warning:
Do not stop the program! 
Because we used a free api account, we are allowed to run only a few queries per minute. 
This is why the code runs queries avoiding the values already put inside, in order to not loose queries for nothing.
But most of the API responses are: "Status code: 429", meaning that we have exceeded the rate limit per minute for your plan.
So please do not stop the program before it ends.



