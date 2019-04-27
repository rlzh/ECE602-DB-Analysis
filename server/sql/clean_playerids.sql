update HallOfFame
inner join Master on HallOfFame.playerID = Master.bbrefID
set HallOfFame.playerID = Master.playerID
where HallOfFame.playerID not in (select playerID from Master);

update Salaries
inner join Master on Salaries.playerID = Master.bbrefID
set Salaries.playerID = Master.playerID
where Salaries.playerID not in (select playerID from Master);