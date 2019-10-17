# This is a program to scrape data from a website and send an email to you to notify a price drop.
# Followed a YouTube tutorial for this example but wanted to practice Python and mess around with
# HTML requests and emailing

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Link to the item on Amazon whose price I want to watch.
URL = 'https://www.amazon.co.uk/Fujifilm-X-T100-Silver-Black-XC15-45/dp/B07D6XP5VL/ref=sr_1_2?keywords=fujifilm+xt100&qid=1570580820&sr=8-2'

# Browser info
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90'
    }
# Function to get the title/price of the item from the HTML, add it into variables. Print it and do a comparison.
# If the comparison is true then it calls a function to send an email.
def check_price():

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[1:7])

    print('\nItem: '+title.strip())
    print('Price: €',converted_price)

    if(converted_price < 500):
        send_mail()

# This function uses the SMTP library to allow email
def send_mail():
    # Connecting with the email client/server. I use Gmail in this case.
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Login to my Gmail account using a gerated app password. This is possible because I have two-step verification enabled on my account.
    server.login('scottdonohd@gmail.com', '***********')

    # Variables that contain the actual content of the email.
    subject = 'Price Fell Down'
    body = """Hey,\n\n
            The camera you had your eye on has dropped in price\n
            Check it out here:\n
            https://www.amazon.co.uk/Fujifilm-X-T100-Silver-Black-XC15-45/dp/B07D6XP5VL/ref=sr_1_2?keywords=fujifilm+xt100&qid=1570580820&sr=8-2
            """

    msg = f"Subject: {subject}\n\n{body}"

    # Sending the email to, from and what it contains.
    server.sendmail(
        'scottdonohd@gmail.com',
        'scottdonohd@gmail.com',
        msg
    )
    # Confirmation of function call
    print("Email has been sent")

    # End connection to the email server.
    server.quit()

# This loop causes the check_price function to be called once a day.
while(True):
    check_price()
    time.sleep(60*60*24)