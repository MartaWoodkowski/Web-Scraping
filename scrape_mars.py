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
    html_format_table = table.to_html(index=False, classes=['table','table-striped'])

    # Clean it up by getting rid of '\n'
    html_format_table = html_format_table.replace('\n', '')



    # MARS HEMISPHERES
    # URL of page to be scraped
    url = 'https://marshemispheres.com/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object
    soup = bs(response.text,'html.parser')

    # Examine the results, then determine element that contains sought info (titles, img urls)
    results = soup.find_all('div', class_='item')

    href_list = []
    title_list = []

    # Loop through returned results and append to the lists above
    for result in results:
        title_list.append(result.h3.text)
        href_list.append(url + result.a['href'])

    image_url_list = []

    # Loop through each img to get high resolution pics urls and append to the 'image_url_list'
    for url_p in href_list:
        response = requests.get(url_p)
        soup = bs(response.text,'html.parser')
        results = soup.find_all('div', class_='downloads')
        image_url_list.append(url + results[0].find_all('a')[1]['href'])

    hemisphere_image_urls = []

    # Create the list of dictionaries with the image url string and the hemisphere title, and 
    # append to 'hemisphere_image_urls' list
    for index in range(len(title_list)):
        hemisphere_image_urls.append({'title':title_list[index], 'img_url':image_url_list[index]})

    

    # Store data in a dictionary
    listings = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Info": html_format_table,
        "Hemisphere":hemisphere_image_urls
    }

    browser.quit()
    
    return listings


