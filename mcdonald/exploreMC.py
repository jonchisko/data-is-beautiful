import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


"""
######
Analiza McDonald's menija
######
"""
plt.style.use('fivethirtyeight')

df = pd.read_csv("./menu.csv")
stolpci = list(df.columns)
for x in stolpci:
    print(x)


#Iščemo artikel, ki ima največ holesterola.
maxCh = df["Cholesterol"].max()
maxChole = df[df["Cholesterol"] == maxCh]
print("Holesterol je %d  (dnevna vrednost %s) in to je item\n %s" % (maxCh,list(maxChole["Cholesterol (% Daily Value)"])[0], maxChole["Item"]))

#Iščemo artikel, ki ima največ sladkorja
maxSug = df["Sugars"].max()
maxSugars = df[df["Sugars"] == maxSug]
print("Sladkor je %d g in to je item\n %s" % ( maxSug, maxSugars["Item"]))

urejenCukr = np.array(sorted(df["Sugars"]))
medianaCukrID = len(urejenCukr)//2
barlist = plt.bar(range(len(df)), urejenCukr, color="greenyellow")
avg = np.mean(df["Sugars"])
plt.plot([0, len(df)], [avg, avg], color="red", label="average")
plt.plot([0, len(df)], [40, 40], color="violet", label="Maximum daily")
#pobarvam nad avg z drugacnim odtenkom
barlist[medianaCukrID].set_color("r")
plt.text(120, 20, "Mediana", size="5")
cukrNadAvg = urejenCukr > avg
for x in np.nonzero(cukrNadAvg)[0]:
    barlist[x].set_color("m")
for x in np.nonzero(urejenCukr > 40)[0]:
    barlist[x].set_color("mediumvioletred")
plt.legend(loc=1)
plt.title("Sugar McDonald's")
plt.ylabel("Sugar [g]")
plt.xlabel("Item")
plt.show()

#koliko izdelkov je nad recommended sugar intake
delezCukr = sum(urejenCukr > 40)/len(df)
print("Tolikšen je delež artiklov, ki so nad priporočljivim vnosom sladkorja (40 gramov) %.2f%%" %(delezCukr*100))

"""
1. Naloga
Najboljsa hrana? Pretvori na kvaliteto in poglej
- Izloči kategorijo, item, serving size, calories from fat, total fat, saturated fat, cholesterol, sodium, carbs, dietary fiber
- konvertiraj vse korektno v kvaliteto 
- izloči manjvredne variante
- uteži vsak kriterij
- izračunaj točke in najboljše variante

2. Naloga
Po kategorijah izdelkov poglej njihove nutricionisticne podatke:
- na plot naredi tako, da boš lahko primerjal vsako kategorijo in njihove mediane oziroma povprečne atribute

3. Naloga, ne vem če sploh
"""
#new data frame
ndf = df.iloc[:, [3,6,8,9,11,13,15,17,18,19,20,21,22,23]]
print("\nIzbrane kategorije: ", list(ndf.columns)[:5], "\n", list(ndf.columns)[5:])

def calFun(val):
    # Manj kalorij je bolje, maksimalne kalorija je 0
    maks = ndf["Calories"].max()
    minimal = ndf["Calories"].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return -100/(maks-minimal) * (val - maks)

def fatFun(val):
    # % daily value mascob
    maks = ndf['Total Fat (% Daily Value)'].max()
    minimal = ndf['Total Fat (% Daily Value)'].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return -100/(maks-minimal) * (val - maks)

def satFatFun(val):
    # % daily value saturated fat
    maks = ndf['Saturated Fat (% Daily Value)'].max()
    minimal = ndf['Saturated Fat (% Daily Value)'].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return -100/(maks-minimal) * (val - maks)

def transFatFun(val):
    #g trans fata ??
    maks = ndf['Trans Fat'].max()
    minimal = ndf["Trans Fat"].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return (-100/(maks-minimal)) * (val - maks)

def choleFun(val):
    maks = ndf['Cholesterol (% Daily Value)'].max()
    minimal = ndf['Cholesterol (% Daily Value)'].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return (-100/(maks-minimal)) * (val - maks)

def sodFun(val):
    maks = ndf['Sodium (% Daily Value)'].max()
    minimal = ndf['Sodium (% Daily Value)'].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return (-100/(maks-minimal)) * (val - maks)

