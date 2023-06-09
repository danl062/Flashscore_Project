import pymysql


def create_database():
    conn = pymysql.connect(
        host="data-mining-db1.cttpnp4olbpx.us-west-1.rds.amazonaws.com",
        user="raphael-dan",
        password="raphael_dan",
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS raphael_dan")
    cursor.close()
    conn.close()


def create_tables():
    conn = pymysql.connect(
        host="data-mining-db1.cttpnp4olbpx.us-west-1.rds.amazonaws.com",
        user="raphael_dan",
        password="raphael_dan",
        database='raphael_dan'
    )

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Team ("
                   "id INT NOT NULL AUTO_INCREMENT,"
                   "name VARCHAR(255) NOT NULL,"
                   "PRIMARY KEY (id)"
                   ")")

    cursor.execute("CREATE TABLE IF NOT EXISTS Competition ("
                   "id INT NOT NULL AUTO_INCREMENT,"
                   "name VARCHAR(255) NOT NULL,"
                   "PRIMARY KEY (id)"
                   ")")

    cursor.execute("CREATE TABLE IF NOT EXISTS Stat ("
                   "id INT NOT NULL AUTO_INCREMENT,"
                   "expected_goals_home FLOAT,"
                   "expected_goals_away FLOAT,"
                   "ball_possession_home VARCHAR(255),"
                   "ball_possession_away VARCHAR(255),"
                   "goal_attempts_home INT,"
                   "goal_attempts_away INT,"
                   "shots_on_goal_home INT,"
                   "shots_on_goal_away INT,"
                   "shots_off_goal_home INT,"
                   "shots_off_goal_away INT,"
                   "PRIMARY KEY (id)"
                   ")")

    cursor.execute("CREATE TABLE IF NOT EXISTS Odds ("
                   "id INT NOT NULL AUTO_INCREMENT,"
                   "home_win_odds FLOAT NOT NULL,"
                   "draw_odds FLOAT NOT NULL,"
                   "away_win_odds FLOAT NOT NULL,"
                   "PRIMARY KEY (id)"
                   ")")

    cursor.execute("CREATE TABLE IF NOT EXISTS Game ("
                   "id INT NOT NULL AUTO_INCREMENT,"
                   "date VARCHAR(255) NOT NULL,"
                   "competition_id INT NOT NULL,"
                   "odds_id INT NOT NULL,"
                   "team1_id INT NOT NULL,"
                   "team2_id INT NOT NULL,"
                   "stat_id INT NOT NULL,"
                   "score1 INT,"
                   "score2 INT,"
                   "PRIMARY KEY (id),"
                   "FOREIGN KEY (competition_id) REFERENCES Competition(id),"
                   "FOREIGN KEY (odds_id) REFERENCES Odds(id),"
                   "FOREIGN KEY (team1_id) REFERENCES Team(id),"
                   "FOREIGN KEY (team2_id) REFERENCES Team(id),"
                   "FOREIGN KEY (stat_id) REFERENCES Stat(id)"
                   ")")
    conn.close()


if __name__ == '__main__':
    create_database()
    create_tables()
