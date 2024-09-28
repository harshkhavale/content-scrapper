import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time
from utils import filter_results  # Assuming this exists

def dynamic_scraper(url, search_term=None):
    options = Options()
    options.headless = True  # Run Selenium in headless mode (no GUI)
    
    # Specify the correct path to your ChromeDriver here
    driver = webdriver.Chrome(options=options)
    try:
        # Load the URL and wait for the page to render
        driver.get(url)
        time.sleep(3)  # Adjust time if the page takes longer to load

        # Get the page source
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Initialize results
        results = []

        # Scrape video data from the page (adjust the tags according to your target page)
        videos = soup.find_all('div', class_='thumb')
        
        if not videos:
            print("No videos found. Check the HTML structure or classes used.")
        
        for video in videos:
            title_tag = video.find('div', class_='thumb__title')
            img_tag = video.find('div', class_='thumb__img')
            link_tag = video.find('a', href=True)

            # Debug output
            if title_tag:
                print(f"Title found: {title_tag.text.strip()}")
            else:
                print("Title tag not found")

            if img_tag:
                img = img_tag.find('img')
                if img:
                    thumbnail_src = img['src']  # or use data-src0 if necessary
                else:
                    print("Image tag not found within thumb__img")
            else:
                print("thumb__img tag not found")

            if link_tag:
                video_link = url.split('/videos')[0] + link_tag['href']
            else:
                print("Link tag not found")

            # Only append if all components are found
            if title_tag and img_tag and link_tag:
                video_data = {
                    'title': title_tag.text.strip(),
                    'thumbnail': thumbnail_src,
                    'video_link': video_link
                }
                results.append(video_data)

        # Filter results based on the search term if provided
        if search_term:
            results = filter_results(results, search_term)

        return json.dumps(results, indent=4)

    finally:
        # Ensure driver quits even if there’s an error
        driver.quit()
