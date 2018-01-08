-- COMP9311 Lab6 Exercise - Sample Solution

create or replace function
	insertRating() returns trigger
as $$
declare
	b Beer;
begin
	select * into b from Beer where id = new.beer;
	b.nratings := b.nratings + 1;
	b.totrating := b.totrating + new.score;
	b.rating = b.totrating / b.nratings;
	update Beer
	set    nratings = b.nratings,
	       totrating = b.totrating,
	       rating = b.rating
	where  id = new.beer;
	return new;
end;
$$ language plpgsql;

create or replace function
	updateRating() returns trigger
as $$
declare
	nb Beer; ob Beer;
begin
	select * into nb from Beer where id = new.beer;
	if (new.beer = old.beer) then
		if (new.rating = old.rating) then
			null;  -- updated the Rater?
		else
			-- this is the only required update
			nb.totrating := nb.totrating + new.score - old.score;
			nb.rating = nb.totrating / nb.nratings;
		end if;
	else --(new.beer <> old.beer)
		select * into ob from Beer where id = old.beer;
		ob.totrating := ob.totrating - old.score;
		ob.nratings := ob.nratings - 1;
		ob.rating := ob.totrating / ob.nratings;
		nb.totrating := nb.totrating + new.score;
		nb.nratings := nb.nratings + 1;
		nb.rating := nb.totrating / nb.nratings;
		update Beer
		set    nratings = ob.nratings,
		       totrating = ob.totrating,
		       rating = ob.rating
		where  id = old.beer;
	end if;
	update Beer
	set    nratings = nb.nratings,
	       totrating = nb.totrating,
	       rating = nb.rating
	where  id = new.beer;
	return new;
end;
$$ language plpgsql;

create or replace function
	deleteRating() returns trigger
as $$
declare
	b Beer;
begin
	select * into b from Beer where id = old.beer;
	b.nratings := b.nratings - 1;
	b.totrating := b.totrating - old.score;
	if (b.nratings = 0) then
		b.rating := null;
	else
		b.rating = b.totrating/b.nratings;
	end if;
	update Beer
	set    nratings = b.nratings,
	       totrating = b.totrating,
	       rating = b.rating
	where  id = old.beer;
	return old;
end;
$$ language plpgsql;

create trigger InsertRating
after insert on Ratings
for each row execute procedure insertRating();

create trigger UpdateRating
after update on Ratings
for each row  execute procedure updateRating();

create trigger DeleteRating
before delete on Ratings
for each row execute procedure deleteRating();
