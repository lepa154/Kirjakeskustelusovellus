# Kirjakeskustelusovellus

Sovelluksessa voi jakaa arvosteluja kirjoista, keskustella niistä ja lukea muiden arvosteluja. Jokaisen arvostelun (keskustelun) aihe on tietty kirja. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia: 
Käyttäjä voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos. 
Sovelluksen etusivulla näkyy arvostelujen määrä ja arvostelut. 
Arvostelut liittyvät tiettyyn kirjaan ja ovat myös ketjuja, joissa voi käydä keskustelua. 
Käyttäjä voi hakea arvosteluja kirjan, genren tai arvosanan perusteella. 
Käyttäjä voi antaa arvostelun kirjasta antamalla kirjan nimen, kirjailijan ja arvosanan (1-5).  
Hakemalla tiettyä kirjaa käyttäjä näkee kirjojen arvostelujen keskiarvon (1-5) ja arvostelut kirjasta. 
Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun (arvosteluun). 
Ylläpitäjä voi lisätä ja poistaa keskusteluja ja määrittää kirjoilla genren. Ylläpitäjä voi poistaa arvosteluja.

Sovellukseen voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos. Sovellukseen voi luoda arvostelun.



Kloonaa reposition koneellesi. Tämän jälkeen luo samaan kansioon .env -niminen tiedosto.
.env tiedoston sisällöksi tulee:
- DATABASE_URL=
- SECRET_KEY =

Asenna virtuaaliympäristö ja sovelluksen riippuvuudet komennoilla:
- $cd friendapp
- $python3 -m venv venv
- $source venv/bin/activate
- $pip install flask
- $pip install flask-sqlalchemy
- $pip install psycopg2-binary
- $pip install python-dotenv
- $flask run


