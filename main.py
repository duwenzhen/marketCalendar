import cloudscraper
import datetime
import time
import random
start = datetime.datetime(2022,1,15)
end = datetime.datetime(2022,12,15)
cur = start
scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

while cur <= end:
    print(cur)
    cur = cur + datetime.timedelta(days=30)
    sec = 0.1 * (random.randint(10,50))
    time.sleep(sec)
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    txt = scraper.get("https://www.forexfactory.com/calendar?month={}".format(cur.strftime("%b.%Y"))).text  # => "<!DOCTYPE html><html><head>..."
    file = open(cur.strftime("%b.%Y") + ".txt", "w")
    file.write(txt)
    file.close()



