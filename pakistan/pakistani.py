"""

Podatki so dostopni na naslednjem url: https://www.kaggle.com/zusmani/pakistandroneattacks/data

Napadi ameriških brezpilotnih letal v pakistanskem zračnem prostoru od leta 2004 do oktobra 2017.

Podatkovna zbirka vsebuje detajlno informacijo o 397 napadih, ki so ubili približno 3558 in poškodovali 1333 ljudi, vključno z 2539 civilisti.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math


df = pd.read_csv("/Users/jonskoberne/PycharmProjects/dataExplore/PakistanDroneAttacksWithTemp Ver 10 (October 19, 2017).csv.xls", encoding='latin1')


vrstice, stolpci = df.shape
print("Data ima %d vrstic in %d stolpcev" % (vrstice, stolpci))
print("Torej imamo %d napadov." % vrstice)
stolpci_imena = list(df.columns)
print("Katere atribute imamo:", stolpci_imena[:stolpci//2],"\n", stolpci_imena[stolpci//2:])



#ohrani le vrstice, ki imajo znano vrednost in obdrži le stolpce, ki jih potrebujemo date 'Al-Qaeda', 'Taliban', 'Civilians Min', 'Civilians Max', 'Foreigners Min'
#'Foreigners Max', 'Total Died Min', 'Total Died Mix', 'Injured Min', 'Injured Max',
atributi = ['Al-Qaeda', 'Taliban', 'Civilians Min', 'Civilians Max', 'Foreigners Min', 'Foreigners Max', 'Total Died Min', 'Total Died Mix',
            'Injured Min', 'Injured Max', 'Women/Children']

df2 = df.loc[np.logical_not(df["Date"].isnull()), ['S#', 'Date', 'Time', 'Location', 'City', 'Province', 'No of Strike', 'Al-Qaeda', 'Taliban', 'Civilians Min',
                                                   'Civilians Max', 'Foreigners Min', 'Foreigners Max', 'Total Died Min', 'Total Died Mix', 'Injured Min',
                                                   'Injured Max', 'Women/Children', 'Special Mention (Site)', 'Comments',
                                                   'References', 'Longitude', 'Latitude', 'Temperature(C)', 'Temperature(F)']]


#Podatkovna zbirka ima kar nekaj Nanov, ki jih bomo nastavili kot nič in plotali ...



for attr in atributi:
    #vrstice kjer je ta attr null in stolpec tega attr nastavimo na 0
    df2.loc[df2[attr].isnull(), attr] = 0
    #negativne vrednosti tudi odstranimo za začetek
    df2.loc[df2[attr] < 0, attr] = 0

# Narišimo prvo gibanje števila smrti preko vseh let
fig, ax = plt.subplots(figsize=(20,10))
#Vzamemo le tiste vrstice, kjer je Died Mix oziroma max neenak nič, da lepše izrišemo :)
smrtiMin = df2.loc[df2["Total Died Mix"] != 0, "Total Died Min"]
smrtiMax = df2.loc[df2["Total Died Mix"] != 0, "Total Died Mix"]
datumi = df2.loc[df2["Total Died Mix"] != 0, "Date"]
avgDeath = smrtiMin + (smrtiMax - smrtiMin)/2

ticks = np.arange(len(datumi))
#poglejmo se trend smrti
coefTrenda = np.polyfit(ticks, np.array(smrtiMax, dtype="float"), 4)
funkcijaTrenda = np.poly1d(coefTrenda)
ax.bar(ticks, avgDeath, align="center", color="blue", alpha=0.8, label="Average number of deaths")
ax.bar(ticks, smrtiMax-avgDeath, align="center", color="cornflowerblue", alpha=0.7, bottom=avgDeath, label="High estimate")
ax.plot(ticks, funkcijaTrenda(ticks), color="red", alpha=0.8, label="Trend Line")
ax.set_title("Number of deaths in Pakistan (drone attacks)")
#dejansko hocemo na x label le 10 datumov
indeksi = np.arange(0, len(ticks), len(ticks)//10)
ax.set_xticks(indeksi)
ax.set_xticklabels(datumi[indeksi], rotation=20)
ax.set_ylabel("Number of deaths")
ax.set_xlabel("Date")
ax.legend(loc=1)
#plt.show()

print("Največ smrtnih žrtev v napadu",df2['Total Died Mix'].max(),"\nNa dan:", df2.loc[df2["Total Died Mix"] == df2["Total Died Mix"].max(), "Date"])



"""

Naloga:
 1) Poglej kako se je gibalo število smrti po urah :)
 2) Probaj izrisati situacijo na zemljevidu, torej število smrti v napadu je nek atribut, x in y pa sta geografska dolžina in širina
