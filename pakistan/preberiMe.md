# Pakistan
Podatki, ki sem jih uporabil za tokratne grafe, lahko pridobite tukaj ali pa 
[tukaj](https://www.kaggle.com/zusmani/pakistandroneattacks/data).
Napadi ameriških brezpilotnih letal v pakistanskem zračnem prostoru od leta 2004 do oktobra 2017.
Podatkovna zbirka vsebuje podrobne informacije o 397 napadih, ki so ubili približno 3558 in poškodovali 1333 ljudi, 
vključno z 2539 civilisti.

![Uvodni graf](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2019.55.52.png)


## Na Zemljevidu

Spodnji graf prikazuje napade in njihovo inteziteto na zemljevidu.
![Map](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2019.20.54.png)
[Klik](http://htmlpreview.github.io/?https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/gmap_plot.html)

## Frekvenca napadov
Število napadov sem pregledal oziroma izrisal skozi celotno časovno obdobje. Na grafu je narisana maksimalna ocena smrtnih žrtev
in povprečno število smrtnih žrtev. Slednji podatek sem dobil tako, da sem povprečil maksimalno število smrtnih žrtev
in minimalno.
Na podatke sem nato "fital" polinom, ki nam prikazuje trend - vidimo, da se število žrtev počasi "zmanjšuje".

![graf1](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2019.20.28.png)
Podoben pristop sem naredil za naslednji graf, ki prikazuje število žrtev čez dan. Za vsako uro sem seštel število žrtev in to
naredil preko vseh let, ki so zajeta v podatkih.

![graf2](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2019.20.40.png)



## "graphs" that did not make the cut
Tale je identičen grafu, ki prikazuje število smrti skozi celotno obdobje. Razlika je, da je ta linija, ki je pobarvana pod sabo.
![graf1](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2023.51.45.png)
Akumulativno število smrti.
![graf2](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2023.51.53.png)
Več napadov združenih v en incident, da je x os krajša - torej časovni razpon.
![graf3](https://github.com/jonchisko/data-is-beautiful/blob/master/pakistan/Screen%20Shot%202017-10-27%20at%2023.52.16.png)
