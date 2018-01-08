-- Beer rating database


-- Location(id, state, country)

copy Location from stdin;
1	New South Wales	Australia
2	Victoria	Australia
3	Queensland	Australia
4	Western Australia	Australia
5	California	U.S.A.
6	Wisconsin	U.S.A.
7	\N	England
8	\N	Scotland
9	\N	Belgium
10	South Australia	Australia
11	Tasmania	Australia
12	Oregon	U.S.A.
13	Wisconsin	U.S.A.
14	Texas	U.S.A.
\.
select setval('Location_id_seq', max(id)) as "Location id" from Location;


-- Taster(id, family, given, livesIn)

copy Taster from stdin;
1	Shepherd	John	1
2	Wiggins	Adam	1
3	Ullman	Jeff	5
4	Claughton	Sarah	7
5	Ramakrishnan	Raghu	13
6	Elmasri	Ramez	14
7	Garcia-Molina	Hector	5
8	Richardson	Geoff	2
9	Beatty	Peter	3
10	Porteous	Rose	4
\.
select setval('Taster_id_seq', max(id)) as "Taster id" from Taster;


-- BeerStyle(id, name)

copy BeerStyle from stdin;
1	Lager
2	Pilsner
3	Pale Ale
4	Barleywine
5	Bock
6	Stout
7	Porter
8	Bitter
9	Trappist
10	Imperial Stout
11	Lambic
12	Ale
13	Scotch Ale
14	Wheat Beer
\.
select setval('BeerStyle_id_seq', max(id)) as "BeerStyle id" from BeerStyle;


-- Brewer(id, name, locatedIn)

copy Brewer from stdin;
1	Carlton and United	2
2	Castlemaine/Perkins	3
3	Toohey's	1
4	Scharer's Little Brewery	1
5	Matilda Bay Brewing	4
6	Sierra Nevada	5
7	New Glarus Brewing	6
8	Pete's	5
9	North Coast Brewing	5
10	Chimay	9
11	Calendonian Brewing	8
12	Maltshovel Brewery	1
13	Cooper's	10
14	Cascade	11
\.
select setval('Brewer_id_seq', max(id)) as "Brewer id" from Brewer;


-- Beer(id, name, style, brewer)

copy Beer from stdin;
1	Rasputin	10	9
2	80/-	13	11
3	Pale Ale	3	6
4	Old Tire	11	7
5	Old	12	3
6	New	1	3
7	Fosters	1	1
8	James Squire Amber Ale	12	12
9	James Squire Pilsener	2	12
10	Burragorang Bock	5	4
11	Scharer's Lager	1	4
12	Chimay Red	9	10
13	Chimay Blue	9	10
14	Victoria Bitter	1	1
15	Sterling	1	1
16	Empire	1	1
17	Premium Light	1	14
18	Sparkling Ale	12	13
19	Sheaf Stout	3	3
20	Crown Lager	1	1
21	Bigfoot Barley Wine	4	6
22	James Squire Porter	7	12
23	Redback	14	5
24	XXXX	1	2
25	Red	1	3
\.
select setval('Beer_id_seq', max(id)) as "Beer id" from Beer;


-- Ratings(taster, beer, score)

copy Ratings from stdin;
1	1	4
1	2	4
1	3	5
1	12	3
1	14	1
1	16	3
1	20	2
2	14	1
2	5	4
2	6	1
3	1	1
3	10	3
3	3	4
4	10	4
4	11	3
4	14	1
4	5	3
4	6	2
4	8	3
4	9	3
5	4	5
5	3	3
5	1	3
6	21	3
6	3	4
7	3	4
7	7	3
8	16	3
8	9	4
8	23	4
9	24	5
10	23	5
\.
