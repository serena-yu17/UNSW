from csv import reader
import matplotlib.pyplot as plt
from calendar import month_name
from collections import deque

strmax = "Mean maximum temperature (Degrees C) for years 1859 to 2016 "
tmpmax = deque()
strmin = "Mean minimum temperature (Degrees C) for years 1859 to 2016 "
tmpmin = deque()
with open("IDCJCM0037_066062.csv") as f:
    for row in reader(f):
        if len(row) > 1 and row[0][:30] == strmax[:30]:
            for i in range(12):
                tmpmax.append(float(row[i + 1]))
        if len(row) > 1 and row[0][:30] == strmin[:30]:
            for i in range(12):
                tmpmin.append(float(row[i + 1]))
        if len(tmpmax) and len(tmpmin):
            break
mintemp = int(min(tmpmin))
maxtemp = int(max(tmpmax))
avgmin = (tmpmin[0] + tmpmin[11]) / 2
avgmax = (tmpmax[0] + tmpmax[11]) / 2
tmpmin.appendleft(avgmin)
tmpmin.append(avgmin)
tmpmax.appendleft(avgmax)
tmpmax.append(avgmax)
x = [0.5]
for i in range(12):
    x.append(i + 1)
x.append(12.5)
fig = plt.figure(figsize=(5, 3.5))
plt.title("Mean min and max temperatures in Sydney", fontsize=10)
plt.grid(b=True, ls="dotted")
plt.axis([0.5, 12.5, mintemp - 1, maxtemp + 1])
plt.plot(x, tmpmin, "b-")
plt.plot(x, tmpmax, "r-")
plt.fill_between(x, tmpmin, tmpmax, color="grey", alpha="0.1")
xtk = [(i + 1) for i in range(12)]
plt.xticks(xtk, month_name[1:13], fontsize=8)
fig.autofmt_xdate(rotation=30)
ytk = []
i = mintemp
while i <= maxtemp:
    ytk.append(i)
    i += 0.5
plt.yticks(ytk, fontsize=4)
plt.show()
