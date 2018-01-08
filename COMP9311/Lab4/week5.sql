
-- Q1: how many page accesses on March 2?

create or replace view Q1(nacc) as
select count(*)
from   Accesses
where  accTime >= '2005-03-02 00:00:00' and accTime < '2005-03-03 00:00:00';

-- Q2: how many times was the MessageBoard search facility used?

create or replace view Q2(nsearches) as
select count(*)
from   Accesses
where  page like 'messageboard%' and params like '%state=search%';

-- Q3: on which Tuba lab machines were there incomplete sessions?

create or replace view Q3(hostname) as
select distinct h.hostname
from   Hosts h, Sessions s
where  h.hostname like 'tuba%cse.unsw.edu.au' and s.host=h.id
	and not s.complete
;

-- Q4: min,avg,max bytes transferred in page accesses

create or replace view Q4(min,avg,max) as
select min(nbytes),avg(nbytes)::integer,max(nbytes)
from   Accesses;

-- Q5: number of sessions from CSE hosts

create or replace view CSEHosts as
select *
from   Hosts
where  hostname like '%cse.unsw.edu.au';

create or replace view Q5(nhosts) as
select count(*)
from   Sessions s, CSEHosts c
where  s.host = c.id
;

-- Q6: number of sessions from non-CSE hosts

create or replace view nonCSEHosts as
select *
from   Hosts
where  hostname not like '%cse.unsw.edu.au';

create or replace view Q6(nhosts) as
select count(*)
from   Sessions s, nonCSEHosts c
where  s.host = c.id
;

-- Q7: session id and number of accesses for the longest session?

create or replace view sessLength as
select session,count(*) as length
from   Accesses
group by session;

create or replace view Q7(session,length) as 
select session,length
from   sessLength
where  length = (select max(length) from sessLength);

-- Q8: frequency of page accesses

create or replace view Q8(page,freq) as
select page,count(*)
from   Accesses
group by page
order by count(*) desc
;

-- Q9: frequency of module accesses

create or replace view ModuleAccess as
select session, seq, substring(page from '^[^/]+') as module
from   Accesses;

create or replace view Q9(module,freq) as
select module,count(*)
from   ModuleAccess
group by module
order by count(*) desc
;

-- Q10: "sessions" which have no page accesses

create or replace view Q10(session) as
select id
from   Sessions s
where  not exists (select * from Accesses where session=s.id);
