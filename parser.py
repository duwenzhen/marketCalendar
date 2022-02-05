import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

class news:
    def __init__(self, date, time, currency, eventname, impact):
        self.date = date
        self.time = time
        self.currency = currency
        self.eventname = eventname
        self.impact = impact
    def __str__(self):
        return "{} {} {} {} {}".format(self.date, self.time, self.currency, self.eventname, self.impact)


def parsing(filename, holidays):
    year = filename.split('.')[1]
    if not os.path.exists(year):
        os.mkdir(year)

    f = open(filename, 'r')
    txt = f.read()
    soup = BeautifulSoup(txt, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

    #class="calendar__table "
    table = soup.find('table', attrs={'class':'calendar__table'})
    table_body = table.find('tbody')

    rows = table_body.findAll('tr', attrs={'class' : 'calendar_row'})
    #events = []
    currentday = ""
    curenttime = ""
    for row in rows:
        if "newday" in row['class']:
            currentday = row.find_all('td', attrs={'class': 'date'})[0].find_all('span', attrs={'class' : 'date'})[0].find_all('span')[0].text.strip()
        time = row.find_all('td', attrs={'class': 'time'})[0].text.strip()
        curenttime = curenttime if time == "" else time
        if curenttime == "All Day":
            curenttime = "1:01am"
        try:
            curenttimeConverted = datetime.datetime.strptime(curenttime, "%I:%M%p")
        except:
            curenttimeConverted = datetime.datetime.strptime("1:01am", "%I:%M%p")
        curenttime_towrite = curenttimeConverted.strftime("%H:%M:%S")
        currency = row.find_all('td', attrs={'class': 'currency'})[0].text.strip()
        eventname = row.find_all('td', attrs={'class': 'event'})[0].text.strip()
        if currency == "" and eventname == "":
            continue
        impact = row.find_all('td', attrs={'class': 'impact'})[0].find('span')['class'][0].strip()
        if impact.lower() == "holiday":
            df2 = {'currency': currency, 'date': year + ' ' + currentday}
            holidays = pd.concat([holidays, df2])

        evenement = news(currentday, curenttime_towrite, currency, eventname, impact)
        date = datetime.datetime.strptime(year + ' ' + currentday, "%Y %b %d")
        outputpath = os.path.join(year, date.strftime("%Y%m%d") + ".csv")
        if not os.path.exists(outputpath):
            output = open(outputpath, 'a')
            output.write("{},{},{},{}\n".format("time", "currency", "event", "impact"))
        else:
            output = open(outputpath, 'a')
        output.write("{},{},{},{}\n".format(evenement.time, evenement.currency, evenement.eventname, evenement.impact))
        output.close()

    return holidays



import glob
if __name__ == "__main__":
    holidays = pd.DataFrame(columns=["currency","date"])
    for f in glob.glob("*.txt"):
        holidays = parsing(f, holidays)
    holidays.to_csv("holidays.csv", index=False)