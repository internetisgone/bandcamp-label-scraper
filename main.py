from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import random

####### options #######

# bandcamp label(s) to scrape
LABEL_LINKS = [
   "https://absurdtrax.bandcamp.com/music",
   ]  

# http proxy 
PROXY = "https://127.0.0.1:7890"

# whether to include release date
INCLUDE_RELEASE_DATE = False 

WAIT_INTERVAL_MIN = 1

WAIT_INTERVAL_MAX = 3

####### selenium web driver #######

options = webdriver.ChromeOptions()
options.page_load_strategy = "normal"
options.add_argument("--headless")  
options.add_argument("--proxy-server = %s" % PROXY)

driver = webdriver.Chrome(options = options)

def fetch_page_soup(link):
   try: 
      driver.get(link)
      driver.implicitly_wait(0.5)
      page_content = driver.page_source.encode("utf-8") 

      return BeautifulSoup(page_content, "html.parser")
   except Exception as e:
      print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went wrong when fetching {link} : {e}")
   
def get_release_date(album_link):
   try:
      print(f"getting album info {album_link}")
      soup = fetch_page_soup(album_link)

      if soup:
         info_container = soup.find(id = "trackInfoInner")
         if info_container:
            date = info_container.find("div", class_="tralbum-credits").find(string=True, recursive=False).strip()
            if "released" in date:
               date = date.split("released ")[1] 
            elif "releases" in date:
               date = date.split("releases ")[1]
            else:
               date = ""
            return date
         
      print(f"｡ﾟ･ (>_<) ･ﾟ｡ rlease date not found for {album_link}")
      return ""
   except Exception as e:
      print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went wrong with this request {album_link} : {e}")
      return ""

def write_to_csv(LABEL_LINKS):
   for label_link in LABEL_LINKS:
      label_link = label_link.split("?")[0]  # remove everything after "?"
      label_name = get_label_name(label_link)
      if label_name == None:
         print(f"invalid label url: {label_link}")
         return
      label_link_music = get_label_catalogue_link(label_link)

      # get label page content
      soup = fetch_page_soup(label_link_music)

      # create a csv file
      with open(f"{label_name}.csv", "w", newline = "", encoding = "utf-8") as f: 
         writer = csv.writer(f)
         # header
         if INCLUDE_RELEASE_DATE:
            header = [ "Artist", "Album", "Date", "Link" ]  
         else:
            header = [ "Artist", "Album", "Link" ] 
         writer.writerow(header)
         
         def parse_grid(grid):
            album_containers = grid.find_all("li")

            for container in album_containers:
               album_link = container.a.get("href")
               album_link = album_link.split("?")[0]
               if album_link[0] == "/":
                  # complete the relative link
                  album_link = get_label_clean_link(label_link) + album_link

               artist = container.a.p.span.text.strip()
               title = container.a.p.find(string = True, recursive = False).strip()
   
               if INCLUDE_RELEASE_DATE:
                  # fetch release date from album page
                  date = get_release_date(album_link)
                  # wait a random interval before sending the next album request
                  interval = random.randint(WAIT_INTERVAL_MIN, WAIT_INTERVAL_MAX) 
                  print(f"sleeping for {interval} seconds... \n")
                  time.sleep(interval)
                  row = [ artist, title, date, album_link ]
               else:
                  row = [ artist, title, album_link ]

               print(f"writing new row... {row} \n")
               writer.writerow(row) 

         if soup:
            # parse all albums
            music_grid = soup.find(id = "music-grid")
            if music_grid:
               parse_grid(music_grid)
            else:
               print(f"｡ﾟ･ (>_<) ･ﾟ｡ label music grid not found for {label_link_music}")

            # some labels have featured albums in a separate container
            featured_grid = soup.find("ol", class_="featured-grid featured-items featured-music occupied")
            if featured_grid:
               parse_grid(featured_grid)
         else:
            print(f"｡ﾟ･ (>_<) ･ﾟ｡ empty response for {label_link_music}")

      # wait a random interval before sending the next label request
      interval = random.randint(WAIT_INTERVAL_MIN, WAIT_INTERVAL_MAX) 
      print(f"sleeping for {interval} seconds... \n")
      time.sleep(interval)

   # quit driver when done with all labels 
   driver.quit()

####### utilities #######

# get label name from the url
def get_label_name(label_link):
   return label_link.split("https://")[1].split(".bandcamp.com")[0]

# in case catalogue page is not shown by default
def get_label_catalogue_link(label_link):
   if not label_link.endswith("/music") or label_link.endswith("/music/"):
         if label_link.endswith("/"):
            return label_link + "music"
         else:
            return label_link + "/music"
   else:
      return label_link

# clean label base url in case album links are relative links
def get_label_clean_link(label_link):
   if label_link.endswith("/music"):
      return label_link[0:-6]
   elif label_link.endswith("/music/"):
      return label_link[0:-7]
   else:
      return label_link

if __name__ == "__main__":
   write_to_csv(LABEL_LINKS)