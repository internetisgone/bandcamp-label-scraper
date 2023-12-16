import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# bandcamp label(s) to scrape
label_links = [
   "https://sahelsounds.bandcamp.com/music",
   ]  

# http / https proxy local listening port 
port = "1087"

proxies = {
   "http": f"127.0.0.1:{port}",
   "https": f"127.0.0.1:{port}",
}

# whether to include release date in result.csv
# if set to True this script will take longer to complete execution
# cuz date can only be obtained from album page
include_release_date = False 

def get_label_page(label_link):
   try: 
      # send a get request
      response_label = requests.get(label_link, proxies = proxies, timeout = 2)
      # return soup
      return BeautifulSoup(response_label.text, "html.parser")
   except requests.exceptions.RequestException as e:
      print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went wrong with this request {label_link} : {e}")
      return

def get_release_date(album_link):
   try:
      print(f"getting album info {album_link}")
      response = requests.get(album_link, proxies = proxies, timeout = 2)
      soup = BeautifulSoup(response.text, "html.parser")

      if soup:
         info_container = soup.find(id = "trackInfoInner")
         if info_container:
            date = info_container.find("div", class_="tralbum-credits").find(string=True, recursive=False).strip()
            date = date.split("released ")[1]
            return date
         
      print(f"｡ﾟ･ (>_<) ･ﾟ｡ rlease date not found for {album_link}")
      return ""
   except requests.exceptions.RequestException as e:
      print(f"｡ﾟ･ (>_<) ･ﾟ｡ something went wrong with this request {album_link} : {e}")
      return ""

def write_to_csv(label_links):
   with open("result.csv", "w", newline = "", encoding = "utf-8") as f: 
      writer = csv.writer(f)
      # csv header
      if include_release_date:
         header = [ "Artist", "Album", "Date", "Link" ]  
      else:
         header = [ "Artist", "Album", "Link" ] 
      writer.writerow(header)

      for label_link in label_links:
         # clean up label link
         label_link = label_link.split("?")[0]  # remove everything after "?"
         label_link_music = get_label_catalogue_link(label_link)

         def parse_grid(grid):
            album_containers = grid.find_all("li")

            for container in album_containers:
               album_link = container.a.get("href")
               album_link = album_link.split("?")[0]
               if album_link[0] == "/":
                  # complete the relative link
                  album_link = get_label_clean_link(label_link) + album_link

               artist = container.a.p.span.text.strip()
               title = container.a.p.find(text=True, recursive=False).strip()
   
               if include_release_date:
                  # fetch release date from album page
                  date = get_release_date(album_link)
                  # wait a random interval before sending the next album request
                  interval = random.randint(2, 5) 
                  print(f"sleeping for {interval} seconds... \n")
                  time.sleep(interval)
                  row = [ artist, title, date, album_link ]
               else:
                  row = [ artist, title, album_link ]

               print(f"writing new row... {row} \n")
               writer.writerow(row) 

         # get label page content
         soup = get_label_page(label_link_music)

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
         interval = random.randint(2, 5) 
         print(f"sleeping for {interval} seconds... \n")
         time.sleep(interval)

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

if __name__ == '__main__':
   write_to_csv(label_links)