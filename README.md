# Glo's Datasets of Interest
Some Python-based investigations about datasets I'm personally interested in.

All of my notes are in Jupyter notebooks (.ipynb). The notes and datasets are included in every dataset folder.

## [Presidents of Chile](presidents-of-chile)
**Source:** `persons`, `tenures` and `deaths` datasets manually gathered from Wikipedia

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

## [A Place for Salvador Allende](a-place-for-salvador-allende)
**Source:** Based on the previous work at http://www.abacq.org/calle/, which compiled places sent by users from around the world.

At first, I've manually gathered a few places from Chile and elsewhere, but I'm thinking of scraping http://www.abacq.org/calle/ instead and then verifying the data using OpenStreetMap and Google Maps.

**Questions to answer:**
* Prove that there are more places named after Salvador Allende, President of Chile from 1970 to 1973, _outside_ of Chile than there are _inside_ of Chile. There is a historical reason behind this which is worth elaborating on when the dataset is more matured.

