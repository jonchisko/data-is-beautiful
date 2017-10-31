# Rdeče vino
Zelo na hitro, malo igranje s scipy modeli za učenje iz podatkov.
Nekaj stvari je malo na hitro, bolj zase kot, da bi nekdo lahko kaj uporabnega odkril (v tem tekstu hihi).

Vir podatkov: [klik](https://www.kaggle.com/danielpanizzo/wine-quality)

## Matrični graf atributi vs atributi
![Atributi](https://github.com/jonchisko/data-is-beautiful/blob/master/redWine/Screen%20Shot%202017-10-31%20at%2016.27.42.png)
Na zgornjem grafu lahko vidimo kateri atributi korelirajo medseboj.

## Porazdelitev kvalitet
![Kvaliteta](https://github.com/jonchisko/data-is-beautiful/blob/master/redWine/Screen%20Shot%202017-10-31%20at%2016.44.25.png)
## Ena korelacija
![Korelacija](https://github.com/jonchisko/data-is-beautiful/blob/master/redWine/korelacija.pdf)
Vidimo korelacijo med:
1) most acids involved with wine or fixed or nonvolatile (do not evaporate readily
2) density: the density of water is close to that of water depending on the percent alcohol and sugar content

## Učenje

Po preurejanju atributov na scalo med 0 in 1, sem uporabil SVM in nevronsko mrežo. Primerjal sem ju z večinskim klasifikatorjem,
rezultati pa so naslednji:
Večinski razred je 5
Večinski klasifikator, točnost: 0.431
SVM: 0.589
Nevronske: 0.628
