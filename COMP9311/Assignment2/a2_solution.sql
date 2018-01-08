-- COMP9311 17s2 Assignment 2 - Sample Solutions
-- These are sample solutions ONLY. Other solutions are also acceptable
-- Each of the 18 queries is worth 2 marks.
-- The total mark M will be out of 36 then it will be scaled to 15 by applying the following formula:
-- final_a2_mark = M*15/36


-- Q1 ---------------------------------------
CREATE OR REPLACE VIEW Q1(Name, Country) AS
SELECT c.name, c.country 
FROM company AS c
WHERE c.country <> 'Australia';

-- Q2 ---------------------------------------
CREATE OR REPLACE VIEW Q2(Code) AS
SELECT e.code
FROM executive AS e
GROUP by e.Code
HAVING count(e.person) > 5;

-- Q3 ---------------------------------------
CREATE OR REPLACE VIEW Q3(Name) AS
SELECT co.name
FROM company AS co
INNER JOIN category ca ON co.code = ca.code AND ca.sector = 'Technology';

-- Q4 ---------------------------------------
CREATE OR REPLACE VIEW Q4(Sector, Number) AS
SELECT c.sector,
    count(DISTINCT c.industry)  -- eliminate the duplicated records since an industry can consist of multiple companies
FROM category AS c
GROUP BY c.sector;

-- Q5 ---------------------------------------
CREATE OR REPLACE VIEW Q5 (Name) AS 
SELECT DISTINCT e.person 
FROM executive AS e 
INNER JOIN category AS c ON e.code = c.code 
AND c.sector = 'Technology';

-- Q6 ---------------------------------------
CREATE OR REPLACE VIEW Q6(Name) AS
SELECT co.name
FROM category AS ca
INNER JOIN company AS co ON co.code = ca.code AND co.country = 'Australia'
AND co.zip like '2%'
WHERE ca.sector = 'Services';

-- Q7 ---------------------------------------
-- intermediate view that support Q7 and later questions
-- numbering the ASX table
CREATE OR REPLACE VIEW ASXNum (num, dt, code, volume, price) AS
SELECT
    -- numbering the records for each code for later use
    -- link the previous date by this num
    Row_number() over(PARTITION BY a.code ORDER BY a.code, a."Date") AS num, 
    a.* 
FROM asx AS a;

CREATE OR REPLACE VIEW Q7("Date", Code, Volume, PrevPrice, Price, Change, Gain) AS 
SELECT 
    a.dt, 
    a.code, 
    a.volume, 
    aPre.price                                   AS PrevPrice, 
    a.price                                      AS CurrPrice, 
    a.price - aPre.price                         AS PriceChange, 
    (a.price - aPre.price) * 100.00 / aPre.price AS Gain 
FROM ASXNum AS a 
     left JOIN ASXNum AS aPre 
            ON a.code = aPre.code 
           AND a.num  = aPre.num + 1 
WHERE  a.num > 1;

-- Q8 ---------------------------------------
-- intermediate view that support Q8
-- retrive largest volume for each date
CREATE OR REPLACE VIEW Q8supp("Date", Code, Volume) AS
SELECT
    tmp.dt,
    tmp.code,
    tmp.volume
FROM
(
    SELECT
        Row_number() over(PARTITION BY a."Date" ORDER BY a.volume desc) AS num, -- number the records by volume for each date
        a."Date" AS DT,
        a.code,
 	a.volume
    FROM asx AS a
)AS tmp
WHERE tmp.num = 1;

CREATE OR REPLACE VIEW Q8("Date", Code, Volume) AS
SELECT
    a."Date",
    a.code,
    a.volume
FROM asx AS a
INNER JOIN Q8supp supp 
        ON a."Date" = supp."Date"
       AND a.volume = supp.volume  -- any code has the largest volume on that day should be listed
ORDER BY a."Date", a.code;

-- Q9 ---------------------------------------
CREATE OR REPLACE VIEW Q9(Sector, Industry, Number) AS
SELECT
    c.sector,
    c.industry,
    count(DISTINCT c.code) AS cnt
FROM category AS c
GROUP BY c.sector, c.industry
ORDER BY c.sector, c.industry;

-- Q10 -------------------------------------
CREATE OR REPLACE VIEW Q10(Code, Industry) AS
SELECT
    c.code,
    c.industry
FROM category AS c
WHERE not EXISTS
(
    SELECT
        tmp.code
    FROM category AS tmp
    WHERE tmp.industry = c.industry
          AND tmp.code <> c.code
);

-- Q11 ------------------------------------
CREATE OR REPLACE VIEW Q11(Sector, AvgRating) AS
SELECT
    cmpy.sector,
    AVG(cmpy.AvgCompanyStar)
FROM
(
    -- calculate the average star for each company first
    SELECT
        c.sector,
        c.code,
        AVG(r.star) AS AvgCompanyStar
    FROM category AS c
    INNER JOIN rating AS r 
            ON c.code = r.code
    GROUP BY c.sector, c.code
) AS cmpy
GROUP BY cmpy.sector
ORDER BY AVG(cmpy.AvgCompanyStar) DESC;

-- Q12 ------------------------------------
CREATE OR REPLACE VIEW Q12(Name) AS
SELECT
    tmp.person
FROM
(
    SELECT
        e.person,
        COUNT(DISTINCT e.code)
    FROM executive AS e
    GROUP BY e.person
    HAVING COUNT(DISTINCT e.code) > 1 -- more than one company
) AS tmp;

-- Q13 ------------------------------------
CREATE OR REPLACE VIEW Q13(Code, Name, Address, Zip, Sector) AS
SELECT
    co.code,
    co.name,
    co.address,
    co.zip,
    ca.sector
