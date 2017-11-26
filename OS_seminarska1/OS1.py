
# uvozi naslednje knjiznice
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from plotly import plotly

plt.style.use('fivethirtyeight')

# file locations ~/Desktop/OS/seminarska1/paketi.csv
# preberi podatke v podatkovni okvir

df = pd.read_csv("~/Desktop/OS/seminarska1/paketi.csv", encoding="utf-8")

# Tole je prvih pet vrstic podatkovnega okvirja
print(df.head(5))
# Tole so kategorije telekomunikacijskih paketov
print(list(df.columns))
# Tole so variante oziroma telekomunikacijski paketi, ki jih ponujajo ponudniki
print(df[df.columns[0]])


### NEKJE TUKAJ VRŽI ŠE SLIKO DREVESA KRITERIJEV

# Uredimo podatkovni okvir.
# Vrsticam dam imena prvega stolpca in odstranim prvi stolpec (torej imena paketov)
# Odstranim ceno naročnine za prvo leto, saj je všteta skupaj z naročnino drugega leta v ceno paketa za dve leti
# Naročnino drugega leta pustim, saj je to cena, ki jo bomo nato redno plačevali, če se ne odločimo menjati paketa oziroma lahko
# bi jo tudi odstranil, saj obstaja možnost, da bodo čez dve leti boljši paketi in bomo ponovno vezali za novo leto nek nov paket.
df.index = df['Paket']
print(df.index)
# spustimo prva dva stolpca - ime paketa in prvo letno naročnino
df = df.iloc[:, 2:]

# popravi tudi INF inf na neko številko, ki bo gotovo največja
df = df.replace('inf', 10000)
print(df.head(5))

# Tole so postopki, da pretvorim vrednosti v koristnosti !

## Cena (redna mesecna)
def cena_redna(val):
    # max cena je 0
    #min cena je 100
    if val == max(df['Cena (redna mesecna)']):
        return 0
    if val == min(df['Cena (redna mesecna)']):
        return 100
    #lin funkcija
    k = (0-100)/(max(df['Cena (redna mesecna)']) - min(df['Cena (redna mesecna)']))
    # n je konst, ki jo morma pristeti, da pridem na pravo linijo
    n = abs(k*max(df['Cena (redna mesecna)'])) # tole bo negativno, moram dati +, in pristeti... da bi bila max vrednost res 0
    return k * val + n

## Cena vezava dve leti
def cena_vsa(val):
    # max cena je 0
    # min cena je 100
    if val == max(df['Cena vezava dve leti']):
        return 0
    if val == min(df['Cena vezava dve leti']):
        return 100
    # lin funkcija
    k = (0 - 100) / (max(df['Cena vezava dve leti']) - min(df['Cena vezava dve leti']))
    n = abs(k * max(df['Cena vezava dve leti']))
    return k * val + n

## Internet (dol)
def intG(val):
    # max hitrost 100
    # min hitrost 0
    if val == max(df['Internet (dol)']):
        return 100
    if val == min(df['Internet (dol)']):
        return 0

    # od 100 Mbit naprej mi ni več tako pomembno
    if val >= 100:
        # lin funkcija  za vrednosti od 100 naprej
        # y2 - y1 / x2 - x1
        k1 = (100 - 80) / (max(df['Internet (dol)']) - 100)
        # +70, ker je k = 1/10 in 100 = 1/10 * 300 + n ; n = 100 - 30 = 70
        return k1 * val + 70
    else:
        #prvi del lin funkcija do 100
        k2 = (80 - 0) / (100 - min(df['Internet (dol)']))
        # min*k + n = 0
        # n = -min*k
        return k2 * val - (min(df['Internet (dol)']))*k2

## Internet (gor)
def intD(val):
    # max hitrost 100
    # min hitrost 0
    if val == max(df['Internet (gor)']):
        return 100
    if val == min(df['Internet (gor)']):
        return 0

    # od 10 Mbit naprej mi ni več tako pomembno za upload
    if val >= 10:
        # lin funkcija  za vrednosti od 100 naprej
        # y2 - y1 / x2 - x1
        k1 = (100 - 80) / (max(df['Internet (gor)']) - 10)
        #n
        n = 100 - k1 * max(df['Internet (gor)'])
        return k1 * val + n
    else:
        #prvi del lin funkcija do 10
        k2 = (80 - 0) / (10 - min(df['Internet (gor)']))
        # min*k + n = 0
        # n = -min*k
        return k2 * val - (min(df['Internet (gor)']))*k2

