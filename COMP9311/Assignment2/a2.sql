--List all the company names and countries that are incorporated outside Australia.
CREATE OR REPLACE VIEW Q1(Name, Country) AS
  SELECT
    Name,
    Country
  FROM Company
  WHERE Country != 'Australia'       --company not in Australia
  ORDER BY Name;

--List all the company codes that have more than five executive members on record (i.e., at least six).
CREATE OR REPLACE VIEW Q2(Code) AS
  SELECT Code
  FROM Executive
  GROUP BY Code
  HAVING COUNT(Code) > 5         --count executive members
  ORDER BY Code;

--List all the company names that are in the sector of "Technology"
CREATE OR REPLACE VIEW Q3(Name) AS
  SELECT DISTINCT Name
  FROM Company, Category
  WHERE Company.Code = Category.Code AND Category.Sector = 'Technology'   --sector of "Technology"
  ORDER BY Name;

--Find the number of Industries in each Sector
CREATE OR REPLACE VIEW Q4(Sector, Number) AS
  SELECT
    Sector,
    COUNT(DISTINCT Industry) AS "Number"
  FROM Category
  GROUP BY Sector                            -- count in each sector
  ORDER BY Sector;

--Find all the executives (i.e., their names) that are affiliated with companies in the sector of "Technology". If an executive is affiliated with more than one company, he/she is counted if one of these companies is in the sector of "Technology".
CREATE OR REPLACE VIEW Q5(Name) AS
  SELECT DISTINCT Person AS "Name"
  FROM Executive
    INNER JOIN Category ON (Executive.Code = Category.Code)
  WHERE Category.Sector = 'Technology'            --obtain sector information from Table Category
  ORDER BY "Name";

--List all the company names in the sector of "Services" that are located in Australia with the first digit of their zip code being 2.
CREATE OR REPLACE VIEW Q6(Name) AS
  SELECT DISTINCT Name
  FROM Company
    INNER JOIN Category ON (Company.Code = Category.Code)
  WHERE Category.Sector = 'Services'               -- sector
        AND Company.Country = 'Australia'          -- location
        AND Company.Zip ~ '^2'                     -- regex to check zip code start with 2
  ORDER BY Name;

--Create a database view of the ASX table that contains previous Price, Price change (in amount, can be negative) and Price gain (in percentage, can be negative). (Note that the first trading day should be excluded in your result.) For example, if the PrevPrice is 1.00, Price is 0.85; then Change is -0.15 and Gain is -15.00 (in percentage but you do not need to print out the percentage sign).
CREATE OR REPLACE VIEW Q7("Date", Code, Volume, PrevPrice, Price, Change, Gain) AS
  SELECT
    Asx_late."Date"                                            AS "Date",
    Asx_late.Code,
    Asx_late.Volume,
    Asx_early.Price                                            AS PrevPrice,
    Asx_late.Price,
    Asx_late.Price - Asx_early.Price                           AS Change,
    (Asx_late.Price - Asx_early.Price) / Asx_early.Price * 100 AS Gain
  FROM ASX Asx_early, ASX Asx_late
  WHERE Asx_early.Code = Asx_late.Code    --cross the earlier day with the current day
        AND Asx_early."Date" = (
    SELECT max("Date")
    FROM Asx Asx_general
    WHERE Asx_general."Date" < Asx_late."Date"       --find the last exchange day
          AND Asx_general.Code = Asx_early.Code
  )
  ORDER BY Asx_late."Date";

--Find the most active trading stock (the one with the maximum trading volume; if more than one, output all of them) on every trading day. Order your output by "Date" and then by Code.
CREATE OR REPLACE VIEW Q8("Date", Code, Volume) AS
  SELECT
    "Date",
    Code,
    Volume
  FROM ASX Asx_Day
  WHERE Volume = (
    SELECT max(Volume) -- max trading volume
    FROM ASX ASX_All -- look in all stocks
    WHERE ASX_All."Date" = Asx_Day."Date"   -- for the day
  )
  ORDER BY "Date", Code;

--Find the number of companies per Industry. Order your result by Sector and then by Industry.
CREATE OR REPLACE VIEW Q9(Sector, Industry, Number) AS
  SELECT
    Sector,
    Industry,
    Count(Code) AS Number -- number of companies
  FROM Category
  GROUP BY Sector, Industry
  ORDER BY Sector, Industry;

--List all the companies (by their Code) that are the only one in their Industry (i.e., no competitors).
CREATE OR REPLACE VIEW Q10(Code, Industry) AS
  SELECT
    Code,
    Industry
  FROM Category
  WHERE Industry IN (-- locate industries that have only 1 company
    SELECT Industry
    FROM Category
    GROUP BY Industry
    HAVING COUNT(Code) = 1           -- count the companies involved in this industry, must be 1
  )
  ORDER BY Code;

