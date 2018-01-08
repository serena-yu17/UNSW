import pygal.maps.world as pw
from csv import reader
from os import path
import pycountry
from pygal.style import Style
from webbrowser import open_new_tab


def isNum(s):
    if len(s) == 0:
        return 0
    for i in range(len(s)):
        if not (s[i].isdigit() or s[i] == '.'):
            return 0
    return 1


def alpha_two(cuy):
    if len(cuy) != 3:
        return None
    try:
        country = pycountry.countries.lookup(cuy)
    except LookupError:
        return None
    return country.alpha_2


cuty = set()
for key in pw.COUNTRIES:
    cuty.add(key)
co2 = dict()
data_path = path.abspath(path.join(path.dirname(__file__), "API_EN", "API_EN.ATM.CO2E.KT_DS2_en_csv_v2.csv"))
with open(data_path, "r") as f:
    csvdt = reader(f)
    for row in csvdt:
        if len(row) > 56:
            code = alpha_two(row[1])
            if code is not None:
                code = code.lower()
                if code in cuty:
                    if isNum(row[55]):
                        co2[code] = float(row[55])
                else:
                    print("Leaving out", row[0])
            else:
                print("Leaving out", row[0])
nodata = dict()
for code in cuty:
    if code not in co2:
        nodata[code]='?'

wmp = pw.World()
wmp.force_uri_protocol = "http"
wmp.title = "CO2 emissions in 2011"
wmp.add("Known data", co2)
wmp.add("No data", nodata)
wmp.style = Style(colors=("#B22222", "#A9A9A9"), legend_font_size=10, tooltip_font_size=8)
wmp.render()
wmp.render_to_file("CO2_emissions.svg")
#
# Open browser window
open_new_tab("file://" + path.realpath("CO2_emissions.svg"))