def carbsFun(val):
    maks = ndf['Carbohydrates (% Daily Value)'].max()
    minimal = ndf['Carbohydrates (% Daily Value)'].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return (-100/(maks-minimal)) * (val - maks)

def fiberFun(val):
    maks = ndf['Dietary Fiber (% Daily Value)'].max()
    minimal = ndf['Dietary Fiber (% Daily Value)'].min()
    if val >= maks:
        return 100
    if val <= minimal:
        return 0
    else:
        return (100/(maks-minimal)) * (val-minimal)

def sugarFun(val):
    maks = ndf['Sugars'].max()
    minimal = ndf['Sugars'].min()
    if val >= maks:
        return 0
    if val <= minimal:
        return 100
    else:
        return (-100/(maks-minimal)) * (val - maks)

def proteinFun(val):
    maks = ndf['Protein'].max()
    minimal = ndf['Protein'].min()
    if val >= maks:
        return 100
    if val <= minimal:
        return 0
    else:
        return (100/(maks-minimal)) * (val-minimal)

def aFun(val):
    maks = ndf['Vitamin A (% Daily Value)'].max()
    minimal = ndf['Vitamin A (% Daily Value)'].min()
    if val >= maks:
        return 100
    if val <= minimal:
        return 0
    else:
        return (100/(maks-minimal)) * (val-minimal)

def cFun(val):
    maks = ndf['Vitamin C (% Daily Value)'].max()
    minimal = ndf['Vitamin C (% Daily Value)'].min()
    if val >= maks:
        return 100
    if val <= minimal:
        return 0
    else:
        return (100/(maks-minimal)) * (val-minimal)

def calciumFun(val):
    maks = ndf['Calcium (% Daily Value)'].max()
    minimal = ndf['Calcium (% Daily Value)'].min()
    if val >= maks:
        return 100
    if val <= minimal:
        return 0
    else:
        return (100/(maks-minimal)) * (val-minimal)

def ironFun(val):
    maks = ndf['Iron (% Daily Value)'].max()
    minimal = ndf['Iron (% Daily Value)'].min()
    if val >= maks:
        return 100
    if val <= minimal:
        return 0
    else:
        return (100/(maks-minimal)) * (val-minimal)



funkcije = [calFun, fatFun, satFatFun, transFatFun, choleFun, sodFun, carbsFun, fiberFun, sugarFun, proteinFun, aFun, cFun, calciumFun, ironFun]
ddf = ndf.copy()
for i, colName in enumerate(ndf.columns):
    ddf[colName] = ndf[colName].apply(funkcije[i])


#izracunaj score za vsako
#vektor utezi
#14
#weights = [100 for x in range(ddf.shape[1])]
weights = [100, 75, 70, 100, 90, 60, 40, 70, 80, 30, 80, 80, 80, 80]
slovarId = {}
for varianta in range(len(ddf)):
    score = sum(ddf.iloc[varianta, :] * weights) / sum(weights)
    slovarId[varianta] = score

import operator
urejeno = sorted(slovarId.items(), key=operator.itemgetter(1), reverse=True)
imenaIzdelkov = []
value = []
for id, val in urejeno:
    imenaIzdelkov.append(df["Item"][id])
    value.append(val)

fig, ax = plt.subplots(figsize=(20,10))
ax.barh(np.arange(len(imenaIzdelkov[:10])), value[:10], align="center", color="b", alpha=0.8)
ax.set_yticks(np.arange(len(imenaIzdelkov[:10])))
ax.set_yticklabels(np.arange(1,len(imenaIzdelkov[:10])+1))
for y, ime in enumerate(imenaIzdelkov[:10]):
   ax.text(2, y, ime, size=12)
ax.set_xlabel("Score")
ax.set_ylabel("Item")
ax.set_title("Scoring of items on the menu, top10")
plt.gca().invert_yaxis()
plt.show()

fig, ax = plt.subplots(figsize=(20,10))
CONST = 10
tiks = np.arange(len(imenaIzdelkov[-CONST:]))
imena = imenaIzdelkov[-CONST:]
vrednosti = value[-CONST:]
ax.barh(tiks, vrednosti, align="center", color="b", alpha=0.8)
ax.set_yticks(tiks)
ax.set_yticklabels(tiks+1)
for y, ime in enumerate(imena):
    ax.text(2, y, ime, size=12)
ax.set_title("Scoring of items on the menu, flop10")
ax.set_xlabel("Score")
ax.set_ylabel("Item")
plt.gca().invert_yaxis()
plt.show()


