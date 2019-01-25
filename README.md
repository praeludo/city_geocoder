# City Geocoder

Retourne les coordonnées GPS d'un lieu en interrogeant le service Nominatim d'OpenStreetMap. Répond aux exigences du Usage Policy du service (1 requête max par seconde, indication d'un UserAgent et d'une adresse mail, caching) - cf. https://operations.osmfoundation.org/policies/nominatim/
Nécessite un server Redis accessible (par exemple en local dans un container).

Returns GPS coordinates for a place by interrogating OpenStreetMap's Nominatim service. Meet Nominatim Usage Policy requirements (1 request / sec, email address and UserAgent set up, caching), please read https://operations.osmfoundation.org/policies/nominatim/ for further information.
Needs a Redis server (for example running in a local container). 

# Python version

Testé avec Python 3.7

Tested with Python 3.7

# Usage

`python3 city_geocoder.py --city Paris --country France --email email@provider.com`

# License

MIT