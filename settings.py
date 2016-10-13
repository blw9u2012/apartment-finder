import os

## Price

# The minimum rent you want to pay per month.
MIN_PRICE = 1100

# The maximum rent you want to pay per month.
MAX_PRICE = 2800

## Location preferences

# The Craigslist site you want to search on.
# For instance, https://sfbay.craigslist.org is SF and the Bay Area.
# You only need the beginning of the URL.
CRAIGSLIST_SITE = 'washingtondc'

# What Craigslist subdirectories to search on.
# For instance, https://sfbay.craigslist.org/eby/ is the East Bay, and https://sfbay.craigslist.org/sfc/ is San Francisco.
# You only need the last three letters of the URLs.
AREAS = ["doc"]

# A list of neighborhoods and coordinates that you want to look for apartments in.  Any listing that has coordinates
# attached will be checked to see which area it is in.  If there's a match, it will be annotated with the area
# name.  If no match, the neighborhood field, which is a string, will be checked to see if it matches
# anything in NEIGHBORHOODS.
BOXES = {
    "adams_morgan": [
        [-77.0490826,38.914436],
        [-77.0364703,38.9265541]
    ],
    "capitol_hill": [
        [-77.009182,38.878012],
        [-76.988282,38.895375]
    ],
    "columbia_heights": [
        [-77.036599,38.919011],
        [-77.025189,38.937411]
    ],
    "brookland": [
        [-76.996232,38.921264],
        [-76.97154,38.942563]
    ],
    "shaw": [
        [-77.0270776,38.9056116],
        [-77.0149112,38.9169828]
    ],
    "petworth": [
        [-77.036465,38.934994],
        [-77.011398,38.950048]
    ],
    "bloomingdale": [
        [-77.0149272,38.910771],
        [-77.0090318,38.9223703]
    ],
    "mount_vernon": [
        [-77.02353,38.902411],
        [-77.011785,38.90761]
    ],
    "union_station": [
        [-77.0042975029,38.8971406395],
        [-76.9877779484,38.9011615003]
    ],
    "u_street" : [
        [-77.0344378,38.9121319043],
        [-77.0216488838,38.920711]
    ],
    "h_street": [
        [-77.009128,38.896127],
        [-76.984162,38.902573]
    ],
    "noma": [
        [-77.014762,38.904443],
        [-77.000406,38.912601]
    ],
    "eckington": [
        [-77.009075,38.908884],
        [-76.996447,38.921189]
    ]
}

# A list of neighborhood names to look for in the Craigslist neighborhood name field. If a listing doesn't fall into
# one of the boxes you defined, it will be checked to see if the neighborhood name it was listed under matches one
# of these.  This is less accurate than the boxes, because it relies on the owner to set the right neighborhood,
# but it also catches listings that don't have coordinates (many listings are missing this info).
NEIGHBORHOODS = [
    "adams morgan", "capitol hill", "columbia heights",
    "brookland", "shaw", "petworth", "bloomingdale",
    "mount vernon", "union station", "u street", "h street",
    "noma", "eckington"
]

## Transit preferences

# The farthest you want to live from a transit stop.
MAX_TRANSIT_DIST = 2 # kilometers

# Transit stations you want to check against.  Every coordinate here will be checked against each listing,
# and the closest station name will be added to the result and posted into Slack.
TRANSIT_STATIONS = {

}

## Search type preferences

# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
CRAIGSLIST_HOUSING_SECTION = 'apa'

## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 60 * 60 * 3

# Which slack channel to post the listings into.
SLACK_CHANNEL = "#housing"

# Bot name that will be posting to slack
BOT_NAME = "craigslistbot"

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = os.getenv('SLACK_TOKEN', "")

# Token that allows us to make requests to Google's Geocoding service
GEOCODE_API_TOKEN = os.getenv('GEOCODE_API_TOKEN', "")