INSERT INTO People  
	(TwitchPersonName, IsStreamer) 
VALUES 
	('Bubbler', 0),
	('Cubbler', 1),
	('Dubbler', 0),
	('Eubbler', 0),
	('Fubbler', 1),
	('Gubbler', 0),
	('Hubbler', 0)

INSERT INTO Command
	(CommandName, CommandTypeID, CommandDescription, ProbabilityActivate)
VALUES
	('HiDad', 'Listener', 'This command has a chance to say "Hi, I''m dad" to a user if they trigger it', 2),
	('Escape', 'Interact', 'Try to escape the prison through 12 gates, if you can', 2),
	('DeezNuts', 'Listener', 'Make sure that we got em', 2),
	('BusterVoice', 'Interact', 'How much do you love buster''s voice', 2)

INSERT INTO CommandPerson 
	(PersonID, CommandID)
VALUES
	(5, 1),
	(5, 4),
	(2, 1),
	(2, 2),
	(2, 3),
	(2, 4)


INSERT INTO CommandResponse 
	(ResponseText, CommandID, ReponseProbability)
VALUES
	(' loves buster''s voice %', 4, 100),
	(' got through gate 8 but did something that means end', 2, 10),
	(' got through all 12 gates. Hell yeah.', 2, 1),
	(' couldn''t even get through the first gate. What a chump.', 2, 50),
	(' isn''t even trying to escape. Shame on them.', 2, 39),
	(' deez nuts', 3, 100),
	('Hi ___ I''m dad', 1, 100)

INSERT INTO CommandTrigger 
	(TriggerText, CommandID)
VALUES
	('I''m', 1),
	('Im', 1),
	('im', 1),
	('!escape', 2),
	('!bustersVoice', 1)

INSERT INTO PersonCommandHistory
	(PersonID, CommandID, ResponseID)
VALUES
	(1, 2, 5),
	(1, 1, 7),
	(4, 3, 6),
	(6, 2, 3)


SELECT * FROM People
SELECT * FROM Command
SELECT * FROM CommandResponse
SELECT * FROM CommandPerson
SELECT * FROM CommandTrigger
SELECT * FROM PersonCommandHistory
