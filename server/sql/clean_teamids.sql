
update Salaries
inner join Teams on Salaries.teamID = Teams.teamIDBR
set Salaries.teamID = Teams.teamID
where Salaries.teamID not in (select teamID from Teams);