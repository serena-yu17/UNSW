-- Q5 Find beers that are the only one by their brewer

-- How many beers does each brewer make?

select manf,count(name)
from beers
group by manf;

-- Restrict to groups of size 1 (i.e. makes just one beer)

select manf
from beers
group by manf
having count(name) = 1;

-- Soln: Select beers whose brewer is one of those who makes only one beer

select name
from Beers
where manf in (select manf
		from beers
		group by manf
		having count(name) = 1);


-- Q6 Find the beers sold at the bars where John drinks

-- AA: set of bars where John drinks

select bar from frequents where drinker='John';

-- Soln: Which beers are sold in a bar belonging to AA

select beer
from Sells
where bar in (select bar from frequents where drinker='John');

-- Alternative

-- Collect together info about beers sold in bars and drinkers who drink in them

select s.beer, s.bar, f.drinker
from Sells s join Frequents f on (f.bar = s.bar);

-- Filter entries that are for John (has duplicates)

select s.beer
from Sells s join Frequents f on (f.bar = s.bar)
where f.drinker = 'John';

-- Soln: eliminate duplicates

select distinct s.beer
from Sells s join Frequents f on (f.bar = s.bar)
where f.drinker = 'John';


-- Q7 How many different beers are there?

-- "different beers" means "distinct beers"
-- Since name is a primary key, no chance of duplicates

select count(name) from beers;

-- So this should give the same result as above

select count(distinct name) from beers;

-- Soln:

select count(name) from beers;


-- Q8 How many different brewers are there?

-- Since brewers may appear in several Beers tuples,
-- the two queries below have different results

select count(manf) from beers;
select count(distinct manf) from beers;

-- we're asked for "different brewers" = "distinct brewers"

-- Soln:

select count(distinct manf) from beers;


-- Q9 How many beers does each brewer make

-- we've already seen the basic query for this

select manf,count(name)
from   Beers
group by manf;

-- since it seems useful, let's turn it into a view

create view BrewersBeers(brewer,nbeers) as
select manf,count(name)
from   Beers
group by manf;

-- Soln:

select * from BrewersBeers;


-- Q10 Which brewer makes the most beers?

-- most number of beers by one brewer

select max(nbeers) from brewersbeers ;

-- Soln: get the brewer who makes this many beers

select brewer
from   BrewersBeers 
where  nbeers = (select max(nbeers) from BrewersBeers);


-- Q11 Bars where either Gernot or John drink

-- information for this query is in the Frequents table

select * from frequents;

-- we want tuples which have a drinker which is either Gernot or John

select bar from frequents where drinker='Gernot' or drinker='John';

-- or

select bar from frequents where drinker in ('Gernot','John');


-- Q12 Bars where both John and Gernot drink

-- same approach as above doesn't work ...
-- in a given tuple, the drinker cannot have two values

-- WRONG:
select bar from frequents where drinker='Gernot' and drinker='John';

-- could use set intersection
-- (set of Gernot's bars) and (set of John's bars)

-- Soln:

(select bar from frequents where drinker='Gernot')
intersect
(select bar from frequents where drinker='John');

-- Alternative: generate pairs of dinkers with a common bar

select d1.bar, d1.drinker, d2.drinker
from Frequents d1 join Frequents d2 on (d1.bar = d2.bar);

-- will generate (B,D1,D2) and (B,D2,D1) for all pairs
-- so we can take just one ordering and not miss anything

-- Soln:

select d1.bar, d1.drinker, d2.drinker
from Frequents d1 join Frequents d2 on (d1.bar = d2.bar)
where d1.drinker = 'Gernot' and d2.drinker = 'John';


-- Q11 reprised ... the set approach also works for OR

-- Soln: (set of Gernot's bars) union (set of John's bars)

(select bar from frequents where drinker='Gernot')
union
(select bar from frequents where drinker='John');

-- set operations remove duplicates
-- if we really want them, use "union all"

(select bar from frequents where drinker='Gernot')
union all
(select bar from frequents where drinker='John');


-- Q18 Which beers are sold at all bars?

-- Basic approach:
-- for each beer b {
--     BB = set of bars where b is sold
--     AB = set of all bars
--     if (AB == BB) then b is sold at all bars
-- }

-- "foreach beer b" is implemented as:

select name
from   Beers b
where  someConditionInvolvingB

-- Unfortunately, SQL does not have set equality
-- but it does have set difference and empty set check
-- so rephrase above test as
--
--     if (isEmpty(AB - BB)) then b is sold at all bars

-- Soln:

select name
from   Beers b
where  not exists (                                  -- isEmpty
	(select name from Bars)                      -- AB
	except                                       -- set diff
	(select bar from Sells where beer = b.name)  -- BB
	);

-- alternative approach
-- for each beer b {
--     NA = number of bars
--     NB = number of bars where b sold
--     if (NA == NB) then b is sold at all bars
-- }

-- Since NB is a single number, can be solved using group-by and count

-- Soln:

select beer,count(bar)
from   Sells
group  by beer
having count(bar) = (select count(*) from Bars);

-- Note: the above approach only works in some cases
-- The set-based approach works in all cases


-- Q22 How many bars in suburbs where dinkers live?
--     (must include all such suburbs, even if no bars)

-- A straight join doesn't work, because omits suburbs with no bar

select * from Drinkers d join Bars b on (d.addr = b.addr);

-- Outer join ensures that *all* dinker-suburbs appear

select * from Drinkers d left outer join Bars b on (d.addr = b.addr);

-- Once we've got drinker-suburbs associated with bars,
-- it's a straightforward group and count()
-- But count() is nice in giving zero for NULL cases

-- Soln:

select d.addr, count(b.name)
from   Drinkers d left outer join Bars b on (d.addr = b.addr)
group  by d.addr;

