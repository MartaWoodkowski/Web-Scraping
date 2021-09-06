#!/usr/bin/env python
# coding: utf-8
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


def scrape(): 
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # NASA MARS NEWS
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Get the Title of the latest article
    news_title = browser.find_by_css('div.content_title')[0].text

    # Get the content of the latest article
    news_p = browser.find_by_css('div.article_teaser_body')[0].text



    # JPL MARS SPACE IMAGES - FEATURED IMAGE
    # URL of page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find full size .jpg image
    browser.find_by_text(' FULL IMAGE').click()

    # Save the image to a variable
    featured_image_url = browser.find_by_css('img.fancybox-image')[0]['src']



    # MARS FACTS
    # URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'

    # Extracting second table 
    table = pd.read_html(url)[0] 

    # Naming the columns
    table.columns=['Description','Mars','Earth']

    # Convert the data to an HTML table string
    html_format_table = table.to_html(index=False, border=True, classes=['table','table-striped','table-responsive'])
    
    # Clean it up by getting rid of '\n'
    html_format_table = html_format_table.replace('\n', '')

    # Replace the align (from default 'right') to 'left'
    html_format_table = html_format_table.replace('right', 'left')



    # MARS HEMISPHERES
    # URL of page to be scraped
    url = 'https://marshemispheres.com/'
        
    # Go to main page
    browser.visit(url)

    # Find how many links to pictures are on the page
    links = browser.find_by_css('h3')
    links_number = len(links)-1

    hemisphere_image_urls = []

    for x in range(links_number):
        
        # Get the title
        links = browser.find_by_css('h3')
        title = links[x].text
        
        # Click the link
        links[x].click()
        
        # Extract picture url
        url_link = browser.find_by_text('Sample')['href']
        
        # Create dictionary
        hemisphere_image_urls.append({"title":title,"img_url":url_link})
        
        #Go back orginal page
        browser.find_by_text('Back').click()
    

    # Store data in a dictionary
    listings = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Info": html_format_table,
        "Hemispheres":hemisphere_image_urls
    }

    browser.quit()
    
    return listings