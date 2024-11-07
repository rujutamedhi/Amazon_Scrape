# used beautiful soup since Amazon is static website

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import traceback

try:
    # Initialize lists to store all the details
    product_names = []
    prices = []
    ratings = []
    seller_names = []
    stars = []
    
    # Specify the URL
    url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"
    
    # Set up headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    
    # Send request to get the main page content
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    
    # Find all product links on the page
    box = soup.find("span", class_="rush-component s-latency-cf-section")
    links = box.find_all('a', class_="a-link-normal s-no-outline")
    
    # Loop through each product link
    for link in links:
        href = link.get('href')
        product_url = "https://www.amazon.in" + href
        
        # Send a request for each product's detail page
        r1 = requests.get(product_url, headers=headers)
        soup1 = BeautifulSoup(r1.text, "lxml")
        
        # Locate the product detail section
        box1 = soup1.find("div", class_="centerColAlign")
        
        # Extract product name
        name = box1.find("span", class_="a-size-large product-title-word-break")
        product_names.append(name.text.strip() if name else "Not available")
        print(name)
        
        # Extract price
        price_tag = box1.find("span", class_="a-price-whole")
        prices.append(price_tag.text.strip() if price_tag else "Not available")
        
        # Extract ratings
        rating = box1.find("span", id="acrCustomerReviewText")
        ratings.append(rating.text.strip() if rating else "Not available")
        
        # Extract stars
        star = box1.find("span", class_="a-size-base a-color-base")
        stars.append(star.text.strip() if star else "Not available")
        
        # Extract seller name
        box2 = soup1.find("div", class_="a-box-inner")
        seller_name = box2.find("a", id="sellerProfileTriggerId")
        seller_names.append(seller_name.text.strip() if seller_name else "Not available")
        
        # Pause between requests to avoid being blocked
        time.sleep(2)
    
    # Create a DataFrame from the collected data
    data = {
        "Product Name": product_names,
        "Price": prices,
        "Rating": ratings,
        "Seller Name": seller_names,
        "Stars": stars
    }
    
    # Save data to CSV
    df = pd.DataFrame(data)
    df.to_csv('ScrapedData.csv', index=False)
    print("Data scraped and saved successfully!")

except Exception as e:
    print("An error occurred:", e)
    traceback.print_exc()
