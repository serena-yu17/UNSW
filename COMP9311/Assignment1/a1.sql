-- COMP9311 17s2 Assignment 1
-- Schema for OzCars
--
-- Date: 
-- Student Name: Feng Yu
-- Student ID: 5173286
--

-- Some useful domains; you can define more if needed.

CREATE DOMAIN URLType as
	varchar(100) check (value like 'http://%');

CREATE DOMAIN EmailType as
	varchar(100) check (value like '%@%.%');

CREATE DOMAIN PhoneType as
	char(10) check (value ~ '[0-9]{10}');
	
CREATE DOMAIN CarLicenseType as
    varchar(6) check (value ~ '[0-9A-Za-z]{1,6}');

CREATE DOMAIN OptionType as varchar(12)
	check (value in ('sunroof','moonroof','GPS','alloy wheels','leather'));

CREATE DOMAIN VINType as char(17)
	check (VALUE ~ '^[0-9A-HJ-NPR-Z]{17}$');

CREATE DOMAIN MoneyType as NUMERIC(8, 2)
	check (VALUE > 0);

	
-- EMPLOYEE

CREATE TABLE Employee (
	EID SERIAL,
    TFN char(9) unique not null check(TFN ~ '^\d{9}$'),
	salary integer not null check(salary > 0),
	firstname varchar(50) not null,
	lastname varchar(50),
	PRIMARY KEY (EID)
);

CREATE TABLE Admin(
	EID INTEGER REFERENCES Employee(EID),	
	PRIMARY KEY(EID)	
);

CREATE TABLE Mechanic(
	EID INTEGER REFERENCES Employee(EID),	
	license char(8) unique not null check(license ~ '^[a-zA-Z0-9]{8}$'),
	PRIMARY KEY(EID)
);

CREATE TABLE Salesman(
	EID INTEGER REFERENCES Employee(EID),
	commRate INTEGER not null check(commRate >= 5 AND commRate <= 20),
	PRIMARY KEY(EID)
);

-- CLIENT

create table Client (
	CID SERIAL,
	name varchar(100) not null,
	phone PhoneType not null,
	email EMAILTYPE,
	address varchar(200) not null,	
	PRIMARY KEY(CID)
);

CREATE TABLE Company(
	CID INTEGER REFERENCES Client(CID),
	url URLType,
	ABN char(11) unique not null check(ABN ~'^[0-9]{11}$'),
	PRIMARY KEY(CID)
);

-- CAR

CREATE TABLE Car(
	VIN VINType,
	"year" INTEGER not null check("year" >= 1970 AND "year" <= 2099),
	model varchar(40) not null,
	manufacturer varchar(40) not null,
	PRIMARY KEY(VIN)
);

CREATE TABLE CarOptions(
	VIN VINType REFERENCES Car(VIN),
	option OptionType,
	PRIMARY KEY(VIN, option)
);

CREATE TABLE UsedCar(
	VIN VINType REFERENCES Car(VIN),
	plateNumber CarLicenseType not null,
	PRIMARY KEY(VIN)
);

CREATE TABLE NewCar(
	VIN VINType REFERENCES Car(VIN),
	cost MoneyType not null,
	charges MoneyType not null,	
	PRIMARY KEY(VIN)
);

-- Relationships

CREATE TABLE RepairJob(
	number INTEGER check(number >= 1 AND number <= 999),
	"date" DATE not null,
	description varchar(250) not null,
	parts MoneyType not null,
	"work" MoneyType not null,
	client INTEGER not null REFERENCES Client(CID),
	VIN VINType REFERENCES UsedCar(VIN),
	PRIMARY KEY(number, VIN)
);

CREATE TABLE Does(
	mechanic INTEGER REFERENCES Mechanic(EID),
	number INTEGER,
	VIN VINType,
	FOREIGN KEY(number, VIN) REFERENCES RepairJob(number, VIN),
	PRIMARY KEY(mechanic, number, VIN)
);

CREATE TABLE Buys(
	salesman INTEGER not null REFERENCES Salesman(EID),
	"date" DATE,
	price MoneyType not null,
	commission MoneyType not null,
	seller INTEGER REFERENCES Client(CID),
	VIN VINType REFERENCES UsedCar(VIN),
	PRIMARY KEY("date", seller, VIN)
);

CREATE TABLE Sells(
	salesman INTEGER not null REFERENCES Salesman(EID),
	"date" DATE,
	price MoneyType not null,
	commission MoneyType not null,
	buyer INTEGER REFERENCES Client(CID),
	VIN VINType REFERENCES UsedCar(VIN),
	PRIMARY KEY("date", buyer, VIN)
);

CREATE TABLE SellsNew(
	salesman INTEGER not null REFERENCES Salesman(EID),
	"date" DATE,
	plateNumber CarLicenseType not null,
	price MoneyType not null,
	commission MoneyType not null,
	client INTEGER REFERENCES Client(CID),
	VIN VINType REFERENCES NewCar(VIN),
	PRIMARY KEY("date", Client, VIN)
);






