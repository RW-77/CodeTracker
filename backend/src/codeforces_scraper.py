from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import time as time_library
# 116.0.5845.110 
def scrape():
    time_library.sleep(5) # codeforces slow rendering issue

    url = "https://codeforces.com/contests?complete=true"
    op = Options()
    op.add_argument('--headless')
    op.add_argument('--no-sandbox')
    op.add_argument("window-size=1920,1080")
    
    service = ChromeService(executable_path="/Users/caleb/Documents/Projects/ContestScheduler/venv/lib/python3.11/site-packages/chromedriver_binary/chromedriver")
    driver = webdriver.Chrome(service=service, options=op) # add options=op later
    # print(f"webdriver version: {driver.capabilities['version']}") # print chromedriver version
    driver.get(url)

    cf_content = BeautifulSoup(driver.page_source, 'lxml')
    contest_flex_div = cf_content.find('div', class_='contestList')

    datatable = contest_flex_div.find("div", class_="datatable")

    table = datatable.find("table")

    contests = table.select("tr[data-contestid]")

    contestDict = {}
    for idx, contest in enumerate(contests):
        currentDict = {}
        cols = contest.find_all("td")
        unwanted = cols[0].find("a")
        if(unwanted != None):
            unwanted.extract()
        name = cols[0].getText().strip()
        time = str(cols[2].getText().strip())
        utc_idx = time.find("UTC")
        if utc_idx != -1:
            time = time[:utc_idx]
        dt = datetime.strptime(time, "%b/%d/%Y %H:%M").astimezone(tz = timezone.utc)

        currentDict['site'] = "CF"
        currentDict['name'] = name        
        currentDict['time'] = dt.strftime("%Y-%m-%d %H:%M")

        contestDict[idx] = currentDict
        # print(contestDict[idx]) # debug

    return contestDict

def run():
    return scrape()
    try:
        return scrape()
    except Exception as e:
        print(__file__, "is broken")
        print(e)
        return {}

# run()