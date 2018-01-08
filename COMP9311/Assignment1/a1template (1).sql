-- COMP9311 17s2 Assignment 1
-- Schema for OzCars
--
-- Date: 
-- Student Name: 
-- Student ID: 
--

-- Some useful domains; you can define more if needed.

create domain URLType as
	varchar(100) check (value like 'http://%');

create domain EmailType as
	varchar(100) check (value like '%@%.%');

create domain PhoneType as
	char(10) check (value ~ '[0-9]{10}');


-- EMPLOYEE

create table Employee (
	EID          serial, 
    ...
    salary       integer not null check (salary > 0),
	...
	primary key (EID)
);


-- CLIENT

create table Client (
	CID          serial,
	...
	primary key (CID)
);



-- CAR

create domain CarLicenseType as
        varchar(6) check (value ~ '[0-9A-Za-z]{1,6}');

create domain OptionType as varchar(12)
	check (value in ('sunroof','moonroof','GPS','alloy wheels','leather'));

create domain VINType as char(17) check ...
