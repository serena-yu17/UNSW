


# IMPORTANT:
#   POSTGRESQL must be running at the local machine and the database ASX has
#   been created and populated.
#   Your POSTGRESQL user must have permission to connect
#   Find pg_hba.conf from this command
#       SHOW hba_file;
#   in POSTGRESQL
#
#
import psycopg2
from psycopg2.extensions import AsIs
import datetime
import subprocess
import os
import sys
from getpass import getpass

s = input("Input your login to PostgreSQL\nLeave blank for default: postgres @ localhost : 5432\n")
if len(s) == 0:
    uname = "postgres"
    hst = "localhost"
    prt = "5432"
else:
    s = s.split("@")
    uname = s[0].strip()
    hst = "localhost"
    prt = "5432"
    if len(s) == 2 and s[1] != "":
        s1 = s[1].split(":")        
        hst = s1[0].strip()
        if len(s1) == 2 and s1[1] != "":
            prt = s1[1].strip()
dbn = input("Input the name of your database (default: asx)\n")
if len(dbn) == 0:
    dbn = "asx"
print(f"{uname} on {hst}:{prt}, db {dbn}")
psd = getpass()
lines = []
print("Processing...")
conn = psycopg2.connect(dbname=dbn, user=uname, password=psd, host=hst, port=prt)
conn.autocommit = True
cur = conn.cursor()

def read_cur():
    columns = [desc[0] for desc in cur.description]
    lines.append("\t".join(columns))
    lines.append("--------------------------")
    count = 0
    for tup in cur.fetchall():
        if tup is not None and len(tup) > 0:
            ls = list()
            for elem in tup:
                ls.append(str(elem))
            count += 1
            lines.append("\t".join(ls))
    lines.append("--------------------------")
    lines.append(f"({count} rows)")

for i in range(1, 16):
    s = f"SELECT * FROM Q{i};"
    lines.append("\n" + s)
    cur.execute(s)
    read_cur() 

# 16
lines.append(("\n---------------\n>>>Q16 trigger\t\n",))
lines.append("\n>>> Running tests...\n")
lines.append(">>> Here should receive 2 exceptions:\n")
try:
    cur.execute("INSERT INTO Executive VALUES(%s,%s);", ('AAD', 'Mr. Stephen John Mikkelsen BBS, CA'))
except psycopg2.Error as e:
    lines.append("EXCEPTION: " + e.diag.message_primary + '\n')
try:    
    cur.execute("Update Executive set person = 'Mr. Michael Kelly' where code = 'AAD' and person = 'Mr. Charlie Keegan';")
except psycopg2.Error as e:
    lines.append("EXCEPTION: " + e.diag.message_primary + '\n')

lines.append(">>> The below query should be empty:\n")
cur.execute("SELECT * FROM Executive WHERE Code = 'AAD' AND (Person = 'Mr. Stephen John Mikkelsen BBS, CA' or Person = 'Mr. Michael Kelly');")
read_cur()
# restore
lines.append("\n>>> Reverting changes...")
cur.execute("DELETE FROM Executive WHERE Code = 'AAD' AND Person = 'Mr. Stephen John Mikkelsen BBS, CA';")
cur.execute("Update Executive set person = 'Mr. Charlie Keegan' where code = 'AAD' and person = 'Mr. Michael Kelly';")


