CREATE TABLE People (PersonID int Primary Key NOT NULL AUTO_INCREMENT,
	TwitchPersonName varchar(255) NOT NULL,
	IsStreamer bit NOT NULL DEFAULT 0);

CREATE TABLE Command (CommandID int Primary Key NOT NULL AUTO_INCREMENT, 
	CommandName varchar(255) NOT NULL,
	CommandTypeID varchar(255),
	CommandDescription varchar(255),
	ProbabilityActivate int DEFAULT 100);

CREATE TABLE CommandPerson (CommandPersonID int Primary Key NOT NULL AUTO_INCREMENT,
	PersonID int NOT NULL,
	CommandID int NOT NULL);

CREATE TABLE CommandResponse (ResponseID int Primary Key NOT NULL AUTO_INCREMENT,
	ResponseText varchar(255),
	CommandID int NOT NULL,
	ResponseProbability int);

CREATE TABLE PersonCommandHistory (HistoryID int Primary Key NOT NULL AUTO_INCREMENT,
	PersonID int NOT NULL, 
	CommandID int NOT NULL, 
	ResponseID int NOT NULL,
	DateAchieved datetime DEFAULT Now());

CREATE TABLE CommandTrigger (CommandTriggerID int Primary Key NOT NULL AUTO_INCREMENT,
	CommandID int NOT NULL,
	TriggerText varchar(255));


--DROP TABLE PEOPLE
--DROP TABLE Command
--DROP TABLE CommandPerson
--DROP TABLE CommandResponse
--DROP TABLE PersonCommandHistory
--DROP TABLE CommandTrigger