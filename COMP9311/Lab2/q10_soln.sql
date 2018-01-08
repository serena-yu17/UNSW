--For Q10 
create table Employees (
	tfn         char(11)
	            constraint ValidTFN
				check (tfn ~ '[0-9]{3}-[0-9]{3}-[0-9]{3}'),
	givenName   varchar(30) not null,  -- must have a given name
	familyName  varchar(30),           -- some people have only one name
	hoursPweek  float
				check (hoursPweek >= 0 and hoursPweek <= 168), --7*24 
	primary key (tfn)
);

create table Departments (
	id          char(3)                          -- [[:digit:]] == [0-9]
	            constraint ValidDeptId check (id ~ '[[:digit:]]{3}'),
	name        varchar(100) unique,
	manager     char(11) not null unique
	            constraint ValidEmployee references Employees(tfn) DEFERRABLE,
	primary key (id)
);

alter table Employees
	add column worksIn char(3) not null
		constraint ValidDepartment references Departments(id) DEFERRABLE;


create table DeptMissions (
	department  char(3)
	            constraint ValidDepartment references Departments(id),
	keyword     varchar(20),
	primary key (department,keyword)
);


--insertion example for Q10 

begin;

set constraints all deferred;

insert into employees values ('111-111-111','YANG','YANG',40.0,'100');
insert into departments values ('100','Administration','111-111-111'); 

set constraints all immediate;

commit;