#!/usr/bin/env python
# coding: utf-8

# In[13]:


# DEPENDENCIES
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


# Set Executable path
# Create an instance of a Splinter Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
# specifying that we'll be using Chrome as our browser
# ** is unpacking the dictionary we've stored the path in
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Add a delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# set up HTML parser
html = browser.html
# Beautiful Soup parses the HTML text and then stores it as an object ('news_soup')
news_soup = soup(html, 'html.parser')
# create variable slide_elem to hold our parent element (entire <div/> tag containing its descendent (other tags nested within))
# CSS works from right to left -- will return the last item of a list
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Find the 'content_title' class within parent element
slide_elem.find('div', class_='content_title')


# ### Title & Summary

# In[6]:


# Use parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use parent element to find the paragraph text
news_para = slide_elem.find('div', class_='article_teaser_body').get_text()
news_para


# ### Featured Images

# In[8]:


# Visit Space Images website
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# In[9]:


# Find and click the 'FULL IMAGE' button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Combine with base url to get complete url
img_url = url+img_url_rel
img_url


# In[19]:


# Scrape entire table to Pandas DF
url = 'https://galaxyfacts-mars.com'
df = pd.read_html(url)[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[20]:


# Convert pandas DF back into HTML format to use in web app later
df.to_html()


# In[21]:


# Close the automated browser when we are done
browser.quit()


# In[ ]:




