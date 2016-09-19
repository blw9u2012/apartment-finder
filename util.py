import settings
import math
import urllib3
import json

urllib3.disable_warnings()

def coord_distance(lat1, lon1, lat2, lon2):
    """
    Finds the distance between two pairs of latitude and longitude.
    :param lat1: Point 1 latitude.
    :param lon1: Point 1 longitude.
    :param lat2: Point two latitude.
    :param lon2: Point two longitude.
    :return: Kilometer distance.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km

def in_box(coords, box):
    """
    Find if a coordinate tuple is inside a bounding box.
    :param coords: Tuple containing latitude and longitude.
    :param box: Two tuples, where first is the bottom left, and the second is the top right of the box.
    :return: Boolean indicating if the coordinates are in the box.
    """
    if box[0][0] < coords[0] < box[1][0] and box[1][1] < coords[1] < box[0][1]:
        return True
    return False

def post_listing_to_slack(sc, listing):
    """
    Posts the listing to slack.
    :param sc: A slack client.
    :param listing: A record of the listing.
    """
    try:
        desc = "{0} | {1} | {2} | <{3}>".format(listing["area"], listing["price"], listing["name"], listing["url"])
        sc.api_call(
            "chat.postMessage", channel=settings.SLACK_CHANNEL, text=desc,
            username=settings.BOT_NAME, icon_emoji=':kirby:'
        )
    except Exception, e:
        print "Failed to post to slack :("

def find_points_of_interest(geotag, location):
    """
    Find points of interest, like transit, near a result.
    :param geotag: The geotag field of a Craigslist result.
    :param location: The where field of a Craigslist result.  Is a string containing a description of where
    the listing was posted.
    :return: A dictionary containing annotations.
    """
    area_found = False
    area = ""

    for a, coords in settings.BOXES.items():
        if in_box(geotag, coords):
            area = a
            area_found = True

    # If the listing isn't in any of the boxes we defined, check to see if the string description of the neighborhood
    # matches anything in our list of neighborhoods.
    if len(area) == 0:
        for hood in settings.NEIGHBORHOODS:
            if hood in location.lower():
                area = hood
                area_found = True
    return {
        "area_found": area_found,
        "area": area
    }

def get_coordinates(where):
    where = where.replace(" ", "+")
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}".format(where, settings.GEOCODE_API_TOKEN)
    http_agent = urllib3.PoolManager()
    request = http_agent.request('GET', url)
    response = json.loads(request.data)
    box = []
    # Coordinates of the viewport on Google Maps
    try:
        _coords = response['results'][0]['geometry']['viewport']
        box = [[0, 0], [0, 0]]

        # Convert to acceptable format
        for k, v in _coords.iteritems():
            # Get coordinates of southwest corner first...
            if k == 'southwest':
                for x, y in v.iteritems():
                    if x == 'lng':
                        box[0][0] = y
                    else:
                        box[0][1] = y
            else:
                for x, y in v.iteritems():
                    if x == 'lng':
                        box[1][0] = y
                    else:
                        box[1][1] = y
        return box
    except Exception, e:
        print "Unable to get coordinates :("
    return box


