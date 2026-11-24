# Dashboard Kamer 0.26

Kamerdashboard voor kamer 0.26: koffierad, plekken en inchecken, stemming, traktaties, radio, klok en weer.

Alles draait in één HTML-bestand (`index.html`); gegevens worden lokaal in de browser opgeslagen (localStorage).

## Muziek

De draaimuziek (`spin-tune.m4a`) is een ingekorte versie van "Party and Gameover loop" (happy theme) door gilzoide, CC0: https://opengameart.org/content/party-and-gameover-loop

## Weer

Het wandscherm (Android 5.1, Chrome 39) vertrouwt het certificaat van open-meteo.com niet. Daarom haalt de workflow `.github/workflows/pages.yml` elk uur het weer op en publiceert het als `weather.json`; de pagina gebruikt dat als terugval.
