# DEPENDENCIES
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # Set Executable path
    # Create an instance of a Splinter Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # specifying that we'll be using Chrome as our browser
    # ** is unpacking the dictionary we've stored the path in
    browser = Browser('chrome', **executable_path, headless=False) ### change headless=True if you don't want to see the script 'work'-ing

    # Run all scraping functions and store results in a dictionary
    news_title, news_paragraph = mars_news(browser)
    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    # Close the automated browser when we are done
    browser.quit()

    return data



def mars_news(browser):
    # Visit Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Add a delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert browser html to a soup object and then quit browser
    html = browser.html
    # Beautiful Soup parses the HTML text and then stores it as an object ('news_soup')
    news_soup = soup(html, 'html.parser')
    
    # Use try/except for error handling
    try:
        # create variable slide_elem to hold our parent element (entire <div/> tag containing its descendent (other tags nested within))
        # CSS works from right to left -- will return the last item of a list
        slide_elem = news_soup.select_one('div.list_text')

        # Find the 'content_title' class within parent element
        # Use parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use parent element to find the paragraph text
        news_para = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_para


def featured_image(browser):
    # Visit Space Images website
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the 'FULL IMAGE' button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Try/Except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Combine with base url to get complete url
    img_url = url+img_url_rel
    
    return img_url


def mars_facts(browser):
    # Scrape entire table to Pandas DF
    url = 'https://galaxyfacts-mars.com'

    # Try/Except for error handling
    try:
        # use 'read_html' to scrape facts table into a pandas df
        df = pd.read_html(url)[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert pandas DF back into HTML format to use in web app later
    return df.to_html()

# If running as script, print scraped data
if __name__ == '__main__':
    print(scrape_all())