"""
import time

ure = df2.loc[np.logical_not(df2["Time"].isnull()), "Time"]

mnozica_ur = set(ure)
from collections import defaultdict
slovar1 = defaultdict(int)
slovar2 = defaultdict(int)
for ura in mnozica_ur:
    pyUra = time.strptime(ura, "%H:%M")
    slovar1[pyUra] += df2.loc[df2["Time"] == ura, "Total Died Min"].sum()
    slovar2[pyUra] += df2.loc[df2["Time"] == ura, "Total Died Mix"].sum()

from collections import _itemgetter

#uredim po uri
minimalne = sorted(slovar1.items(), key=_itemgetter(0))
maksimalne = sorted(slovar2.items(), key=_itemgetter(0))

ura = []
minz = []
maxz = []
for indeks in range(len(minimalne)):
    ura.append(time.strftime("%H:%M", minimalne[indeks][0]))
    minz.append(minimalne[indeks][1])
    maxz.append(maksimalne[indeks][1])

minz = np.array(minz, dtype="int")
maxz = np.array(maxz, dtype="int")

fig, ax = plt.subplots(figsize=(20,10))
ticks = np.arange(len(ura))
avgDeath = minz + (maxz - minz)/2

#fitajmo še trend (:
trendCoef = np.polyfit(ticks, avgDeath, 6)
trendFun = np.poly1d(trendCoef)

ax.plot(ticks, avgDeath, color="red", alpha=0.9, linewidth=2, label="Average number of deaths")
ax.fill_between(ticks, minz, maxz, color="pink", alpha=0.7, label="Delta between max and min estimates")
ax.plot(ticks, trendFun(ticks), color="cornflowerblue", alpha=0.6, label="Trend")
ax.set_title("Deaths by hour")
ax.set_xticks(ticks)
ax.set_xticklabels(ura, rotation=90)
ax.set_xlabel("Time of day")
ax.set_ylabel("Number of deaths")
ax.legend(loc=1)
#plt.show()


"""
Se geografski grafi, something new for me :o
"""

from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

#Longitude Latitude

#long in lat ne smeta bit nan
selekcija = np.logical_and(np.logical_and(np.logical_not(df2["Latitude"].isnull()), np.logical_not(df2["Longitude"].isnull())), df2["Total Died Mix"] != 0)
lati = df2.loc[selekcija, "Latitude"]
longi = df2.loc[selekcija, "Longitude"]
died = df2.loc[selekcija, "Total Died Mix"]


map_options = GMapOptions(lat=30.29, lng=69.73, map_type="roadmap", zoom=6)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options
)
plot.title.text = "Pakistan"


plot.api_key = "api google"

source = ColumnDataSource(
    data=dict(
        lat=lati,
        lon=longi,
        velikost=died
    )
)

circle = Circle(x="lon", y="lat", size="velikost", fill_color="red", fill_alpha=0.9, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
#show(plot)

#####
#####
#
#####
#####
print(df2["Date"][-2:])

alkaida = df2["Al-Qaeda"].sum()
talibani = df2["Taliban"].sum()
civilMin = df2['Civilians Min'].sum()
civilMax = df2['Civilians Max'].sum()
fMin = df2['Foreigners Min'].sum()
fMax = df2['Foreigners Max'].sum()
totalMin = df2["Total Died Min"].sum()
totalMax = df2["Total Died Mix"].sum()
womenChild = df2["Women/Children"].sum()
print(alkaida, talibani, civilMax, civilMin, fMax, fMin, totalMin, totalMax, womenChild)
civilAvg = (civilMax+civilMin)/2
fAvg = (fMax + fMin)/2
totalAvg = (totalMax + totalMin)/2
seznamcek = [womenChild, alkaida, fAvg, talibani, civilAvg, totalAvg]
names = ["Women/Children", "Al-Qaeda", "Foreigner", "Taliban", "Civilian", "Total"]
fig, ax = plt.subplots(figsize=(20,10))

#narisimo se mine in max za tiste 3 :) ... prvo narisemo maxe, da potem cez narisemo dejanske vrednosti -> pride polna barva do izraza
ax.barh(4, civilMax, color="cornflowerblue", alpha=0.5, label="max")
ax.barh(2, fMax, color="cornflowerblue", alpha=0.5)
ax.barh(5, totalMax, color="cornflowerblue", alpha=0.5)

ax.barh(np.arange(len(seznamcek)), seznamcek, color="blue", alpha=1, label="average or exact value")
#narisimo se mine in max za tiste 3 :)
ax.barh(4, civilMin, color="m", alpha=1, label="min value")

ax.barh(2, fMin, color="m", alpha=1)

ax.barh(5, totalMin, color="m", alpha=1)
ax.set_yticks(np.arange(len(names)))
ax.set_yticklabels(names)
ax.set_xlabel("Number of deaths")
ax.set_ylabel("Group")
ax.set_title("Number of deaths by group [2004-2017]")
plt.gca().invert_yaxis()
ax.legend(loc=1)
plt.show()