# ECE656-DB-Analysis

1. Introduction

This server-client data mining system aims to analyze whether a player can be nominated to Hall of Fame, whether can be inducted into Hall of Fame and wether he will become manager later, based on his performance in batting, fielding, pitching or all. 

2. Client function

The client interface contains three parts: Data cleaning, Data Analysis and Data Validation. 

Data Cleaning is for adding indexes and removing incorrect values of playerID and teamID in Batting, Fielding, Pitching, AwardsPlayers, HallOfFame and Managers tables, refer to Master table. 

Data Analysis is to give overall accuary and f1 score for prediction. User can select their desired source for analysis: using individual table or all tables. And then choose the analysis type: HallofFame nomination, HallofFame or will become a manager. The result will be print in the output log. 

Data Validation is to give individual prediction by player name. The prediction value and real value will be shown in the output log.

3. Server function

The server process includes database connection, sql query, decision tree construction, result prediction and validation. DataBase connection will use pymysql to connect to given database by user, password and host. The source of decision tree construction will be queried by sql command. The tree algorithm is stored in tree.py. The final result will be sent to client side.

4. Using this system

1) Start python process server_main.py in server, with command:
    python server/server_main.py [-h] [-u USER] [-p PASSWORD] [-pt PORT] [-db DATABASE] [-ht HOST]
    please use python server/server_main.py -h for details. This process needs to be grant permission to create view in database in order to gain process speed. 

2) Start client interface in user terminal:
    python client/client_main.py

3) Select desired cleaning options for database cleaning. The process will take around X mins to finish.

4) Select desired source and target for data analysis. Please wait for 1-2 mins to finish as the decision tree needs to be built from scratch. The result of accurancy and F1 score will be shown in output log. 

5) Enter player's first name, last name and desired analysis type for data validation. Please wait for 1-2 mins to finish as the decision tree needs to be built from scratch. The result of decision tree prediction and acutal value will be shown in the output log. 