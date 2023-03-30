import pymysql

# Establish a connection to the MySQL server
conn = pymysql.connect(
 host="localhost",
 user="root",
 password="30030705EasG:",
 database="Flashscore"
)
cursor = conn.cursor()

# Create the table
cursor.execute('''CREATE TABLE IF NOT EXISTS matches
             (id INT PRIMARY KEY ,
              competition VARCHAR(32),
              match_date DATE,
              team1 VARCHAR(32),
              team2 VARCHAR(32),
              score1 INT,
              score2 INT,
              bet_home FLOAT,
              bet_draw FLOAT,
              bet_away FLOAT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS team
             (id INT PRIMARY KEY,
              Team_name VARCHAR(32))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS competition
             (id INT PRIMARY KEY,
              Competition_name VARCHAR(32))''')
conn.commit()
conn.close()
