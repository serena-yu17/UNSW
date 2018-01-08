-- COMP9311 17s2 Assignment 1 (Stage 2) - Sample Solution
-- 				Schema for OzCars


-- Some useful domains; you can define more if needed.

create domain URLType as
 varchar(100) check (value like 'http://%');

create domain EmailType as
 varchar(100) check (value like '%@%.%');

create domain PhoneType as
 char(10) check (value ~ '[0-9]{10}');

create domain CarLicenseType as
        varchar(6) check (value ~ '[0-9A-Za-z]{1,6}'); 

create domain OptionType as varchar(12)
 check (value in ('sunroof','moonroof','GPS','alloy wheels','leather'));

create domain VINType as char(17) 
         check (value ~ '[0-9A-HJ-NPR-Z]{17}');


-- Employee
create table Employee (
  EID          serial primary key, 
  firstname    varchar(50) not null,
  lastname     varchar(50) not null,
  salary       integer not null check (salary > 0),
  TFN          char(9) check (TFN ~ '[0-9]{9}') not null unique
);


-- Admin
create table Admin(
  EID integer references Employee(EID),
  primary key (EID)
);


-- Mechanic
create table Mechanic(
  EID      integer references Employee(EID),
  license  char(8) check (license ~ ' [0-9A-Za-z]{8}') not null,
  primary key (EID)
);


-- Salesman
create table Salesman(
  EID       integer references Employee(EID),
  commRate  integer check (commRate >= 5 and commRate <= 20) not null,
  primary key (EID)
);


-- Client
create table Client (
  CID      serial primary key,
  phone    PhoneType not null,
  address  varchar(200) not null,
  name     varchar(100) not null,
  email    EmailType
);


-- Company
create table Company(
  CID     integer references Client(CID),
  ABN     char(11) check (ABN ~ '[0-9]{11}') not null unique,
  url     URLType,
  primary key(CID)
);


--Car
create table Car(
  VIN  VINType primary key,
  year  integer check (year>=1970 and year <= 2099 ) not null,
  model  varchar(40) not null,
  manufacturer  varchar(40) not null
);


-- Car Options (multi-valued)
create table CarOptions (
  VIN     VINType,
  options OptionType not null, -- if null, you don't need an entry in this table.
				-- Also since options is part of the composite primary key for this table no need to put not null constraint.
  primary key (VIN,options),
  foreign key (VIN) references Car(VIN)
);


-- Newcar
create table NewCar(
  VIN VINType references Car(VIN),
  cost numeric(8,2) not null,
  charges numeric(8,2)  not null,
  primary key(VIN)
);


--UsedCar
create table UsedCar(
  VIN VINType references Car(VIN),
  plateNumber CarLicenseType not null,
  primary key(VIN)
);


--RepairJob
create table RepairJob(
  VIN  VINType,
  number  integer check (number >=1 and number <=999),
  description varchar(250),
  parts numeric(8,2) not null,
  work  numeric(8,2) not null,
  "date" date not null,
  CID integer not null,
  primary key(VIN, number),
  foreign key(VIN) references UsedCar(VIN),
  foreign key(CID) references Client(CID)
);


-- Does
create table Does (
  VIN             VINType,
  number          integer check (number >=1 and number <= 999),
  EID             integer,
  primary key (VIN, number, EID),
  foreign key (VIN, number) references RepairJob (VIN, number),
  foreign key (EID) references Mechanic (EID) 
);


-- Buys
create table Buys (
  EID    integer references Salesman(EID) not null,
  CID     integer references Client(CID),
  VIN    VINType references UsedCar(VIN),
  price numeric(8,2) check (price > 0.0) not null,
  "date"  date,
  commission numeric(8,2) check (commission > 0.0) not null,
  primary key (CID, VIN, "date")
);


-- Sells
create table Sells(
  EID    integer references Salesman(EID) not null,
  CID     integer references Client(CID),
  VIN    VINType references UsedCar(VIN),
  price numeric(8,2) check (price > 0.0) not null,
  "date"  date,
  commission numeric(8,2) check (commission > 0.0) not null,
  primary key (CID, VIN, "date")
);


-- SellsNew

create table SellsNew(
  EID    integer references Salesman(EID) not null,
  CID    integer references Client(CID),
  VIN    VINType references NewCar(VIN),
  price numeric(8,2) check (price > 0.0) not null,
  "date"  date,
  commission numeric(8,2) check (commission > 0.0) not null,
  plateNumber    CarLicenseType not null,
  primary key (CID, VIN, "date")
);
