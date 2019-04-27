alter table Master add primary key (playerID);
alter table Batting add primary key (playerID, yearID, stint, teamID, lgID);
alter table Pitching add primary key (playerID, yearID, stint, teamID, lgID);
alter table Fielding add primary key (playerID, yearID, stint, teamID, lgID, Pos);
alter table AllstarFull add primary key (playerID, yearID, lgID, gameID);
alter table HallOfFame add primary key (playerID, yearID, votedBy);
alter table Managers add primary key (playerID, yearID, teamID, lgID, inseason);
alter table Teams add primary key (yearID, teamID, lgID);
alter table BattingPost add primary key (playerID, yearID, teamID, lgID, round);
alter table PitchingPost add primary key (playerID, yearID, teamID, lgID, round);
alter table TeamsFranchises add primary key (franchID);
alter table FieldingOF add primary key (playerID, yearID, stint);
alter table ManagersHalf add primary key (playerID, yearID, teamID, lgID, half);
alter table TeamsHalf add primary key (yearID, teamID, lgID, half);
alter table Salaries add primary key (playerID, yearID, teamID, lgID);
alter table SeriesPost add primary key (yearID, round);
alter table AwardsManagers add primary key (playerID, awardID, yearID, lgID);
alter table AwardsPlayers add primary key (playerID, yearID, awardID, lgID);
alter table AwardsShareManagers add primary key (playerID, yearID, awardID, lgID);
alter table AwardsSharePlayers add primary key (playerID, yearID, awardID, lgID);
alter table FieldingPost add primary key (playerID, yearID, lgID, round, Pos);
alter table Appearances add primary key (playerID, yearID, teamID, lgID);
alter table Schools add primary key (schoolID);
alter table CollegePlaying add primary key (playerID, schoolID, yearID);
alter table FieldingOFsplit add primary key (playerID, yearID, lgID, stint, Pos);
alter table Parks add primary key (`park.key`);
alter table HomeGames add primary key (`park.key`, `team.key`, `year.key`, `league.key`);

-- alter table Teams add index teamID_idx (teamID);






alter table Batting 
add foreign key (playerID) references Master (playerID);
alter table Batting 
add foreign key (teamID) references Teams (teamID);
alter table Pitching
add foreign key (playerID) references Master (playerID);
alter table Pitching
add foreign key (teamID) references Teams (teamID);
alter table Fielding
add foreign key (playerID) references Master (playerID);
alter table Fielding
add foreign key (teamID) references Teams (teamID);
alter table AllstarFull
add foreign key (playerID) references Master (playerID);
alter table AllstarFull
add foreign key (teamID) references Teams (teamID);
alter table HallOfFame
add foreign key (playerID) references Master (playerID);
alter table Managers
add foreign key (playerID) references Master (playerID);
alter table Managers
add foreign key (teamID) references Teams (teamID);
alter table Teams
add foreign key (franchID) references TeamsFranchises (franchID);
alter table BattingPost
add foreign key (playerID) references Master (playerID);
alter table BattingPost
add foreign key (teamID) references Teams (teamID);
alter table PitchingPost
add foreign key (playerID) references Master (playerID);
alter table PitchingPost
add foreign key (teamID) references Teams (teamID);
alter table FieldingOF
add foreign key (playerID) references Master (playerID);
alter table ManagersHalf
add foreign key (playerID) references Master (playerID);
alter table ManagersHalf
add foreign key (teamID) references Teams (teamID);
alter table Salaries
add foreign key (playerID) references Master (playerID);
alter table Salaries
add foreign key (teamID) references Teams (teamID);
alter table SeriesPost
add foreign key (teamIDWinner) references Teams (teamID);
alter table SeriesPost
add foreign key (teamIDLoser) references Teams (teamID);
alter table AwardsManagers
add foreign key (playerID) references Master (playerID);
alter table AwardsPlayers
add foreign key (playerID) references Master (playerID);
alter table AwardsShareManagers
add foreign key (playerID) references Master (playerID);
alter table AwardsSharePlayers
add foreign key (playerID) references Master (playerID);
alter table FieldingPost
add foreign key (playerID) references Master (playerID);
alter table FieldingPost
add foreign key (teamID) references Teams (teamID);
alter table Appearances
add foreign key (playerID) references Master (playerID);
alter table Appearances
add foreign key (teamID) references Teams (teamID);
alter table CollegePlaying
add foreign key (playerID) references Master (playerID);
alter table CollegePlaying
add foreign key (schoolID) references Schools (schoolID);
alter table FieldingOFsplit
add foreign key (playerID) references Master (playerID);
alter table FieldingOFsplit
add foreign key (teamID) references Teams (teamID);
alter table HomeGames
add foreign key (`park.key`) references Parks (`park.key`);
alter table HomeGames
add foreign key (`team.key`) references Teams (`teamID`);