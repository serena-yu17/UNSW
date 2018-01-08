ALTER TABLE beer
  DROP COLUMN totRating;
ALTER TABLE beer
  DROP COLUMN nRatings;
ALTER TABLE beer
  DROP COLUMN rating;
ALTER TABLE beer
  ADD COLUMN totRating INTEGER DEFAULT 0;
ALTER TABLE beer
  ADD COLUMN nRatings INTEGER DEFAULT 0;
ALTER TABLE beer
  ADD COLUMN rating FLOAT;


CREATE OR REPLACE FUNCTION func_upd()
  RETURNS TRIGGER AS $$
BEGIN
  IF (NEW.score != old.score AND new.beer = old.beer)
  THEN

    UPDATE beer
    SET totrating = totRating + NEW.score - old.score
    WHERE beer.id = new.beer;

    UPDATE beer
    SET rating = totrating / nRatings
    WHERE beer.id = new.beer;

  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS r_update
ON ratings;

CREATE TRIGGER r_update
AFTER UPDATE ON ratings
FOR EACH ROW
EXECUTE PROCEDURE func_upd();

--------------

CREATE OR REPLACE FUNCTION func_ins()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE beer
  SET totrating = totRating + NEW.score
  WHERE beer.id = new.beer;

  UPDATE beer
  SET nRatings = nRatings + 1
  WHERE beer.id = new.beer;

  UPDATE beer
  SET rating = totrating / nRatings
  WHERE beer.id = new.beer;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS r_insert
ON ratings;

CREATE TRIGGER r_insert
AFTER INSERT ON ratings
FOR EACH ROW
EXECUTE PROCEDURE func_ins();

-------------
CREATE OR REPLACE FUNCTION func_del()
  RETURNS TRIGGER AS $$
BEGIN
  UPDATE beer
  SET totrating = totRating - old.score
  WHERE beer.id = old.beer;

  UPDATE beer
  SET nRatings = nRatings - 1
  WHERE beer.id = old.beer;

  IF ((SELECT nratings
       FROM beer
       WHERE beer.id = old.beer) != 0)
  THEN
    UPDATE beer
    SET rating = totrating / nRatings
    WHERE beer.id = old.beer;
  ELSE
    UPDATE beer
    SET rating = NULL
    WHERE beer.id = old.beer;
  END IF;

  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS r_delete
ON ratings;

CREATE TRIGGER r_delete
AFTER DELETE ON ratings
FOR EACH ROW
EXECUTE PROCEDURE func_del();