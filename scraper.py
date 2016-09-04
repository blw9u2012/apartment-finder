from craigslist import CraigslistHousing
from dateutil.parser import parse
from util import post_listing_to_slack, find_points_of_interest
from slackclient import SlackClient
from pymongo import MongoClient
import time
import settings

# Initialize Mongo client....
client = MongoClient('localhost', 27017)
db = client['listings']
listing_collections = db['listings']

def scrape_area(area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistHousing(site=settings.CRAIGSLIST_SITE, area=area, category=settings.CRAIGSLIST_HOUSING_SECTION,
                             filters={'max_price': settings.MAX_PRICE, 'min_price': settings.MIN_PRICE})

    results = []
    gen = cl_h.get_results(sort_by='newest', geotagged=True, limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception, e:
            print str(e)
            continue
        #listing = session.query(Listing).filter_by(cl_id=result["id"]).first()
        # Check for listing
        listing = listing_collections.find_one({"id": result["id"]})

        # Don't store the listing if it already exists.
        if listing is None:
            if result["where"] is None:
                # If there is no string identifying which neighborhood the result is from, skip it.
                continue

            lat = 0
            lon = 0
            if result["geotag"] is not None:
                # Assign the coordinates.
                lat = result["geotag"][0]
                lon = result["geotag"][1]

                # Annotate the result with information about the area it's in and points of interest near it.
                geo_data = find_points_of_interest(result["geotag"], result["where"])
                result.update(geo_data)
            else:
                result["area"] = ""

            # Try parsing the price.
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            listing = {
                "link": result["url"],
                "created": parse(result["datetime"]),
                "lat": lat,
                "lon": lon,
                "name": result["name"],
                "price": price,
                "location": result["where"],
                "cl_id": result["id"],
                "area": result["area"]
            }

            # Insert into the collection...
            _listing_id = listing_collections.insert_one(listing)

    return results

def do_scrape():
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = []
    for area in settings.AREAS:
        all_results += scrape_area(area)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post each result to slack.
    for result in all_results:
        post_listing_to_slack(sc, result)
