alter table Teams add index teamID_idx (teamID);

update HallOfFame inner join Master on HallOfFame.playerID = Master.bbrefID set HallOfFame.playerID = Master.playerID where HallOfFame.playerID not in (select playerID from Master);

update Salaries inner join Master on Salaries.playerID = Master.bbrefID set Salaries.playerID = Master.playerID where Salaries.playerID not in (select playerID from Master);

update Salaries inner join Teams on Salaries.teamID = Teams.teamIDBR set Salaries.teamID = Teams.teamID where Salaries.teamID not in (select teamID from Teams); 


update CollegePlaying 
set schoolID = 'caallan'
where schoolID = 'caallia';

update CollegePlaying 
set schoolID = 'cwpost'
where schoolID = 'ctpostu';

update CollegePlaying 
set schoolID = 'txtyler'
where schoolID = 'txutper';

update CollegePlaying 
set schoolID = 'txangel'
where schoolID = 'txrange';