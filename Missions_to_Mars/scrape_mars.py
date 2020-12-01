

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():

    browser = Browser("chrome")
    mars = {}




    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # Find all the content title and paragraph
    news_title =  soup.find_all('div', class_='content_title')
    news_p = soup.find_all('div', class_='article_teaser_body')

    print(news_title)
    print(news_p)


    # A blank list to hold the headlines " we are trying to display all titles "
    news_titles = []
    # Loop over div elements
    for result in news_title:
        # Identify the anchor...
        if (result.a):
            # And the anchor has non-blank text...
            if (result.a.text):
                # Append thext to the list
                news_titles.append(result)
    news_titles



    # A blank list to hold the paragraphs " we are trying to display all paragraph "
    news_para = []
    # Loop over div elements
    for result in news_p:
        # Identify the anchor...
        if (result.text):
            # Append thext to the list
            news_para.append(result)
    news_para


    #Top 5 Titles
    top_titles = []
    # Print only the headlines
    for x in range(5):
        temp=news_titles[x].text
        newvar = temp.strip('\n\n')
        top_titles.append(newvar)
    mars["news_title"] =top_titles[0]

    #Top 5 Paragraph
    top_paragraph = []
    # Print only the headlines
    for x in range(5):
        temp=news_para[x].text
        newvar = temp.strip('\n\n')
        top_paragraph.append(newvar)
    top_paragraph
    mars["news_paragraph"] =top_paragraph[0]


    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    browser.find_by_id('full_image').click()
    time.sleep(2)
    browser.find_link_by_partial_text('more info').click()
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find('figure', class_="lede")
    featured_image_url = featured_image_url.a.img["src"]
    featured_image_url

    main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = main_url + featured_image_url

    featured_image_url
    mars["featured_image"] =featured_image_url


    ### Mars Facts



    # define url
    mars_facts_url = "https://space-facts.com/mars/"

    # read html into pandas
    tables = pd.read_html(mars_facts_url)

    # It returns 3 tables. The first has the data needed, so will convert to a dataframe and clean up nameing

    facts_mars = tables[0]
    facts_mars.columns = ["Description", "Value"]

    facts_mars

    #setting index
    facts_mars.set_index('Description', inplace=True)
    facts_mars.head()

    #Use Pandas to convert the data to a HTML table string.
    html_table = facts_mars.to_html()
    html_table
    mars["facts"] =html_table



    # define url and open in browser

    mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_url)



    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #finding titles of hemispheres
    hemisphere_titles = soup.find_all('h3')
    hemisphere_titles



    #Use a Python dictionary to store the data using the keys `img_url` and `title`.

    hemisphere_image_urls = []

    #going through each title, clicking it opening the wide image coping url printing as we go along and putting in dictionary
    for i in range(len(hemisphere_titles)):
        hemisphere_title = hemisphere_titles[i].text
        print(hemisphere_title)
        
        hemisphere_images = browser.find_by_tag('h3')
        hemisphere_images[i].click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_url = soup.find('img', class_='wide-image')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        print(img_url)
        
        hemisphere_dict = {"title": hemisphere_title, "img_url":img_url}
        hemisphere_image_urls.append(hemisphere_dict)
        
        browser.back()

    #printing dictionary

    hemisphere_image_urls
    mars["hemispheres"] =hemisphere_image_urls



    return mars

if __name__ == "__main__":
    print(scrape_info())