--List all sectors ranked by their average ratings in descending order. AvgRating is calculated by finding the average AvgCompanyRating for each sector (where AvgCompanyRating is the average rating of a company).

CREATE OR REPLACE VIEW AvgCpRating(code, AvgCompanyRating) AS
  SELECT
    code,
    avg(star) AS AvgCompanyRating
  FROM Rating
  GROUP BY code;

-- This is unnecessary, because each company has only one instance in the Table Rating, and thus AvgCompanyRating is the same as its Stat attribute, because average of a single number is always equal to itself. Nevertheless, I followed the instructions anyways.
-- "select Category.Sector, sum(Rating.star) / count(Rating.code) as AvgRating" for the select clause is sufficient for this query, no need for an extra view.

CREATE OR REPLACE VIEW Q11(Sector, AvgRating) AS
  SELECT
    Category.Sector,
    avg(AvgCpRating.AvgCompanyRating) AS AvgRating
  FROM Category, AvgCpRating
  WHERE Category.code = AvgCpRating.code
  GROUP BY Sector
  ORDER BY AvgRating DESC, sector;

--Output the person names of the executives that are affiliated with more than one company.
CREATE OR REPLACE VIEW Q12(Name) AS
  SELECT Person AS Name
  FROM Executive
  GROUP BY Person
  HAVING COUNT(Code) > 1                     -- affiliated with more than one company
  ORDER BY Name;

--Find all the companies with a registered address in Australia, in a Sector where there are no overseas companies in the same Sector. i.e., they are in a Sector that all companies there have local Australia address.
CREATE OR REPLACE VIEW Q13(Code, Name, Address, Zip, Sector) AS
  SELECT
    Company.Code,
    Company.Name,
    Company.Address,
    Company.Zip,
    Category.Sector
  FROM Company, Category
  WHERE Company.Code = Category.Code AND Company.Country = 'Australia' AND Category.sector NOT IN (
    SELECT Sector -- exclude companies outside Australia
    FROM Category, Company
    WHERE Company.Code = Category.Code AND Company.Country != 'Australia'
  )
  ORDER BY Code;

--Calculate stock gains based on their prices of the first trading day and last trading day (i.e., the oldest "Date" and the most recent "Date" of the records stored in the ASX table). Order your result by Gain in descending order and then by Code in ascending order.
CREATE OR REPLACE VIEW Q14(Code, BeginPrice, EndPrice, Change, Gain) AS
  SELECT
    ASX_First.Code,
    Asx_First.Price                                           AS BeginPrice,
    Asx_end.Price                                             AS EndPrice,
    Asx_end.Price - Asx_First.Price                           AS Change,
    (Asx_End.Price - Asx_First.Price) / Asx_First.Price * 100 AS Gain
  FROM ASX Asx_first, ASX Asx_End
  WHERE Asx_first.Code = Asx_End.Code
        AND Asx_first."Date" = (
    SELECT MIN("Date") --first day
    FROM ASX
  )
        AND Asx_end."Date" = (
    SELECT MAX("Date") --last day
    FROM ASX
  )
  ORDER BY Gain DESC, ASX_First.Code ASC;

--For all the trading records in the ASX table, produce the following statistics as a database view (where Gain is measured in percentage). AvgDayGain is defined as the summation of all the daily gains (in percentage) then divided by the number of trading days (as noted above, the total number of days here should exclude the first trading day).
CREATE OR REPLACE VIEW Q15(Code, MinPrice, AvgPrice, MaxPrice, MinDayGain, AvgDayGain, MaxDayGain) AS
  SELECT
    asx.Code,
    min(asx.price) AS MinPrice,
    avg(asx.price) AS AvgPrice,
    max(asx.price) AS MaxPrice,
    min(Q7.gain)   AS MinDayGain,
    avg(Q7.gain)   AS AvgDayGain,
    max(Q7.gain)   AS MaxDayGain
  FROM Q7, asx --Q7 already calculated day gain and changes, just find out the min, max
  WHERE Q7.Code = asx.Code
  GROUP BY asx.Code
  ORDER BY asx.Code;

--Create a trigger on the Executive table, to check and disallow any insert or update of a Person in the Executive table to be an executive of more than one company. 
CREATE OR REPLACE FUNCTION Q16_insert()
  RETURNS TRIGGER AS $$
BEGIN
  IF (new.Person IN (
    SELECT Person
    FROM Executive
    GROUP BY Person --If the person inserted is already an executive of a company
    HAVING COUNT(Code) > 0))
  THEN
    RAISE EXCEPTION 'This person is already an executive of another company.';
  ELSE
    RETURN new;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Q16_ins
