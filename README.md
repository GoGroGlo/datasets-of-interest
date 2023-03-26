# Glo's Datasets of Interest
Some Python-based investigations about datasets I'm personally interested in.

Most of my notes are in Jupyter notebooks (.ipynb). The notes and datasets are included in every dataset folder.

## [A Place for Salvador Allende](a-place-for-salvador-allende)
**Main repository:** https://github.com/GoGroGlo/a-place-for-salvador-allende

**Source:** Based on the previous work at http://www.abacq.org/calle/, which compiled places sent by users from around the world.

At first, I've manually gathered a few places from Chile and elsewhere, but right now I'm creating a scraper for http://www.abacq.org/calle/ and OpenStreetMap instead and then manually verifying the data using OpenStreetMap and Google Maps. Data collection will be done by country.

**Questions to answer:**
* Prove that there are more places named after Salvador Allende, President of Chile from 1970 to 1973, _outside_ of Chile than there are _inside_ of Chile. There is a historical reason behind this which is worth elaborating on when the dataset is more matured.

## [Presidents of Chile](presidents-of-chile)
**Source:** `persons`, `tenures` and `deaths` datasets manually gathered from Wikipedia in [English](https://en.wikipedia.org/wiki/List_of_presidents_of_Chile) and [Spanish](https://es.wikipedia.org/wiki/Anexo:Presidentes_de_Chile)

**Questions to answer:**
* `persons` - demographic info about individual presidents
    * Is Gabriel Boric indeed the youngest president to take office?
* `tenures` - information about when presidents started and ended their tenure
    * Which presidents did not complete their term, and why?
* `elections` - candidates and votes for every Chilean presidential election (dataset pending, will try to scrape this)
    * Did Salvador Allende run the most number of elections before becoming president?

**Content warning:** Contains various methods of death in the `deaths` dataset and `tenures` notes.

## [Mobile Phones](mobile-phones)
**Source:** GSMArena Phone Dataset at https://www.kaggle.com/datasets/arwinneil/gsmarena-phone-dataset

**Questions to answer:**
* When exactly did big phones became popular?
* Is the audio jack still alive? Did iPhone 7 (or whichever iPhone it was) really start its end?
* Which regions get the most phone models? Where is competition the fiercest?

## [Movies](movies)
**Source:** Some homework for a Python course I was in. I think [`movies.xlsx`](movies/movies.xlsx) is from Kaggle.

**Questions to answer:**
* What are the top 10 movies per audience rating, as measured by their metascores?