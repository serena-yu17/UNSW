-- COMP9311 17s2 Lab5 Exercise
-- Written by: YOUR NAME


-- AllRatings view 

CREATE OR REPLACE VIEW AllRatings(taster, beer, brewer, rating)  AS
  SELECT
    Taster.given  AS taster,
    beer.name     AS beer,
    brewer.name as brewer,
    Ratings.score AS rating
  FROM Taster, Ratings, beer, brewer
  WHERE Ratings.beer = beer.id AND Taster.id = Ratings.taster and brewer.id=beer.brewer
  ORDER BY taster, beer;

-- John's favourite beer

CREATE OR REPLACE VIEW JohnsFavouriteBeer(brewer, beer)  AS
  SELECT
    brewer.name AS brewer,
    beer.name   AS beer
  FROM brewer, beer
  WHERE brewer.id = beer.brewer AND beer.id = (
    SELECT beer
    FROM ratings, taster
    WHERE taster.id = ratings.taster AND taster.given = 'John' AND ratings.score = (
      SELECT max(score)
      FROM ratings, taster
      WHERE taster.id = ratings.taster AND taster.given = 'John'
    )
  );

-- X's favourite beer
DROP TYPE IF EXISTS BEERINFO CASCADE;
CREATE TYPE BEERINFO AS (brewer TEXT, beer TEXT);

CREATE OR REPLACE FUNCTION FavouriteBeer(taster TEXT)
  RETURNS SETOF BEERINFO AS
$$
SELECT
  brewer.name AS brewer,
  beer.name   AS beer
FROM brewer, beer
WHERE brewer.id = beer.brewer AND beer.id = (
  SELECT beer
  FROM ratings, taster
  WHERE taster.id = ratings.taster AND taster.given = $1 AND ratings.score = (
    SELECT max(score)
    FROM ratings, taster
    WHERE taster.id = ratings.taster AND taster.given = $1
  )
);
$$ LANGUAGE SQL;

-- Beer style

CREATE OR REPLACE FUNCTION BeerStyle(brewer TEXT, beer TEXT)
  RETURNS TEXT
AS $$
SELECT beerstyle.name
FROM beerstyle, beer, brewer
WHERE beerstyle.id = beer.style AND beer.brewer = brewer.id AND lower(beer.name) = lower($2) AND
      lower(brewer.name) = lower($1);
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION BeerStyle1(_brewer TEXT, _beer TEXT)
  RETURNS TEXT
AS $$
DECLARE beer_name TEXT;
BEGIN
  SELECT beerstyle.name
  INTO beer_name
  FROM beerstyle, beer, brewer
  WHERE beerstyle.id = beer.style AND beer.brewer = brewer.id AND lower(beer.name) = lower(_beer) AND
        lower(brewer.name) = lower(_brewer);
  RETURN beer_name;
END;
$$ LANGUAGE plpgsql;

-- Taster address

CREATE OR REPLACE FUNCTION TasterAddress(taster TEXT)
  RETURNS TEXT
AS $$
SELECT CASE WHEN (loc.state IS NOT NULL AND loc.country IS NOT NULL)
  THEN loc.state || ', ' || loc.country
       ELSE
         coalesce(loc.state, loc.country)
       END
FROM Taster t, LOCATION loc
WHERE t.given = $1 AND t.livesIn = loc.id;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION TasterAddress(taster TEXT)
  RETURNS TEXT
AS $$
DECLARE add_state   TEXT;
        add_country TEXT;
BEGIN
  SELECT
    loc.state,
    loc.country
  INTO add_state, add_country
  FROM Taster t, LOCATION loc
  WHERE t.given = $1 AND t.livesIn = loc.id;
  IF (add_state IS NOT NULL AND add_country IS NOT NULL)
  THEN
    RETURN add_state || ', ' || add_country;
  ELSEIF (add_state IS NOT NULL)
    THEN
      RETURN add_state;
  ELSE
    RETURN add_country;
  END IF;
END;
$$ LANGUAGE plpgsql;

-- BeerSummary function

CREATE OR REPLACE FUNCTION BeerSummary()
  RETURNS TEXT
AS $$
DECLARE
  tex             TEXT;
  beer_name       TEXT;
  rating_score    TEXT;
  concated_taster TEXT;
  temptext        TEXT;
  cur_text        TEXT;
BEGIN
  FOR beer_name IN SELECT DISTINCT name
                   FROM beer
                   ORDER BY name LOOP
    --average rating
    SELECT cast(round(avg(score), 1) AS TEXT)
    INTO rating_score
    FROM ratings, beer
    WHERE ratings.beer = beer.id AND beer.name = beer_name;
    --concatenate tasters' names
    FOR temptext IN SELECT taster.given
                    FROM taster, ratings, beer
                    WHERE taster.id = ratings.taster AND beer.id = ratings.beer AND beer.name = beer_name LOOP
      IF (concated_taster IS NULL)
      THEN
        concated_taster := temptext;
      ELSE
        IF (temptext IS NOT NULL)
        THEN
          concated_taster := concated_taster || ', ' || temptext;
        END IF;
      END IF;
    END LOOP;
    --concatenate into output text
    cur_text:= 'beer:' || E'\t' || beer_name || E'\n' || 'Rating:' || E'\t' || rating_score || E'\n' || 'Tasters:' ||
               concated_taster || E'\n\n';
    IF (tex IS NULL)
    THEN
      tex:=cur_text;
    ELSE
      IF (cur_text IS NOT NULL)
      THEN
        tex:=
        tex || 'beer:' || E'\t' || beer_name || E'\n' || 'Rating:' || E'\t' || rating_score || E'\n' || 'Tasters:'
        || concated_taster || E'\n\n';
      END IF;
    END IF;
    concated_taster := NULL;
  END LOOP;
  RETURN tex;
END;
$$ LANGUAGE plpgsql;

-- Concat aggregate
CREATE OR REPLACE FUNCTION agg_concat(TEXT, TEXT)
  RETURNS TEXT AS $$
SELECT CASE WHEN ($2 IS NOT NULL)
  THEN
    (SELECT CASE WHEN ($1 != '')
      THEN
        $1 || ',' || $2
            ELSE
              $2
            END)
       ELSE
         $1
       END;
$$ LANGUAGE SQL;

DROP AGGREGATE IF EXISTS concat( TEXT ) CASCADE;
CREATE AGGREGATE concat ( TEXT )
(
STYPE = TEXT,
INITCOND = '',
SFUNC = agg_concat
);

-- BeerSummary view

CREATE OR REPLACE VIEW BeerSummary(beer, rating, tasters)  AS
  SELECT
    beer,
    round(avg(rating), 2) AS rating,
    concat(taster)        AS taster
  FROM AllRatings
  GROUP BY beer;

-- TastersByCountry view

CREATE OR REPLACE VIEW TastersByCountry(country, tasters)
  AS
    SELECT
      location.country,
      concat(taster.given) AS taster
    FROM location, taster
    WHERE location.id = taster.livesin
    GROUP BY location.country;