# 17
lines.append(("\n---------------\n>>>Q17 trigger.\t\n",))
lines.append("\n>>> Running tests...")
cur.execute("DELETE FROM ASX WHERE %s = %s;", (AsIs('"Date"'), datetime.date(2012, 3, 30)))
cur.execute('''INSERT INTO ASX VALUES('2012-03-30','AAD','781200','0.99');
INSERT INTO ASX VALUES('2012-03-30','ABC','1454100','2.70');
INSERT INTO ASX VALUES('2012-03-30','ABP','1824000','1.88');
INSERT INTO ASX VALUES('2012-03-30','ACR','554200','3.98');
INSERT INTO ASX VALUES('2012-03-30','AGK','1822700','14.18');
INSERT INTO ASX VALUES('2012-03-30','AGO','11455000','2.73');
INSERT INTO ASX VALUES('2012-03-30','AIO','2847000','4.81');
INSERT INTO ASX VALUES('2012-03-30','ALL','1537100','2.93');
INSERT INTO ASX VALUES('2012-03-30','ALZ','437800','2.35');
INSERT INTO ASX VALUES('2012-03-30','AMC','6224600','7.06');
INSERT INTO ASX VALUES('2012-03-30','AMP','11066600','4.13');
INSERT INTO ASX VALUES('2012-03-30','ANN','720600','14.46');
INSERT INTO ASX VALUES('2012-03-30','ANZ','17541700','21.39');
INSERT INTO ASX VALUES('2012-03-30','APN','1712800','0.88');
INSERT INTO ASX VALUES('2012-03-30','AQA','543700','5.00');
INSERT INTO ASX VALUES('2012-03-30','AQP','1133900','2.23');
INSERT INTO ASX VALUES('2012-03-30','ASL','1843300','3.92');
INSERT INTO ASX VALUES('2012-03-30','ASX','1577300','30.79');
INSERT INTO ASX VALUES('2012-03-30','AUT','1521500','3.78');
INSERT INTO ASX VALUES('2012-03-30','AWC','20726400','1.24');
INSERT INTO ASX VALUES('2012-03-30','AWE','4380600','2.00');
INSERT INTO ASX VALUES('2012-03-30','BBG','1823900','2.78');
INSERT INTO ASX VALUES('2012-03-30','BDR','2982000','0.68');
INSERT INTO ASX VALUES('2012-03-30','BEN','1754300','7.47');
INSERT INTO ASX VALUES('2012-03-30','BHP','24907900','32.87');
INSERT INTO ASX VALUES('2012-03-30','BKN','541700','8.06');
INSERT INTO ASX VALUES('2012-03-30','BLD','5471700','3.95');
INSERT INTO ASX VALUES('2012-03-30','BLY','2555000','4.00');
INSERT INTO ASX VALUES('2012-03-30','BOQ','4356600','6.58');
INSERT INTO ASX VALUES('2012-03-30','BPT','21398500','1.44');
INSERT INTO ASX VALUES('2012-03-30','BRU','1405300','3.22');
INSERT INTO ASX VALUES('2012-03-30','BSL','3846400','14.22');
INSERT INTO ASX VALUES('2012-03-30','BXB','6615400','6.88');
INSERT INTO ASX VALUES('2012-03-30','CAB','375400','5.46');
INSERT INTO ASX VALUES('2012-03-30','CBA','11897600','45.91');
INSERT INTO ASX VALUES('2012-03-30','CCL','5367000','11.74');
INSERT INTO ASX VALUES('2012-03-30','CDD','245700','6.49');
INSERT INTO ASX VALUES('2012-03-30','CDU','286400','3.47');
INSERT INTO ASX VALUES('2012-03-30','CGF','2410800','3.80');
INSERT INTO ASX VALUES('2012-03-30','CHC','389500','2.06');
INSERT INTO ASX VALUES('2012-03-30','COH','502200','60.05');
INSERT INTO ASX VALUES('2012-03-30','CPL','2796900','1.65');
INSERT INTO ASX VALUES('2012-03-30','CPU','3943600','8.64');
INSERT INTO ASX VALUES('2012-03-30','CQR','1311200','2.90');
INSERT INTO ASX VALUES('2012-03-30','CRZ','1224100','5.30');
INSERT INTO ASX VALUES('2012-03-30','CSL','3557200','35.42');
INSERT INTO ASX VALUES('2012-03-30','CTX','1028800','13.59');
INSERT INTO ASX VALUES('2012-03-30','CWN','1542500','8.43');
INSERT INTO ASX VALUES('2012-03-30','DCG','679700','2.62');
INSERT INTO ASX VALUES('2012-03-30','DJS','6168400','2.17');
INSERT INTO ASX VALUES('2012-03-30','DML','1003300','1.60');
INSERT INTO ASX VALUES('2012-03-30','DOW','2041400','3.86');
INSERT INTO ASX VALUES('2012-03-30','DUE','4324200','1.70');
INSERT INTO ASX VALUES('2012-03-30','DXS','29529500','0.81');
INSERT INTO ASX VALUES('2012-03-30','EHL','2033400','1.00');
INSERT INTO ASX VALUES('2012-03-30','ENV','1150600','0.72');
INSERT INTO ASX VALUES('2012-03-30','EWC','1122600','0.79');
INSERT INTO ASX VALUES('2012-03-30','FBU','939800','4.99');
INSERT INTO ASX VALUES('2012-03-30','FKP','304900','23.95');
INSERT INTO ASX VALUES('2012-03-30','FLT','421400','21.08');
INSERT INTO ASX VALUES('2012-03-30','FMG','22580600','5.75');
INSERT INTO ASX VALUES('2012-03-30','FWD','105600','11.45');
INSERT INTO ASX VALUES('2012-03-30','FXJ','8123600','0.68');
INSERT INTO ASX VALUES('2012-03-30','GBG','1554400','0.62');
INSERT INTO ASX VALUES('2012-03-30','GFF','9592100','0.66');
INSERT INTO ASX VALUES('2012-03-30','GMG','9613400','16.02');
INSERT INTO ASX VALUES('2012-03-30','GNC','1113000','8.76');
INSERT INTO ASX VALUES('2012-03-30','GPT','11967300','2.93');
INSERT INTO ASX VALUES('2012-03-30','GRY','1001200','1.08');
INSERT INTO ASX VALUES('2012-03-30','GUD','301900','7.64');
INSERT INTO ASX VALUES('2012-03-30','HGG','3849800','1.75');
INSERT INTO ASX VALUES('2012-03-30','HVN','4296000','1.89');
INSERT INTO ASX VALUES('2012-03-30','IAG','6655700','3.24');
INSERT INTO ASX VALUES('2012-03-30','IAU','3243500','0.74');
INSERT INTO ASX VALUES('2012-03-30','IFL','608600','5.48');
INSERT INTO ASX VALUES('2012-03-30','IGO','920100','3.94');
INSERT INTO ASX VALUES('2012-03-30','ILU','2361800','17.15');
INSERT INTO ASX VALUES('2012-03-30','IMD','479500','2.92');
INSERT INTO ASX VALUES('2012-03-30','IOF','2694200','9.40');
INSERT INTO ASX VALUES('2012-03-30','IPL','14517800','3.00');
INSERT INTO ASX VALUES('2012-03-30','IRE','165600','6.58');
INSERT INTO ASX VALUES('2012-03-30','IVC','134500','7.74');
INSERT INTO ASX VALUES('2012-03-30','JBH','643600','10.36');
INSERT INTO ASX VALUES('2012-03-30','JHX','1636600','7.30');
INSERT INTO ASX VALUES('2012-03-30','KAR','569800','6.51');
INSERT INTO ASX VALUES('2012-03-30','KCN','628100','6.24');
INSERT INTO ASX VALUES('2012-03-30','LEI','5203500','20.65');
INSERT INTO ASX VALUES('2012-03-30','LLC','1899900','7.18');
INSERT INTO ASX VALUES('2012-03-30','LNC','2050000','1.15');
INSERT INTO ASX VALUES('2012-03-30','LYC','21446600','1.10');
INSERT INTO ASX VALUES('2012-03-30','MAH','3801000','0.82');
INSERT INTO ASX VALUES('2012-03-30','MBN','7259700','0.56');
INSERT INTO ASX VALUES('2012-03-30','MDL','114400','6.28');
INSERT INTO ASX VALUES('2012-03-30','MGR','23465500','1.10');
INSERT INTO ASX VALUES('2012-03-30','MGX','5111200','1.05');
INSERT INTO ASX VALUES('2012-03-30','MIN','418900','11.66');
INSERT INTO ASX VALUES('2012-03-30','MML','1603100','5.03');
INSERT INTO ASX VALUES('2012-03-30','MND','284000','22.45');
INSERT INTO ASX VALUES('2012-03-30','MQA','1074700','1.68');
INSERT INTO ASX VALUES('2012-03-30','MRM','575100','3.10');
INSERT INTO ASX VALUES('2012-03-30','MSB','488800','7.85');
INSERT INTO ASX VALUES('2012-03-30','MTU','222400','3.45');
INSERT INTO ASX VALUES('2012-03-30','MYR','6778800','2.16');
INSERT INTO ASX VALUES('2012-03-30','NCM','8478400','29.39');
INSERT INTO ASX VALUES('2012-03-30','NUF','1230000','4.74');
INSERT INTO ASX VALUES('2012-03-30','NVT','487600','3.34');
INSERT INTO ASX VALUES('2012-03-30','NWH','1277200','3.65');
INSERT INTO ASX VALUES('2012-03-30','OGC','459700','2.53');
INSERT INTO ASX VALUES('2012-03-30','ORG','6147700','12.55');
INSERT INTO ASX VALUES('2012-03-30','ORI','3607400','26.63');
INSERT INTO ASX VALUES('2012-03-30','OSH','7646800','6.94');
INSERT INTO ASX VALUES('2012-03-30','OZL','2429900','9.24');
INSERT INTO ASX VALUES('2012-03-30','PAN','1034600','1.08');
INSERT INTO ASX VALUES('2012-03-30','PBG','1752200','0.55');
INSERT INTO ASX VALUES('2012-03-30','PDN','11408100','1.84');
INSERT INTO ASX VALUES('2012-03-30','PNA','3929300','2.96');
INSERT INTO ASX VALUES('2012-03-30','PPT','173400','24.72');
INSERT INTO ASX VALUES('2012-03-30','PRU','2328800','2.35');
INSERT INTO ASX VALUES('2012-03-30','PRY','2125400','2.72');
INSERT INTO ASX VALUES('2012-03-30','PTM','803600','3.85');
INSERT INTO ASX VALUES('2012-03-30','QAN','13147800','1.78');
INSERT INTO ASX VALUES('2012-03-30','QBE','11262300','13.76');
INSERT INTO ASX VALUES('2012-03-30','QUB','1710200','1.63');
INSERT INTO ASX VALUES('2012-03-30','RHC','508500','19.10');
INSERT INTO ASX VALUES('2012-03-30','RIO','9530900','65.40');
INSERT INTO ASX VALUES('2012-03-30','RMD','3970200','2.96');
INSERT INTO ASX VALUES('2012-03-30','RMS','1225700','0.86');
INSERT INTO ASX VALUES('2012-03-30','RRL','1498300','4.08');
INSERT INTO ASX VALUES('2012-03-30','RSG','2635200','1.76');
INSERT INTO ASX VALUES('2012-03-30','SAR','2116100','0.56');
INSERT INTO ASX VALUES('2012-03-30','SBM','794200','2.06');
INSERT INTO ASX VALUES('2012-03-30','SDL','11050600','0.45');
INSERT INTO ASX VALUES('2012-03-30','SEK','896300','6.95');
INSERT INTO ASX VALUES('2012-03-30','SFR','308800','7.89');
INSERT INTO ASX VALUES('2012-03-30','SGM','619100','14.58');
INSERT INTO ASX VALUES('2012-03-30','SGP','39293300','2.60');
INSERT INTO ASX VALUES('2012-03-30','SGT','588300','2.26');
INSERT INTO ASX VALUES('2012-03-30','SHL','1786600','12.06');
INSERT INTO ASX VALUES('2012-03-30','SIP','1839900','0.59');
INSERT INTO ASX VALUES('2012-03-30','SKI','10670600','1.43');
INSERT INTO ASX VALUES('2012-03-30','SLR','625600','3.41');
INSERT INTO ASX VALUES('2012-03-30','SMX','134900','5.45');
INSERT INTO ASX VALUES('2012-03-30','SPN','6453400','0.98');
INSERT INTO ASX VALUES('2012-03-30','STO','6209400','13.76');
INSERT INTO ASX VALUES('2012-03-30','SUL','773300','7.22');
INSERT INTO ASX VALUES('2012-03-30','SUN','6629500','8.05');
INSERT INTO ASX VALUES('2012-03-30','SVW','617800','9.48');
INSERT INTO ASX VALUES('2012-03-30','SXL','1072500','1.19');
INSERT INTO ASX VALUES('2012-03-30','TAH','9744400','2.47');
INSERT INTO ASX VALUES('2012-03-30','TCL','8916800','5.45');
INSERT INTO ASX VALUES('2012-03-30','TEN','8945000','0.81');
INSERT INTO ASX VALUES('2012-03-30','TLS','101466900','2.99');
INSERT INTO ASX VALUES('2012-03-30','TOL','3820500','5.59');
INSERT INTO ASX VALUES('2012-03-30','TPI','2623500','0.78');
INSERT INTO ASX VALUES('2012-03-30','TPM','837100','1.71');
INSERT INTO ASX VALUES('2012-03-30','TRS','35100','11.75');
INSERT INTO ASX VALUES('2012-03-30','TRY','230300','4.50');
INSERT INTO ASX VALUES('2012-03-30','TSE','12304500','2.37');
INSERT INTO ASX VALUES('2012-03-30','TTS','7199600','2.37');
INSERT INTO ASX VALUES('2012-03-30','UGL','1597500','12.40');
INSERT INTO ASX VALUES('2012-03-30','WBC','19079700','19.88');
INSERT INTO ASX VALUES('2012-03-30','WDC','15146400','8.83');
INSERT INTO ASX VALUES('2012-03-30','WES','5940300','30.02');
INSERT INTO ASX VALUES('2012-03-30','WHC','2862700','5.59');
INSERT INTO ASX VALUES('2012-03-30','WOR','2166000','27.71');
INSERT INTO ASX VALUES('2012-03-30','WOW','6589300','24.71');
INSERT INTO ASX VALUES('2012-03-30','WPL','8515700','33.62');
INSERT INTO ASX VALUES('2012-03-30','WSA','427000','5.33');
INSERT INTO ASX VALUES('2012-03-30','WTF','522000','4.35');''')
cur.execute('''SELECT category.sector, Q7.code, rating.star FROM Q7,Rating, category 
where Q7.code=rating.code and category.code = Q7.code and Q7."Date" = '2012-03-30'
order by category.sector, Q7.gain;''')
lines.append("For each section below, the first company should have 1 star, and the last company in the section 5 star. Ties are allowed.")
read_cur()
# restore 17
lines.append("\n>>> Reverting changes...")
cur.execute("UPDATE Rating SET Star = 3;")


