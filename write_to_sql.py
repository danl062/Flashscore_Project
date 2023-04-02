import pymysql

# Establish a connection to the MySQL server
conn = pymysql.connect(
 host="localhost",
 user="root",
 password="30030705EasG:",
 database="Flashscore"
)

cursor = conn.cursor()

# Create the table Team
cursor.execute("CREATE TABLE IF NOT EXISTS Team ("
               "id INT NOT NULL AUTO_INCREMENT,"
               "Team_name VARCHAR(255) NOT NULL,"
               "PRIMARY KEY (id)"
               ")")

# Create the table Competition
cursor.execute("CREATE TABLE IF NOT EXISTS Competition ("
               "id INT NOT NULL AUTO_INCREMENT,"
               "Competition_name VARCHAR(255) NOT NULL,"
               "PRIMARY KEY (id)"
               ")")


# Create the table Stat
cursor.execute("CREATE TABLE IF NOT EXISTS Stat ("
               "id INT NOT NULL AUTO_INCREMENT,"
               "Expected_Goals FLOAT,"
               "Ball_Possession FLOAT,"
               "Goal_Attempts INT,"
               "Shots_on_Goal INT,"
               "Shots_off_Goal INT,"
               "Blocked_shots INT,"
               "Free_kicks INT,"
               "Corner_kicks INT,"
               "Offsides INT,"
               "Throw_in INT,"
               "Goalkeeper_saves INT,"
               "Fouls INT,"
               "Yellow_cards INT,"
               "Red_cards INT,"
               "Total_passes INT,"
               "Completed_passes INT,"
               "Tackles INT,"
               "Attacks INT,"
               "Dangerous_attacks INT,"
               "PRIMARY KEY (id)"
               ")")

# Create the table Matchs
cursor.execute("CREATE TABLE IF NOT EXISTS Matchs ("
               "id INT NOT NULL AUTO_INCREMENT,"
               "match_date VARCHAR(255) NOT NULL,"
               "competition_id INT NOT NULL,"
               "team1_id INT NOT NULL,"
               "team2_id INT NOT NULL,"
               "home_stat_id INT NOT NULL,"
               "away_stat_id INT NOT NULL,"
               "score1 INT,"
               "score2 INT,"
               "PRIMARY KEY (id),"
               "FOREIGN KEY (competition_id) REFERENCES Competition(id),"
               "FOREIGN KEY (team1_id) REFERENCES Team(id),"
               "FOREIGN KEY (team2_id) REFERENCES Team(id),"
               "FOREIGN KEY (home_stat_id) REFERENCES Stat(id),"
               "FOREIGN KEY (away_stat_id) REFERENCES Stat(id)"
               ")")

# Create the table Odds
cursor.execute("CREATE TABLE IF NOT EXISTS Odds ("
               "id INT NOT NULL AUTO_INCREMENT,"
               "match_id INT NOT NULL,"
               "home_bet_winner FLOAT NOT NULL,"
               "draw_bet FLOAT NOT NULL,"
               "away_bet_winner FLOAT NOT NULL,"
               "PRIMARY KEY (id),"
               "FOREIGN KEY (match_id) REFERENCES Matchs(id)"
               ")")

conn.close()