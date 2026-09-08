CREATE TABLE People (PersonID int IDENTITY(1,1) Primary Key NOT NULL,
	TwitchPersonName varchar(max) NOT NULL,
	IsStreamer bit NOT NULL DEFAULT 0)

CREATE TABLE Command (CommandID int IDENTITY(1,1) Primary Key NOT NULL, 
	CommandName varchar(max) NOT NULL,
	CommandTypeID varchar(max),
	CommandDescription varchar(max),
	ProbabilityActivate int DEFAULT 100)

CREATE TABLE CommandPerson (CommandPersonID int IDENTITY(1,1) Primary Key NOT NULL,
	PersonID int NOT NULL,
	CommandID int NOT NULL)

CREATE TABLE CommandResponse (ResponseID int IDENTITY(1,1) Primary Key NOT NULL,
	ResponseText varchar(max),
	CommandID int NOT NULL,
	ReponseProbability int)

CREATE TABLE PersonCommandHistory (HistoryID int IDENTITY(1,1) Primary Key NOT NULL,
	PersonID int NOT NULL, 
	CommandID int NOT NULL, 
	ResponseID int NOT NULL,
	DateAchieved datetime DEFAULT GetDate())

CREATE TABLE CommandTrigger (CommandTriggerID int IDENTITY(1,1) Primary Key NOT NULL,
	CommandID int NOT NULL,
	TriggerText varchar(max))


--DROP TABLE PEOPLE
--DROP TABLE Command
--DROP TABLE CommandPerson
--DROP TABLE CommandResponse
--DROP TABLE PersonCommandHistory
--DROP TABLE CommandTrigger