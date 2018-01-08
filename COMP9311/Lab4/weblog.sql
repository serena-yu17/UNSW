-- cp -f /mnt/c/OneDrive/UNSW/COMP9311/Lab3/weblog.sql /files

-- Q1: how many page accesses on March 2


create or replace view Q1(nacc) as
	 select count(acctime)
		AS nacc from accesses 
	 where extract(month from acctime) = 3 
		and extract(day from acctime) = 2;
;


-- Q2: how many times was the MessageBoard search facility used?
--insert into Accesses values (3618,75,0,'webgms/messageboard/view_messagetopic','state=search&gid=1596&color=#DDA0DD','2005-03-03 13:15:24',4416);

create or replace view Q2(nsearches) as
	select count(page) 
		as nsearches 
	from accesses 
		where page ~ '^messageboard' and params ~ 'state=search'
;


-- Q3: on which Tuba lab machines were there incomplete sessions?


create or replace view Q3(hostname) as
	select distinct hostname from Hosts where hostname ~* 'tuba' and id in (
		select host from Sessions where complete = false
	)
;


-- Q4: min,avg,max bytes transferred in page accesses

create or replace view Q4(min,avg,max) as
	select min(nbytes) as min, round(avg(nbytes)) as avg, max(nbytes) as max 
		from accesses
;


-- Q5: number of sessions from CSE hosts


create or replace view Q5(nhosts) as
	select count(Sessions.id) as nhosts 
	from Sessions join Hosts on Hosts.id = Sessions.host 
	where hostname ~* 'cse.unsw.edu.au$'
;


-- Q6: number of sessions from non-CSE hosts


create or replace view Q6(nhosts) as
	select count(Sessions.id) as nhosts 
	from Sessions join Hosts on Hosts.id = Sessions.host 
	where hostname !~* 'cse.unsw.edu.au$'
;


-- Q7: session id and number of accesses for the longest session?


create or replace view Q7(session,length) as 
	select session, seq as length
		from Accesses
		where seq in (select max(seq) from Accesses)
;


-- Q8: frequency of page accesses


create or replace view Q8(page,freq) as
	select page, count(page) as freq 
		from accesses group by page order by count(page) desc
;


-- Q9: frequency of module accesses


create or replace view Q9(module,freq) as
	select substring(page from '^([a-z]+)(/|$)') as module, count(page) as freq 
			from accesses
				group by substring(page from '^([a-z]+)(/|$)')
				order by count(substring(page from '^([a-z]+)(/|$)')) desc
;


-- Q10: "sessions" which have no page accesses


create or replace view Q10(session) as
	select id from Sessions
		where not exists (select session from accesses where session = Sessions.id)
;


