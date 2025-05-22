# olx_car_cover_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

# Setup
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(), options=options)

# URL
url = "https://www.olx.in/items/q-car-cover"
driver.get(url)
time.sleep(5)  # Let the JS load

# Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver
driver.quit()

# Scrape results
results = []
for item in soup.select("li.EIR5N"):  # OLX post container
    title = item.select_one("span._2tW1I")  # Title
    price = item.select_one("span._89yzn")  # Price
    location = item.select_one("span._2tW1I._2sVhR")  # Location
    
    if title and price:
        results.append([
            title.get_text(strip=True),
            price.get_text(strip=True),
            location.get_text(strip=True) if location else "N/A"
        ])

# Save to CSV
with open("olx_car_covers.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Price", "Location"])
    writer.writerows(results)

print(f"Saved {len(results)} results to olx_car_covers.csv")
