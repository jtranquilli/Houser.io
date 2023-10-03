import os
import re
import sqlite3
import argparse
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import facebook_scraper
from facebook_scraper import *
import string
import random

# make sure that the ordering of columns in the new db is the same as in posts.db

blacklist = ["women only", "girls only", "females only", "swap", "queer only"]

street_address   = re.compile('\d{2,4} [\w\s]{1,20}(rue|Rue|RUE|rue de la|RUE DE LA|:?:street||de la|rue|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)

set_user_agent("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
#Facebook says 'Unsupported Browser' warnings.warn(f"Facebook says 'Unsupported Browser'")

fb_username = "jtranqs@gmail.com"
fb_password = "opmb1584Ryersie"
pages = 1
credentials = (fb_username,fb_password)

allGroups = itertools.chain(
  get_posts(group=121127129846370, pages=pages, credentials=credentials), # (UQAM, Concordia, McGill, HEC, UdeM) Off-Campus Housing
  get_posts(group=872529396154763, pages=pages, credentials=credentials), # McGill Off campus housing  
  get_posts(group=641712229179289, pages=pages, credentials=credentials), # Chez queer  
  get_posts(group=862226797299645, pages=pages, credentials=credentials), # Montreal Housing, Rooms, Flats, Apartments, Sublets
  get_posts(group=1499524676963883, pages=pages, credentials=credentials) # Cession de bail / sous-location MONTRÉAL (entraide de locataires)
  
)

# sqlite setup
conn = sqlite3.connect('db.sqlite3') #formerly posts.db
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Create table
c.execute("CREATE TABLE IF NOT EXISTS main_housinglisting(post_text text, price real, number_of_rooms INTEGER, image_url text, post_id text PRIMARY KEY, user_id text, address text, time text)")


def serialize_URLS(url_list): #returns a string represented a space delimited list of image URLs
    series = ""
    for url in url_list:
        series += url
        series += " "
        
    return series


def get_address(text):
    temp = re.search(street_address, text) #use regular expresssion matching
    if(temp is None):
        return str("No address")
    temp = temp.group() #grab the string that was matched
    
    address = temp.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
    
    return address
       

class FacebookPost(object):
    def __init__(self, post_text: str, price: int, image_url: str, post_id: str, number_of_rooms: int, user_ID: str, address: str, time: str):
      self.post_text = post_text
      self.price = price
      self.image_url = serialize_URLS(image_url)
      self.post_id = post_id
      self.number_of_rooms = number_of_rooms
      self.user_ID = user_ID
      self.address = address
      self.time = time

def save_post(post: FacebookPost):
  c.execute("REPLACE INTO posts VALUES (?,?,?,?,?,?,?,?)", (
    post.post_text,
    post.price,
    post.number_of_rooms,
    post.image_url,
    post.post_id,
    post.user_ID,
    post.address,
    post.time
  ))

def get_posts_from_db():
  posts = [FacebookPost(p[0], p[1], p[3], p[4], p[2], p[5]) for p in c.execute("SELECT * from posts")]
  return posts

# argument parser setup
parser = argparse.ArgumentParser(description='Scrape Facebook for posts.')
parser.add_argument('--scrape', action='store_true')
parser.add_argument('--display', action='store_true')
parser.add_argument('--plot', action='store_true')
parser.add_argument('--minimum_price', action='store', type=int, default=500)
parser.add_argument('--maximum_price', action='store', type=int, default=6000)
parser.add_argument('--minimum_rooms', action='store', type=int, default=1)
parser.add_argument('--maximum_rooms', action='store', type=int, default=3)
args = parser.parse_args()

def pretty_print(post: FacebookPost):
  print("\n-----------Post----------\n")
  print(f"\n PRICE: {post.price}\n")
  if number_of_rooms(post):
    print(f"\n number_of_rooms: {number_of_rooms(post)}\n")
  print(post.post_text)

def price(post: FacebookPost):
  
    text_as_list = post.post_text.split() #words delimited by spaces
      
    for word in text_as_list:
        if '$' in word:
            word = word.replace('$', '')
            word = word.strip() #remove possible white space just in case
            word = word.translate(str.maketrans('', '', string.punctuation)) #remove punctuation from string
            word = re.sub('\D', '', word) # replace any non-digit character with the empty string
              
            try:
                return int(word) #try converting the value to an int, if this is possible then return it as the answer for price of posting
              
            except:
                pass #do nothing
  
    return 0

def within_price_budget(post: FacebookPost):
  if post.price:
    return int(post.price) >= flags['minimum_price'] and int(post.price) <= flags['maximum_price']

def right_size(post: FacebookPost):
  if post.number_of_rooms:
    return int(post.number_of_rooms) >= flags['minimum_rooms'] and int(post.number_of_rooms) <= flags['maximum_rooms']

def has_text(post: FacebookPost):
  return len(post.post_text) > 1

def number_of_rooms(post: FacebookPost): #attempt to find the number of bedrooms from the posting
    
  match = re.search('([0-9]) bedrooms', post.post_text)
  
  if not match: #check if they used 'rooms' instead of 'bedrooms'
      match = re.search('([0-9]) rooms', post.post_text)
  if not match:  #check if they used 'bedroom' instead of 'bedrooms'
      match = re.search('([0-9]) bedroom', post.post_text)
  if not match:#check if they used 'bdr' instead of 'bedrooms'
      match = re.search('([0-9]) bdr', post.post_text)
  if not match: #check if they used 'beds' instead of 'bedrooms'
      match = re.search('([0-9]) beds', post.post_text)
  if not match: #check if they used 'bed' instead of 'bedrooms'
      match = re.search('([0-9]) bed', post.post_text)  
  if not match: #check if they used 'room' instead of 'bedrooms'
      match = re.search('([0-9]) room', post.post_text)
  if not match: #check if they used 'room' instead of 'bedrooms'
      match = re.search('([0-9]) BEDROOM', post.post_text) 
  if not match: #if all else fails check if they mention whether it is a studio
      if "studio" in post.post_text:
          return 1;
  if match:
    return match.group(1)
  return None

def append_price(post: FacebookPost):
  hasPrice = price(post)
  if hasPrice:
    post.price = hasPrice
    
def append_details_from_text(post: FacebookPost):
  append_price(post)
  append_rooms(post)

def append_rooms(post: FacebookPost):
  hasRooms = number_of_rooms(post)
  if hasRooms:
    post.number_of_rooms = hasRooms


def print_if_passes_filters(post: FacebookPost):
  if passes_filters(post):
    pretty_print(post)

def display():
  for p in get_posts_from_db():
    append_details_from_text(p)
    print_if_passes_filters(p)

def passes_filters(post: FacebookPost):
  return all((
    within_price_budget(post), 
    right_size(post), 
    has_text(post)
  ))

# parse args to flags
flags = vars(args)


flags['scrape'] = True
#flags['display'] = True


if flags['display'] and not flags['scrape']:
  display()


if flags['plot']:
  sns.set(style="whitegrid")
  data = [(post.price, post.number_of_rooms) for post in get_posts_from_db() if (post.price and post.number_of_rooms)]
  df = pd.DataFrame(data, columns=["price", "rooms"])
  sns.jointplot(x="price", y="rooms", data=df, kind="kde");
  plt.show()

if flags['scrape']:
    i = 1
    for post in allGroups:
        time.sleep(random.uniform(1,10)) # sleep for random uniform amount of time to avoid getting banned
        currentFacebookPost = FacebookPost(post.get('text'), None, post.get('images'), post.get('post_id'), None, post.get('user_id'),None, str(post['time']))
        
        currentFacebookPost.post_text = currentFacebookPost.post_text.lower() #makes text checking conditions easier
        currentFacebookPost.address = get_address(currentFacebookPost.post_text)
        currentFacebookPost.address = currentFacebookPost.address
        print("Post Number: ", i)
        append_details_from_text(currentFacebookPost)
        i+=1
        blacklisted = False
        for (word: blacklist):
            
            if word in currentFacebookPost.post_text:
                blacklisted = True
            if blacklisted == True:
                break
                
        save_post(currentFacebookPost)
        
        if i == 5:
            break #for testing purposes, don't scrape a large volume of posts
        #if flags['display']:
          #print_if_passes_filters(currentFacebookPost)

# Save (commit) the changes
conn.commit()
c.close()
