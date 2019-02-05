#Dependencies
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import time
import pandas as pd

# Creating "Scrape" function
def scrape():
    # Splinter browser
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    
    
    #---------------------------------------------------------------------------#
    ### NASA Mars News ###
    #URL of page to be scraped: NASA Mars News site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    response = browser.html
    
    # Creating BeautifulSoup object and parsing with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')
    
    # Retrieving latest news title & description
    news_title = soup.find('div', 'content_title', 'a').text
    news_p = soup.find('div', 'article_teaser_body').text
    
    
    
    #---------------------------------------------------------------------------#
    ### JPL Mars Space Images - Featured Image ###
    # URL for JPL Featured Space Image site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Visit site
    browser.visit(url)
    
    # Moving through pages on site; increased time.sleep from 1 to 4
    time.sleep(4)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)
    browser.click_link_by_partial_text('more info')
    time.sleep(4)
    
    # Retrieve page with the requests module
    response = browser.html
    
    # Creating BeautifulSoup object and parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')
    
    # Retrieve featured image
    image_href = soup.find('figure', 'lede').a['href']
    link = 'https://www.jpl.nasa.gov'
    featured_image_url = link + image_href
    
    #---------------------------------------------------------------------------#
    ### Mars Weather ###
    # URL for Mars Weather Twitter Account
    url = 'https://twitter.com/marswxreport?lang=en'
    
    # Visit site
    browser.visit(url)
    
    # Pulling the html text
    response = browser.html
    
    # Creating BeautifulSoup object and parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')
    
    # Extract the latest tweet
    mars_weather = soup.find('p', 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
   
   
    #---------------------------------------------------------------------------#
    ### Mars Facts ###
    # URL for Mars Facts Webpage
    url = 'https://space-facts.com/mars/'
    
    # Visit site
    browser.visit(url)
    response = browser.html
    
    # Creating BeautifulSoup object and parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')
    
    # Retrieving the entire table
    table= soup.find('table', 'tablepress tablepress-id-mars')
    
    # Retrieving all the rows in the table
    rows = table.find_all('tr')
    
    # Empty lists to hold td elements from each row
    labels = []
    values = []
   
    # Loop through rows & add first 'td' element to labels list and values list
    for row in rows:
        td_elements = row.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
    
    # Create Dataframe
    mars_facts = pd.DataFrame({" ": labels,
                            "Values": values})
    
    # Set a new index
    mars_facts.set_index(" ", inplace=True)
    
    # Show Dataframe
    mars_facts
    
    # Converting Dataframe to html table string
    html_table = mars_facts.to_html(header=False)
    
    
    #---------------------------------------------------------------------------#
    ### Mars Hemispheres ###
    # URL for Mars Facts Webpage
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Visit site
    browser.visit(url)
    
    # Retrieve page with the requests module
    response = browser.html
    
    # Creating BeautifulSoup object and parse with 'html.parser'
    soup = BeautifulSoup(response, 'html.parser')
    
    # Retrieving class for each hemisphere available
    returns = soup.find('div', 'collapsible results')
    
    # Retrieving all anchors in each class pulled above
    hemispheres = returns.find_all('div', {"class": 'description'})
    
    # Creating empty list to hold dictionaries
    hemisphere_image_urls = []
   
    # Looping through all anchors for each hemisphere class
    for description in hemispheres:
        a = description.find('a')
        
        # Retrieving title and link to specific hemisphere page
        title = a.h3.text
        link = 'https://astrogeology.usgs.gov' + a['href']
        
        # Visiting the link
        browser.visit(link)
        time.sleep(4)
        
        # Retrieving link to image
        page = browser.html
        results = BeautifulSoup(page, 'html.parser')
        image_link = results.find('div', 'downloads').find('li').a['href']
        
        # Creating empty dictionary for title & image
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_link
        
        # Adding image_dict to empty list from above
        hemisphere_image_urls.append(image_dict)
    
    mars_dict = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "facts": html_table,
        "hemispheres": hemisphere_image_urls}
    print(mars_dict)
    return mars_dict