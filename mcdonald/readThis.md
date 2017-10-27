# Hitri pregled artiklov na McDonald's meniju

Na hitro sem skočil v podatke, ki jih najdete na naslednjem linku (ali pa na tem repozitoriju): [klikni tukaj](https://www.kaggle.com/mcdonalds/nutrition-facts)

Hitri fun fact #1 : Največ holesterola imata naslednja dva izdelka - big breakfast with hotcakes, eden z
velikim biskvitom, drugi z navadnim. Imata 575 mg holesterola, kar predstavlja 192% dnevno vrednost.

Hitri fun fact #2 : Največ sladkorja ima McFlurry z M&M (srednja velikost). Ima 128 gramov sladkorja.

## Sladkor

![Sladkor v izdelkih](https://github.com/jonchisko/data-is-beautiful/blob/master/mcdonald/Screen%20Shot%202017-10-22%20at%2022.52.58.png)

Vidimo, da imajo izdelki kar veliko sladkorja. Mediana je izdelek, ki ima okoli 20 gramov sladkorja, medtem ko je povprečna 
količina sladkorja v izdelkih na meniju okoli 30 gramov sladkorja. To je že zelo blizu priporočenemu dnevnemu vnosu.
Delež artiklov, ki so nad priporočljivim vnosom sladkorja (40 gramov) je 34.23%.

## Hitra in enostavna ocenitev artiklov

![TOP 10 izbira](https://github.com/jonchisko/data-is-beautiful/blob/master/mcdonald/Screen%20Shot%202017-10-23%20at%2023.10.03.png)

![FLOP 10 izbira](https://github.com/jonchisko/data-is-beautiful/blob/master/mcdonald/Screen%20Shot%202017-10-23%20at%2023.16.53.png)

Uporabil sem enostavne funkcije, ki so pretvorile vrednosti na interval med 0 in 100. Nato sem utežil kriterije oziroma atribute, poudarek je bil na holesterolu, kalorijah, C in A vitaminu, kalciju, železu in trans maščobah.
Izvedel sem uteženo vsoto in pridobil zgornje rezultate, ki niso tako presenetljivi.






