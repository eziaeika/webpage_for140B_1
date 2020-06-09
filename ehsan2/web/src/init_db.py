# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists Users;")
cursor.execute("drop table if exists News;")
cursor.execute("drop table if exists Metrics;")
cursor.execute("drop table if exists Page_Analytics;")
cursor.execute("drop table if exists Page_Users;")
# Create a Users table (wrapping it in a try-except is good practice)

try:
  cursor.execute("""
    CREATE TABLE Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      first_name  VARCHAR(30) NOT NULL,
      last_name   VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      password    VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Users table already exists. Not recreating it.")

# Insert Records
query = "insert into Users (first_name, last_name, email, password) values (%s, %s, %s , %s)"
values = [
  ('rick','gessner','rick@gessner.com', 'password123'),
  ('ramsin','khoshabeh','ramsin@khoshabeh.com', 'password123'),
  ('joshua','ortiz','jso007@ucsd.edu' , 'password123')
]
cursor.executemany(query, values)
db.commit()


try:
  cursor.execute("""
    CREATE TABLE News (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      title       VARCHAR(200) NOT NULL,
      content     VARCHAR(2000) NOT NULL,
      dt          VARCHAR(50) default '00-00-0000-00:00:00'
    );
  """)
except:
  print("News table already exists. Not recreating it.")

# Insert Records
query = "insert into News (title, content, dt) values (%s , %s, %s)"
values = [
  ('connected front and back end','Joshua has connected the UI with backend webserver', '04-20-2020-11:59:59'),
  ('Changed Group','Joshua has been assigned to a new group so this website is obsolete in the context of the previous assignment','04-25-2020-17:59:59'),
  ('Integreated ML model' , 'Joshua Integrated the machine learning alogrithm with chatbot to provide better chatbot responses' ,'04-28-2020-17:59:59')
]
cursor.executemany(query, values)
db.commit()


try:
  cursor.execute("""
    CREATE TABLE Metrics (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      content     VARCHAR(2000) NOT NULL,
      dt          VARCHAR(50) default '00-00-0000-00:00:00'
    );
  """)
except:
  print("News table already exists. Not recreating it.")

# Insert Records
query = "insert into Metrics (content, dt) values (%s, %s)"
values = [
  ('In-Progress: Working on integrating video chat feature into application', '00-00-0000-00:00:00'),
  ('Update: Video Chat Feature integrated into application','00-00-0000-00:00:00'),
  ('In-Progress: Working on implementing feature for tutur signup and registraion' ,'00-00-0000-00:00:00')
]
cursor.executemany(query, values)
db.commit()


try:
  cursor.execute("""
    CREATE TABLE Page_Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      userID      VARCHAR(50) NOT NULL,
      page        VARCHAR(25) NOT NULL
    );
  """)
except:
  print("Page_Users table already exists. Not recreating it.")

query = "insert into Page_Users (userID , page) values (%s, %s)"

values = [
  ('jso007@ucsd.edu', 'dashboard'),
  ('jso007@ucsd.edu','home'),
  ('jso007@ucsd.edu','features'),
  ('jso007@ucsd.edu','pricing'),
  ('jso007@ucsd.edu','about')
]

cursor.executemany(query, values)
db.commit()

try:
  cursor.execute("""
    CREATE TABLE Page_Analytics (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      page        VARCHAR(25) NOT NULL,
      count       int(10) DEFAULT 0 NOT NULL
    );
  """)
except:
  print("Page_Analytics table already exists. Not recreating it.")

query = "insert into Page_Analytics (page, count) values (%s , %s)"
values = [
  ('dashboard',1),
  ('register',1),
  ('home',1),
  ('features',1),
  ('pricing',1),
  ('about',1),
  ('login',1)
]

cursor.executemany(query, values)
db.commit()

# Selecting Records
print('---------- DATABASES INITIALIZED ----------')
cursor.execute("select * from Users;")
[print(x) for x in cursor]
cursor.execute("select * from Page_Analytics;")
[print(x) for x in cursor]
cursor.execute("select * from Page_Users;")
[print(x) for x in cursor]
db.close()