BEFORE INSERT ON Executive
FOR EACH ROW
EXECUTE PROCEDURE Q16_insert();

CREATE OR REPLACE FUNCTION Q16_update()
  RETURNS TRIGGER AS $$
BEGIN
  IF (new.Person != old.person AND
      new.person IN (
        SELECT Person
        FROM Executive
        GROUP BY Person -- If one of the companies have its executive changed to
        HAVING COUNT(Code) > 0))    -- a person who is already an executive of a company
  THEN
    RAISE EXCEPTION 'This person is already an executive of another company.';
  ELSE
    RETURN new;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Q16_updt
BEFORE UPDATE ON Executive
FOR EACH ROW
EXECUTE PROCEDURE Q16_update();

--Suppose more stock trading data are incoming into the ASX table. Create a trigger to increase the stock's rating (as Star's) to 5 when the stock has made a maximum daily price gain (when compared with the price on the previous trading day) in percentage within its sector. For example, for a given day and a given sector, if Stock A has the maximum price gain in the sector, its rating should then be updated to 5. If it happens to have more than one stock with the same maximum price gain, update all these stocks' ratings to 5. Otherwise, decrease the stock's rating to 1 when the stock has performed the worst in the sector in terms of daily percentage price gain. If there are more than one record of rating for a given stock that need to be updated, update (not insert) all these records.


-- A helper view to combine the sector name with the code and gain, for convenience
CREATE OR REPLACE VIEW sector_gain AS
  SELECT
    category.sector,
    Q7."Date",
    Q7.code,
    Q7.gain
  FROM category, Q7
  WHERE category.code = Q7.Code AND Q7."Date" = (SELECT max("Date")
                                                 FROM asx)
  ORDER BY sector;

CREATE OR REPLACE FUNCTION Q17_function()
  RETURNS TRIGGER AS $$
DECLARE maxgain DOUBLE PRECISION;
        mingain DOUBLE PRECISION;
        sect    TEXT;
BEGIN

  IF (new.code IN (SELECT code -- if the company is a new one, let it use default star
                   FROM asx))
  THEN
    -- find out the sector of the company inserted
    SELECT DISTINCT category.sector
    INTO sect
    FROM category
    WHERE category.code = new.code;

    --get the max and min gains from this sector for the current day
    SELECT
      max(sector_gain.gain),
      min(sector_gain.gain)
    INTO maxgain, mingain
    FROM sector_gain
    WHERE sector_gain."Date" = new."Date"
          AND sector_gain.sector = sect;

    -- if the company is the best one(s), set 5 star
    UPDATE Rating
    SET Star = 5
    WHERE Code IN (SELECT code
                   FROM sector_gain
                   WHERE sector_gain.gain = maxgain AND sector_gain.sector = sect);

    -- if there is an even better/worse company appearing for the same day, then the previous best/worse company is no longer the best/worse and its score needs to be reset.
    UPDATE Rating
    SET Star = 3
    WHERE Code IN (SELECT code
                   FROM sector_gain
                   WHERE sector_gain.gain != maxgain
                         AND sector_gain.gain != mingain
                         AND sector_gain.sector = sect);
    -- if the company is the worse one(s), set 1 star
    UPDATE Rating
    SET Star = 1
    WHERE Code IN (SELECT code
                   FROM sector_gain
                   WHERE sector_gain.gain = mingain AND sector_gain.sector = sect);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER Q17
AFTER INSERT ON ASX
FOR EACH ROW
EXECUTE PROCEDURE Q17_function();

--Stock price and trading volume data are usually incoming data and seldom involve updating existing data. However, updates are allowed in order to correct data errors. All such updates (instead of data insertion) are logged and stored in the ASXLog table. Create a trigger to log any updates on Price and/or Voume in the ASX table and log these updates (only for update, not inserts) into the ASXLog table. Here we assume that Date and Code cannot be corrected and will be the same as their original, old values. Timestamp is the date and time that the correction takes place. Note that it is also possible that a record is corrected more than once, i.e., same Date and Code but different Timestamp.
CREATE OR REPLACE FUNCTION Q18_function()
  RETURNS TRIGGER AS $$
BEGIN
  IF (NEW."Date" = OLD."Date" AND OLD.Code = NEW.Code)
  THEN -- do the logging
    INSERT INTO ASXLog ("Timestamp", Code, "Date", OldVolume, OldPrice)
    VALUES (CURRENT_TIMESTAMP, OLD.Code, OLD."Date", OLD.Volume, OLD.Price);
  ELSE 		--we assume that Date and Code cannot be corrected and will be the same as their original
    RAISE EXCEPTION 'The Date and Code must not be corrected.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Q18
BEFORE UPDATE ON ASX
FOR EACH ROW
EXECUTE PROCEDURE Q18_function();

























