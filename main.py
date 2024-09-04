from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib
from datetime import datetime, timedelta
from threading import Timer

load_dotenv()

email = os.environ["MY_EMAIL"]
password = os.environ["MY_EMAIL_PASSWORD"]
smtp_provider = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
url = "https://appbrewery.github.io/instant_pot/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# Find the HTML element that contains the price
price = soup.find(class_="a-offscreen").get_text()

# Remove the dollar sign using split
price_without_currency = price.split("$")[1]

# Convert to floating point number
price_as_float = float(price_without_currency)
print(price_as_float)

# Get the product title
title = soup.find(id="productTitle").get_text().strip()
# print(title)

message = f"{title} is on sale for {price}!"
print(message)

x = datetime.today()
y = x.replace(day=x.day, hour=9, minute=0, second=0, microsecond=0)+timedelta(days=1)
delta_t = y-x

secs = delta_t.total_seconds()
def notify():
    with smtplib.SMTP(smtp_provider) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email,
                            to_addrs=email,
                            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
                            )

if price < "100":
    t = Timer(secs, notify)
    t.start()
