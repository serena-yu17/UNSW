-- Address contains the registered address of the company (excluding the zip code and country
-- Zip is the zip code of the Address
-- Country is the incorporation country of the company (same as the country for the Address)
CREATE TABLE Company (
  Code char(3) primary key check (Code ~ '[A-Z]{3}'),
  Name text not null,
  Address text default null,
  Zip varchar(10) default null,
  Country varchar(40) default null
);

-- Person may contain person name, title and/or qualification
CREATE TABLE Executive (
  Code char(3) references Company(Code),
  Person text,
  primary key (Code, Person)
);

CREATE TABLE Category (
  Code char(3) primary key references Company(Code),
  Sector varchar(40) default null,
  Industry varchar(80) default null
);

CREATE TABLE ASX (
  "Date" date,
  Code char(3) references Company(Code),
  Volume integer not null check (Volume >= 0),
  Price numeric not null check (Price > 0.0),
  primary key ("Date", Code)
);

CREATE TABLE Rating (
  Code char(3) references Company(Code),
  Star integer default 3 check (Star > 0 and Star < 6)
);

CREATE TABLE ASXLog (
  "Timestamp" timestamp,
  "Date" date,
  Code char(3) references Company(Code),
  OldVolume integer not null check (OldVolume >= 0),
  OldPrice numeric not null check (OldPrice > 0.0),
  primary key ("Timestamp", "Date", Code)
);
