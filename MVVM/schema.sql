CREATE TABLE area (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE client (
	id INTEGER NOT NULL, 
	name VARCHAR(80), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE feature_request (
	id INTEGER NOT NULL, 
	title VARCHAR(80), 
	description TEXT, 
	priority INTEGER, 
	due DATETIME, 
	client INTEGER, 
	product_area INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (title), 
	FOREIGN KEY(client) REFERENCES client (id), 
	FOREIGN KEY(product_area) REFERENCES area (id)
);
