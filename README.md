# Kirjakeskustelusovellus

Sovelluksessa voi jakaa arvosteluja kirjoista, keskustella niistä ja lukea muiden arvosteluja. Jokaisen arvostelun (keskustelun) aihe on tietty kirja. Jokainen käyttäjä on peruskäyttäjä.

Sovelluksen ominaisuuksia: 
Käyttäjä voi luoda uuden tunnuksen sekä kirjautua sisään ja ulos. 
Sovelluksen etusivulla näkyy arvostelujen määrä ja arvostelut. 
Arvostelut liittyvät tiettyyn kirjaan ja ovat myös ketjuja, joissa voi käydä keskustelua. 
Käyttäjä voi hakea arvosteluja kirjan nimen perusteella. 
Käyttäjä voi antaa arvostelun kirjasta antamalla kirjan nimen, kirjailijan, arvostelun sisällön ja arvosanan (1-5).  
Hakemalla tiettyä kirjaa käyttäjä näkee arvostelut kirjasta. 
Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun (arvosteluun). 
Käyttäjä voi tallentaa kirjoja suosikkeihin ja katsoa, mitä kirjoja on lisännyt suosikkeihin.



Kloonaa reposition koneellesi. Tämän jälkeen luo samaan kansioon .env -niminen tiedosto.
.env tiedoston sisällöksi tulee:
- DATABASE_URL=
- SECRET_KEY =

Asenna virtuaaliympäristö ja sovelluksen riippuvuudet komennoilla:
- $cd kirjakeskustelusovellus
- $python3 -m venv venv
- $source venv/bin/activate
- $pip install flask
- $pip install flask-sqlalchemy
- $pip install psycopg2-binary
- $pip install python-dotenv
- $flask run


