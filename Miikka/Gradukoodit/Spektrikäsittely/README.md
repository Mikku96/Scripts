# HUOM! Tämä scripti ei toimi tässä julkaisussa, sillä osa tarvittavista aliohjelmista eivät ole vapaassa jaossa. 
## Rakensin pipe_process2_clened.py scriptin yhdistääkseni useamman spektridatan manipulointiin liittyvän työvaiheen.

Scriptit + skylines.txt.

VIS kansio sisältää pari tiedostoa, jos tahtoo testata. Tämä toimii myös mallina kansiorakenteelle.
Jos lataat siis tämän "Spektrikäsittely" kansion, toimii se pohjakansiona, minkä alla on VIS ja VIS_angs.
Pidä scriptit tässä pohjakansiossa.

# PIPELINE KÄYTTÖ
---

### Katso _pipe_process2_cleaned.py_ alusta kansiorakenne ohjeistus.

# Huomioi erityisesti tiedostojen vaaditut nimet (.fits ja .dat)

```
▶ python pipe_process2_cleaned.py {UVB,VIS,NIR} {yes,no} {w1} {w2} {step}
  Argumentit:
  {UVB,VIS,NIR}     Mille kaistalle tehdään prosessointi
  {yes,no}          Cleanataanko spektri? Toisinaan NIR kaistalla taisi tuhota liikaa spektriä.
  {w1}              Minimi aallonpituus
  {w2}              Maksimi aallonpituus
  {step}            Aallonpituus askel
  
  Scripti pyytää inputin:
  Strength: 0.1, Cut off: 0.7, stand. dev.: 5 (2 NIR:llä), median filter: 21
  Näitä käytin itse gradussa.
  
  Lopputuloksena pitäisi tulla output.dat, joka on yhdistetty spektri, sekä _processed.dat päätteiset tiedostot.
```
