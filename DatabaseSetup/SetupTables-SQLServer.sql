CREATE TABLE People (PersonID int IDENTITY(1,1) Primary Key NOT NULL,
	TwitchPersonName varchar(max) NOT NULL,
	IsStreamer bit NOT NULL DEFAULT 0)

CREATE TABLE Command (CommandID int IDENTITY(1,1) Primary Key NOT NULL, 
	CommandName varchar(max) NOT NULL,
	CommandTypeID varchar(max))

CREATE TABLE CommandPerson (CommandPersonID int IDENTITY(1,1) Primary Key NOT NULL,
	PersonID int NOT NULL,
	CommandID int NOT NULL)

CREATE TABLE CommandResponse (ResponseID int IDENTITY(1,1) Primary Key NOT NULL,
	ResponseText varchar(max),
	CommandID int NOT NULL,
	ReponseProbability int)

CREATE TABLE PersonCommandHistory(HistoryID int IDENTITY(1,1) Primary Key NOT NULL,
	PersonID int NOT NULL, 
	CommandID int NOT NULL, 
	ResponseID int NOT NULL,
	DateAchieved datetime DEFAULT GetDate())