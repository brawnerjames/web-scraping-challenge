from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
import requests
import os
import pymongo
import pandas as pd
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    scrape_content = {}

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.mars_db
    collection = db.articles

    #scrape title and paragraph
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    scrape_content['news_title'] = soup.find('div', class_='content_title').text
    scrape_content['news_paragraph'] = soup.find('div', class_='rollover_description_inner').text


    #scrape image
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    browser.click_link_by_id('full_image')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, 'lxml')
    scrape_content['featured_image_url'] = 'https://www.jpl.nasa.gov' + soup.find(class_='main_image')['src'].strip()

    #scrape tweet
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(tweet_url)
    tweet_soup = bs(response.text, 'html.parser')
    scrape_content['tweet'] = tweet_soup.find(class_="tweet-text").text.strip()


    #scrape Mars facts table
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    facts_df = pd.DataFrame(facts_table[0])
    facts_df = facts_df.rename(columns = {0:'Attribute', 1:'Value'})
    scrape_content[col2row0] = facts_df['Value'][0]
    scrape_content[col2row1] = facts_df['Value'][1]
    scrape_content[col2row2] = facts_df['Value'][2]
    scrape_content[col2row3] = facts_df['Value'][3]
    scrape_content[col2row4] = facts_df['Value'][4]
    scrape_content[col2row5] = facts_df['Value'][5]
    scrape_content[col2row6] = facts_df['Value'][6]
    scrape_content[col2row7] = facts_df['Value'][7]
    scrape_content[col2row8] = facts_df['Value'][8]


    #scrape hemisphere data
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #scrape Cerberus Hemisphere data
    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    browser.click_link_by_id('wide-image-toggle')
    html = browser.html
    soup = bs(html, 'lxml')
    scrape_content['cerberus_image_url'] = 'https://astrogeology.usgs.gov' + soup.find(class_='wide-image')['src'].strip()
    scrape_content['cerberus_title'] = soup.find(class_='title').text

    #scrape Schiaparelli Hemisphere data
    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    browser.click_link_by_id('wide-image-toggle')
    html = browser.html
    soup = bs(html, 'lxml')
    scrape_content['schiaparelli_image_url'] = 'https://astrogeology.usgs.gov' + soup.find(class_='wide-image')['src'].strip()
    scrape_content['schiaparelli_title'] = soup.find(class_='title').text

    #scrape Syrtis Major Hemisphere data
    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    browser.click_link_by_id('wide-image-toggle')
    html = browser.html
    soup = bs(html, 'lxml')
    scrape_content['syrtis_image_url'] = 'https://astrogeology.usgs.gov' + soup.find(class_='wide-image')['src'].strip()
    scrape_content['syrtis_title'] = soup.find(class_='title').text

    #scrape Valles Marineris Hemisphere data
    browser.visit(hemi_url)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    browser.click_link_by_id('wide-image-toggle')
    html = browser.html
    soup = bs(html, 'lxml')
    scrape_content['valles_image_url'] = 'https://astrogeology.usgs.gov' + soup.find(class_='wide-image')['src'].strip()
    scrape_content['valles_title'] = soup.find(class_='title').text

    #hemisphere_urls = [
    #{"title": cerberus_title, "img_url": cerberus_image_url},
    #{"title": schiaparelli_title, "img_url": schiaparelli_image_url},
    #{"title": syrtis_title, "img_url": syrtis_image_url},
    #{"title": valles_title, "img_url": valles_image_url},
    #]

    browser.quit

    return scrape_content