# 18
lines.append("\n---------------\nQ18 trigger.\t\n")
cur.execute('UPDATE ASX SET Price = 1.20, volume = 271200 WHERE %s = %s AND Code = %s;',
            (AsIs('"Date"'), datetime.date(2012, 1, 3), 'AAD'))
cur.execute('UPDATE ASX SET Price = 0.91, volume = 171200 WHERE %s = %s AND Code = %s;',
            (AsIs('"Date"'), datetime.date(2012, 1, 3), 'AAD'))
lines.append(">>> 2 records should appear in ASXLog now:\n\n")
cur.execute("SELECT * FROM ASXLog;")
read_cur()
# resore 18
lines.append("\n>>> Reverting changes...")
cur.execute("DELETE FROM ASXLog;")


filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "view_tests.txt")

with open(filepath, 'w') as f:
    for line in lines:
        if line is None:
            continue
        if isinstance(line, str):
            f.write(line)
        else:
            for item in line:
                f.write(str(item))
                f.write('\t')
        f.write('\n')

print("\nTest output file saved to:")
print(os.path.abspath(filepath))

if sys.platform.startswith('darwin'):
    subprocess.call(('open', filepath))
elif os.name == 'nt':
    os.startfile(filepath)
elif os.name == 'posix':
    subprocess.call(('vi', filepath))
