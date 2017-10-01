CREATE TABLE area (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE "feature_request" (
	`id`	INTEGER NOT NULL,
	`title`	VARCHAR ( 80 ) UNIQUE,
	`description`	TEXT,
	`priority`	INTEGER,
	`due`	DATETIME,
	`client`	INTEGER,
	`product_area`	INTEGER,
	`submit_date`	date,
	FOREIGN KEY(`client`) REFERENCES `client`(`id`),
	FOREIGN KEY(`product_area`) REFERENCES `area`(`id`),
	PRIMARY KEY(`id`)
);
CREATE TABLE "client" (
	`id`	INTEGER NOT NULL,
	`name`	VARCHAR ( 80 ) UNIQUE,
	`description`	TEXT DEFAULT "",
	`avatar`	BLOB,
	`joined`	TEXT,
	`homepage`	TEXT,
	`email`	TEXT,
	PRIMARY KEY(`id`)
);
