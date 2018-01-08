CREATE TABLE Employee(
	EID SERIAL;
    TFN char(9) unique not null check(TFN ~ '^\d{9}$');
	salary integer not null check(salary > 0);
	firstname varchar(50) not null;
	lastname varchar(50) not null;
	PRIMARY KEY (EID);
);

CREATE TABLE Administrator(
	EID SERIAL REFERENCES Employee(EID);	
	PRIMARY KEY(EID);	
);

CREATE TABLE Mechanic(
	EID SERIAL REFERENCES Employee(EID);	
	license char(8) unique not null check(license ~ '^\w{8}$');
	"number" INTEGER REFERENCES RepairJob("number");
	PRIMARY KEY(EID);	
);

CREATE TABLE RepairJob(
	"number" INTEGER unique check("number" >= 1 AND "number" <= 999);
	"date" DATE not null;
	description varchar(250) not null;
	parts NUMERIC(6, 2) not null check(parts >= 0);
	"work" NUMERIC(6, 2) not null check("work" >= 0);
	CID SERIAL REFERENCES Client(CID);
	VIN char(17) REFERENCES UsedCar(VIN);
	PRIMARY KEY("number");
);

CREATE TABLE Salesman(
	EID SERIAL REFERENCES Employee(EID);
	commRate INTEGER not null check(commRate >= 5 AND commRate <= 20);
	PRIMARY KEY(EID);
);


CREATE TABLE Client(
	CID SERIAL check(CID >= 0);
	name varchar(100);
	phone char(10) check(phone ~ '^\d{10}$');
	email EMAILTYPE;
	address varchar(200);
	ABN char(11) check(ABN ~'^\d{11}$');
	url URLType;
	CONSTRAINTS isCompany check(
		(ABN is null AND name is not null AND phone is not null AND address is not null)
	OR (ABN is not null)
	);
	PRIMARY KEY(CID);
);

CREATE DOMAIN EMAILTYPE AS 
	TEXT check(
	VALUE ~ '^[a-zA-Z0-9_\-]+[a-zA-Z0-9_\-.]*[a-zA-Z0-9_\-]+@([a-zA-Z0-9.][a-zA-Z0-9-.]+)*.[a-zA-Z0-9]+[a-zA-Z0-9-.]*([a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*)+$');

CREATE DOMAIN URLType AS
	varchar(100) check (value like 'http://%');

CREATE TABLE Car(
	VIN char(17) check(VIN ~ '^(?![IOQ])\w{17}$');
	"year" INTEGER not null check("year" >= 1970 AND "year" <= 2099);
	model varchar(40) not null;
	manufacturer varchar(40) not null;
	PRIMARY KEY(VIN);
);

CREATE TABLE Options(
	sun-roof OptionTYPE;
	built-inGPS	OptionType;
);

CREATE DOMAIN OptionTYPE AS TEXT(
	CONSTRAINTS isOption check(
		VALUE = "sun-roof" OR VALUE = "built-inGPS"
	);
);

CREATE TABLE UsedCar(
	VIN char(17) REFERENCES Car(VIN);
	plateNumber varchar(6) not null check(plateNumber ~ '^\w{6}$');
	-- Buys
	EID SERIAL REFERENCES Salesman(EID);
	seller	SERIAL	REFERENCES Client(CID);
	price NUMERIC(6, 2);
	"data"	DATE;
	commission NUMERIC(6, 2) check(commission >= 0);
	CONSTRAINTS isBuy check(
		
	);
	--End Buys	
	PRIMARY KEY(VIN);
);

CREATE TABLE NewCar(
	VIN char(17) REFERENCES Car(VIN);
	cost INTEGER not null check(cost >= 0);
	charges INTEGER not null check(charges >= 0);	
	PRIMARY KEY(VIN);
);