FROM company AS co
INNER JOIN category AS ca 
        ON co.code = ca.code
-- list the companies that do not in those sectors
WHERE ca.sector NOT IN
(
    -- retrieve the sectors which have oversea companies
    SELECT
        ca.sector
    FROM company AS co
    INNER JOIN category AS ca 
       ON co.code = ca.code
    WHERE co.country <> 'Australia'
);

-- Q14 ------------------------------------
CREATE OR REPLACE VIEW Q14(Code, BeginPrice, EndPrice, Change, Gain) AS
SELECT
    asxn.code,
    old.price,
    new.price,
    new.price - old.price                        AS change,
    (new.price - old.price) * 100.00 / old.price AS Gain
FROM 
(
    -- retrieve the oldest and latest trading date for each company
    SELECT
        a.code,
        MIN(a."Date") AS mi,
        MAX(a."Date") AS mx
    FROM ASX AS a
    GROUP BY a.code
) AS asxn
-- retrieve the prices for both the oldest and latest date for each company
INNER JOIN ASX old 
        ON old.code    = asxn.code
       AND old."Date"  = asxn.mi
INNER JOIN ASX new
        ON new.code    = asxn.code
       AND new."Date"  = asxn.mx
ORDER BY Gain DESC, asxn.code ASC;

-- Q15 ------------------------------------
CREATE OR REPLACE VIEW Q15(Code, MinPrice, AvgPrice, MaxPrice, MinDayGain, AvgDayGain, MaxDayGain) AS
WITH Price AS
(
    SELECT
        a.code,
        MIN(a.price) AS MinPrice,
        AVG(a.price) AS AvgPrice,
        MAX(a.price) AS MaxPrice
    FROM ASX AS a
    GROUP BY a.code
),
Gain AS
(
    SELECT
        q.code,
        MIN(q.gain) AS MinDayGain,
        AVG(q.gain) AS AvgDayGain,
        MAX(q.gain) AS MaxDayGain
    FROM q7 AS q
    GROUP BY q.code
)
SELECT
    p.code,
    p.MinPrice,
    p.AvgPrice,
    p.MaxPrice,
    g.MinDayGain,
    g.AvgDayGain,
    g.MaxDayGain
FROM price AS p
INNER JOIN gain AS g
        ON p.code = g.code;

-- Q16 Insert -----------------------------
CREATE OR REPLACE FUNCTION insertExecutive() RETURNS TRIGGER
AS $$
DECLARE
    e executive;
BEGIN
    SELECT * into e FROM executive AS ex WHERE ex.person = new.person;
    -- if this person can be found in the table, do nothing
    IF (e.person = new.person) THEN
      RETURN NULL;
    ELSE
      UPDATE executive
      SET code   = new.code,
          person = new.person
      WHERE code = new.code AND person = new.person;
      RETURN new;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER checkInsert_Executive
BEFORE INSERT ON executive
FOR EACH ROW
EXECUTE PROCEDURE insertExecutive();

-- Q16 Update -----------------------------
CREATE OR REPLACE FUNCTION updateExecutive() RETURNS TRIGGER
AS $$
DECLARE
    cnt INTEGER;
BEGIN
    SELECT count(1) into cnt FROM executive AS ex WHERE ex.person = new.person;
    -- if this person only has one position, do nothing
    IF (cnt <= 1) THEN
      RETURN NULL;
    ELSE
      -- reset the record to its old value
      UPDATE executive
      SET code   = old.code,
          person = old.person
      WHERE code = new.code AND person = new.person;
      RETURN old;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER checkUpdate_Executive
AFTER UPDATE ON executive
FOR EACH ROW
EXECUTE PROCEDURE updateExecutive();

-- Q17 ------------------------------------
-- supplementary view to support Q17
-- Retrieve the maximal and minimal daily gain for each sector
CREATE OR REPLACE VIEW Q17S(DT, Sector, MaxGain, MinGain) AS
SELECT
    q."Date"    AS DT,
    c.sector,
    MAX(q.gain) AS MaxGain,
    MIN(q.gain) AS MinGain
FROM q7 q
INNER JOIN category AS c
        ON q.code = c.code
GROUP BY q."Date", c.sector;

CREATE OR REPLACE FUNCTION insertASX() RETURNS TRIGGER
AS $$
DECLARE
    MxGain   FLOAT;
    MnGain   FLOAT;
    CurrGain FLOAT;
    sect     TEXT;
BEGIN
    SELECT c.sector INTO sect
    FROM category AS c
    WHERE c.code = new.code;
	
    -- Get Max, Min Gain --
    SELECT q.MaxGain, q.MinGain INTO MxGain, MnGain
    FROM Q17S AS q
    WHERE q.dt   = new."Date"
    AND   q.sector = sect;

    SELECT q.gain INTO CurrGain
    FROM Q7 AS q
    WHERE q."Date" = new."Date"
    AND   q.code   = new.code;
	
    IF (CurrGain <= MnGain) THEN
        UPDATE rating
        SET star = 1
        WHERE code = new.code;
    END IF;
	
    IF (CurrGain >= MxGain) THEN
        UPDATE rating
        SET star = 5
        WHERE code = new.code;
    END IF;
	
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER checkInsert_ASX
AFTER INSERT ON ASX
FOR EACH ROW
EXECUTE PROCEDURE insertASX();

-- Q18 ------------------------------------
CREATE OR REPLACE FUNCTION updateASX() RETURNS TRIGGER
AS $$
BEGIN
    INSERT INTO asxlog values(localtimestamp, old."Date", old.code, old.volume, old.price);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER LogUpdate_ASX
AFTER UPDATE ON asx
FOR EACH ROW
EXECUTE PROCEDURE updateASX();