## TV programi
def tvP(val):
    maks = max(df['TV programi'])
    mini = min(df['TV programi'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0)/(maks - mini)
    return k*val - mini*k

## TV Zamik
def tvZ(val):
    if val == 'Da':
        return 100
    else:
        return 0

## Mobitel(enote/min)
def mobiMin(val):
    maks = max(df['Mobitel(enote/min)'])
    mini = min(df['Mobitel(enote/min)'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0) / (maks - mini)
    return k * val - mini * k

## Mobitel(enote/prenos)
def mobiP(val):
    maks = max(df['Mobitel(enote/prenos)'])
    mini = min(df['Mobitel(enote/prenos)'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0) / (maks - mini)
    return k * val - mini * k

## Mobitel(enote/sms)
def mobiSms(val):
    maks = max(df['Mobitel(enote/sms)'])
    mini = min(df['Mobitel(enote/sms)'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0) / (maks - mini)
    return k * val - mini * k

## Telefonija (enote/min)
def telefon(val):
    maks = max(df['Telefonija (enote/min)'])
    mini = min(df['Telefonija (enote/min)'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0) / (maks - mini)
    return k * val - mini * k

## HBO (vključen)
def hbo(val):
    if val == 'Da':
        return 100
    else:
        return 0

## HD programi
def hd(val):
    maks = max(df['HD programi'])
    mini = min(df['HD programi'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0) / (maks - mini)
    return k * val - mini * k

## Oblak(GB)
def oblak(val):
    maks = max(df['Oblak(GB)'])
    mini = min(df['Oblak(GB)'])
    if val == maks:
        return 100
    if val == mini:
        return 0

    # min * k + n = 0
    # n = -min*k
    k = (100 - 0) / (maks - mini)
    return k * val - mini * k

## Poljuben Dodaten Programski Paket
def extra(val):
    if val == 1:
        return 100
    else:
        return 0



# SPREMENIMO VREDNOSTI KRITERIJEV V KORISTNOST, damo na skupno skalo

funkcije = [cena_redna, cena_vsa, intG, intD, tvP, tvZ, mobiMin, mobiP, mobiSms, telefon, hbo, hd, oblak, extra]

# skopiramo v nov podatkovni okvir
dfKorist = df.copy()
indeks = 0
for stolpec in dfKorist.columns:
    dfKorist[stolpec] = dfKorist[stolpec].apply(funkcije[indeks])
    indeks += 1



# IZLOČIMO MANJVREDNE VARIANTE

# Tole je funkcija, ki odstrani manjvredne variante
## Varianta A je manjvredna od B, ko je varianta B vsaj boljsa v eni kategoriji v ostalih pa enaka
## Manjvredne variante odstranimo, saj jih ne bi v nobenem primeru nikoli izbrali
## Zapomni si, da so imena paketov v prvem stolpcu !!!! Popravi indekse
def odstraniManjvredne(df):
    nrow, ncol = df.shape
    manjvredne = set()

    #izberemo prvo vrstico
    for row1 in range(nrow):
        #izberemo drugo vrstico
        for row2 in range(row1+1, nrow):
            #odstejemo od prve izbrane, drugo izbrano in dobimo vektor razlik
            vektorRazlik = df.iloc[row1] - df.iloc[row2]
            #če naslednji pogoj velja sum(vektorRazlik < 0) != 0 and sum(vektorRazlik > 0) != 0
            #pomeni da ima vektor razlik neg in poz vrednosti kar ni OK, če je ena varianta boljsa od druge je vektor ali
            #cel neg ali cel poz :)
            #negiramo torej ta izraz, dodati moramo se pogoj da ne smejo biti vsi 0
            if not(sum(vektorRazlik < 0) != 0 and sum(vektorRazlik > 0) != 0) and sum(vektorRazlik == 0):
                #če smo tukaj notri je vektor ali cel poz ali cel neg
                #če je cel poz, pomeni da je row1 boljša od row2, pomeni da dodamo row2
                if sum(vektorRazlik) > 0:
                    #dodaj ime paketa, ki je manj vreden
                    manjvredne.add(df.index[row2])
                else:
                    manjvredne.add(df.index[row1])
    # vrni podatkovni okvir brez manjvrednih in manjvredne - imena
    for varianta in manjvredne:
        df = df.loc[df.index != varianta, :]
    return (df, manjvredne)


dfKorist, tt = odstraniManjvredne(dfKorist)


print("Manjvredne variante", tt)
print("Data, prtvorjena v koristnosti, brez manjvrednih", dfKorist)
# fig, ax = plt.subplots()

# UTEŽI , nastavi uteži kriterijem glede na hierarhično drevo
# nastavitev glede na drevo in ročno


# PRVI NIVO

#cena
rednaCena = 0.3
cena2leti = 0.7

#internet
dol = 0.7
gor = 0.2
cloud = 0.1

#gsm
mobiM = 0.3
mobiS = 0.3
mobiPaketi = 0.4

#tv paketi
hb = 0.65
hdd = 0.3
extr = 0.05

# DRUGI NIVO

#televizija
programi = 0.3
zamik = 0.4
paketi = 0.3

#telefonija
gsm = 0.9
stacionarni = 0.1

# TRETJI NIVO
inter = 0.7
teve = 0.2
telefonija = 0.1

# CETRTI NIVO
telek = 0.4
c = 0.6

# Uteži so bile nastavljene glede na drevo. Prvo sem nastavil uteži od spodaj gor, nato pa zmnožil po vejah nazaj dol, da sem dobil dejanske vrednosti

imena = ["redna cena", "vezava dve leti", "internet dol hitrost", "internet gor hitrost", "število programov", "časovni zamik", "mobi minute", "mobi paketi",
         "mobi sms", "stacionarni telefon", "HBO", "HD", "oblak", "dodatni paket"]
utezi = [c*rednaCena, c*cena2leti, telek*inter*dol, telek*inter*gor, telek*teve*programi, telek*teve*zamik,
         telek*telefonija*gsm*mobiM, telek*telefonija*gsm*mobiPaketi, telek*telefonija*gsm*mobiS, telek*telefonija*stacionarni,
        telek*teve*paketi*hb, telek*teve*paketi*hdd, telek*inter*cloud, telek*teve*paketi*extr]

print("Uteži", utezi)
print("Vsota uteži mora biti ena:", sum(utezi))

for x in range(len(imena)):
    print(imena[x], "utežitev %.5f" % (utezi[x]))




## UTEŽENO TOČKOVANJE

def weight_score(varianta, weight):
    score = 0
    for i in range(len(varianta)):
        score += varianta[i]*weight[i]
    return score

def ocene_variant(dataf, weight):
    tocke = []
    i = 0
    for varianta in dataf.index:
        score = weight_score(dataf.loc[varianta], weight)
        tocke.append((varianta, score))
        i+=1
    return tocke


tocke = ocene_variant(dfKorist, utezi)
# UREDI OD MAX DO MIN
tocke = sorted(tocke, key=lambda x: x[1], reverse=True)
for varianta, t in tocke:
    print("varianta:",varianta, "tocke:",t)




###### GRAFI ######
###### GRAFI ######

# prvi graf, narisi graf variant

# drugi graf, narisi barplot tockovanj, kdo je zmagal


####################
####################
####################

# NAJBOLJŠA IN ALTERNATIVA
# najboljsa je A1 kombo S
# alternativa je Oranžni Optimum
top = dfKorist.loc['A1 kombo S']
alt = dfKorist.loc['Oranžni Optimum']

fig, ax = plt.subplots()

x1 = np.arange(len(top))
y1 = top
x2 = np.arange(len(alt))
y2 = alt
ax.plot(x1, y1, "g", alpha = 0.8, label="Top - A1 kombo S", linestyle="-", marker = "o", markersize=10, linewidth=2)
ax.plot(x2, y2, "r", alpha = 0.8, label="Alt - T2 Optimum", linestyle="-", marker = "o", markersize=10, linewidth=2)
ax.set_title("Top varianta in alternativa")
ax.set_xticks(x2)
ax.set_ylabel("Koristnost")
ax.set_xlabel("Kriterij")
ax.set_xticklabels(dfKorist.columns, rotation=10, size=6)
ax.legend(loc=1)
#plt.show()

# PRIMERJAVA VARIANT Z NAJBOLJŠO
#y1 so vrednosti za najboljso varianto
ostale_notTop = [x[0] for x in tocke[1:]]


for varianta in ostale_notTop:
    fig, ax = plt.subplots()
    ax.bar(x1, y1, color="green", alpha=0.8, label="TOP - A1 kombo S")
    y = dfKorist.loc[varianta]
    x = np.arange(len(y))
    #ax.fill_between(x, y, y1, where=y>=y1, alpha=0.8, color=barva)
    ax.bar(x, y, color="blue", alpha=0.8, label=varianta)
    ax.set_title("Top vs %s" % (varianta))
    ax.set_xticks(x)
    ax.set_ylabel("Koristnost")
    ax.set_xlabel("Kriterij")
    ax.set_xticklabels(dfKorist.columns, rotation=10, size=6)
    ax.legend(loc=1)
#plt.show()

# PRIMERJAVA VARIANT Z NAJSLABŠO
najslabsa = tocke[-1][0]

ostale_notTop = [x[0] for x in tocke[:-1]]

y1 = dfKorist.loc[najslabsa]
x1 = np.arange((len(y1)))

for varianta in ostale_notTop:
    fig, ax = plt.subplots()
    ax.bar(x1, y1, color="red", alpha=0.8, label=najslabsa)
    y = dfKorist.loc[varianta]
    x = np.arange(len(y))
    #ax.fill_between(x, y, y1, where=y>=y1, alpha=0.8, color=barva)
    ax.bar(x, y, color="cyan", alpha=0.8, label=varianta)
    ax.set_title("Najslabša vs %s" % (varianta))
    ax.set_xticks(x)
    ax.set_ylabel("Koristnost")
    ax.set_xlabel("Kriterij")
    ax.set_xticklabels(dfKorist.columns, rotation=10, size=6)
    ax.legend(loc=1)

#plt.show()


### # MAAAAAP

def weight_score2(varianta, weight):
    cena = 0
    lastnost = 0
    for i in range(len(varianta)):
        # to je cena
        if i < 2:
            cena += varianta[i]*weight[i]
        else:
            lastnost += varianta[i]*weight[i]
    return (cena, lastnost)

x_cena = []
y_lastnost = []
imena = dfKorist.index
for varianta in dfKorist.index:
    x,y = weight_score2(dfKorist.loc[varianta], utezi)
    x_cena.append(x)
    y_lastnost.append(y)

fig, ax = plt.subplots()
ax.scatter(x_cena, y_lastnost, color="red", s=30)
i = 0
for ime in imena:
    ax.annotate("(%s)"%ime, xy = (x_cena[i], y_lastnost[i]), textcoords='data', size=10)
    i+=1

# narisi se ovojnico
# linija ki povezuje zunanje
linija_x = []
linija_y = []
for i in range(len(imena)):
    if imena[i] == "Oranžni Diamant HBO":
        linija_x.append(0)
        linija_y.append(y_lastnost[i])
        linija_x.append(x_cena[i])
        linija_y.append(y_lastnost[i])
    if imena[i] == "Oranžni Optimum" or imena[i] == "A1 kombo S":
        linija_x.append(x_cena[i])
        linija_y.append(y_lastnost[i])


ax.plot(linija_x, linija_y, color="blue", alpha=0.7, linestyle="-", linewidth=2)
ax.fill_between(linija_x, linija_y, 0, color="blue", alpha=0.3)

ax.set_title("MAP koristnost - telekomunikacija vs cena")
ax.set_ylabel("Telekomunikacije")
ax.set_xlabel("Cena")
#plt.show()



## SENZITIVNOST
## Za analizo občutljivosti preverimo občutljivost modela na spremembe uteži.
#  Torej, direktno odgovarja na vprašanje: ali bi
# majhna sprememba uteži bistveno vplivala na naš odločitven model?

# nastavimo c in jo spreminjamo
variabilna_utez_cena = np.linspace(0, 1, 40)
slovar = {}
for c in variabilna_utez_cena:
    # ostalo utez dobimo tako da 1 - c
    telek = 1 - c
    utezi_tmp = [c*rednaCena, c*cena2leti, telek*inter*dol, telek*inter*gor, telek*teve*programi, telek*teve*zamik,
            telek*telefonija*gsm*mobiM, telek*telefonija*gsm*mobiPaketi, telek*telefonija*gsm*mobiS, telek*telefonija*stacionarni,
            telek*teve*paketi*hb, telek*teve*paketi*hdd, telek*inter*cloud, telek*teve*paketi*extr]


    # sedaj v vsaki iteraciji spremenimo utez ceni in nato popravimo vse utezi
    # v spodnji zanki gremo cez vse iteracije in jim izracunamo tocke glede na utezi
    for varianta in dfKorist.index:
        utility = weight_score(dfKorist.loc[varianta], utezi_tmp)
        if varianta not in slovar:
            slovar[varianta] = [(c, utility)]
        else:
            slovar[varianta].append((c, utility))


# NARISI GRAF SENZITIVNOSTI


fig, ax = plt.subplots()
for varianta in slovar:
    xi = [xy[0] for xy in slovar[varianta]]
    yi = [xy[1] for xy in slovar[varianta]]
    ax.plot(xi, yi, linestyle="--", linewidth=1, label=varianta)
    ax.set_xlabel("Cena Utež")
    ax.set_ylabel("Koristnost")
    ax.set_title("Senzitivnost modela")
    #ax.set_xticks(xi)
    ax.legend(loc=1)
#plt.show()

# IN SE MALENKOST BOLJ REDEK
fig, ax = plt.subplots()
for varianta in slovar:
    if varianta == "T3 giga" or varianta == "Top Trio C" or varianta == "Oranžni Diamant HBO" or varianta == "A1 kombo S" or varianta == "Oranžni Optimum" or varianta == "A1 kombo L":
        xi = [xy[0] for xy in slovar[varianta]]
        yi = [xy[1] for xy in slovar[varianta]]
        ax.plot(xi, yi, linestyle="-", linewidth=2, label=varianta)
        ax.set_xlabel("Cena Utež")
        ax.set_ylabel("Koristnost")
        ax.set_title("Senzitivnost modela")
        #ax.set_xticks(xi)
        ax.legend(loc=1)




### KAJ ČE
### za koliko bi se moral poceniti Oranžni optimum, da bi postal absolutni zmagovalec ???
"""
varianta: A1 kombo S tocke: 61.7422222222
varianta: Top Trio Start tocke: 59.8584474632
varianta: Oranžni Optimum tocke: 59.3258198182
"""

# Koliko mora biti redna cena nizja, da se nam splaca?
# treba je dodati, da če manjšamo redno ceno, se manjša tudi dvo letna cena, saj je polovico nje redna cena
# popravljaš tako, da vsako zmanjšanje v redni ceni - > dvoletna cena - 12*zmanjšanje_redne_cene

#to so koristnosti !!
vrsticaOOT = dfKorist.loc['Oranžni Optimum']
#redna cena, start, konec, koliko tock
price_movement = np.linspace(vrsticaOOT[0], 0, 30)
prejsnja_redna = df.loc['Oranžni Optimum', "Cena (redna mesecna)"]
dveLeti_cena = df.loc['Oranžni Optimum', "Cena vezava dve leti"]
for price in price_movement:
    redna_cena = price
    dveLeti_cena = dveLeti_cena - 12*(prejsnja_redna-redna_cena)

    #nastavim prejsnjo redno na prejsno vrednost
    prejsnja_redna = redna_cena
    # updejtam vrstico, da jo posljem v izracun
    tmp_vrstica = vrsticaOOT.copy()
    # moramo cene pretvoriti v koristnosti
    tmp_vrstica[0] = cena_redna(redna_cena)
    tmp_vrstica[1] = cena_vsa(dveLeti_cena)
    tocke = weight_score(tmp_vrstica, utezi)

    if tocke > 61.7422222222:
        print("TOČKE", tocke, ". Za toliko bi se morala zmanjsati redna cena, "
                              "da bi bil Oranžni Optimum najboljša izbira:", df.loc['Oranžni Optimum', "Cena (redna mesecna)"] - redna_cena,
                            "cena akcija:", redna_cena, ", cena regular:", df.loc['Oranžni Optimum', "Cena (redna mesecna)"],
                            "Toliksna bi bila celotna cena za dve leti: ", dveLeti_cena)
        break


### NARISI ZVEZDAST GRAF

theta = np.linspace(0, 2*np.pi-0.08, len(dfKorist.columns))
vrednosti = dfKorist.loc['Oranžni Optimum']
vrednosti1 = dfKorist.loc['A1 kombo S']
vrednosti2 = dfKorist.loc['Oranžni Diamant HBO']
vrednosti3 = dfKorist.loc['T3 giga']

ax = plt.subplot(111, projection='polar')
ax.fill_between(theta, vrednosti, 0, label='Oranžni Optimum', alpha = 0.7, color="blue")
ax.fill_between(theta, vrednosti1, 0, label='A1 kombo S', alpha = 0.7, color="cyan")
ax.fill_between(theta, vrednosti2, 0, label='Oranžni Diamant HBO', alpha = 0.7, color="red")
ax.fill_between(theta, vrednosti3, 0, label='T3 giga', alpha = 0.7, color="orange")
ax.set_title("Prikaz bolj robnih primerov - koristnost")
ax.set_xticks(theta)
ax.set_xticklabels(dfKorist.columns, size=7)
ax.legend(bbox_to_anchor=(0, 1.2))
#plt.show()