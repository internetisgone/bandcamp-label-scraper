import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# 厂牌的 bandcamp 页面
label_links = [
   "https://sahelsounds.bandcamp.com/music",
   ]  

# 代理服务器的本地监听端口 http / https local listening port 
port = "1087"

# todo
fetch_release_date = False

proxies = {
   "http": f"127.0.0.1:{port}",
   "https": f"127.0.0.1:{port}",
}

# def get_album_info(link):
#    # send a get request
#    response = requests.get(link, proxies = proxies, timeout = 2)
#    # parse html 
#    soup = BeautifulSoup(response.text, "html.parser")
#    # get album data
#    name_section = soup.find(id = "name-section")
#    title = name_section.h2.text.strip()
#    artist = name_section.h3.span.a.text.strip()
#    info_container = soup.find(id = "trackInfoInner")
#    year = info_container.find("div", class_="tralbum-credits").find(string=True, recursive=False).strip()
#    year = year.split("released ")[1]

#    return [ artist, title, year ]
      
def write_to_csv(label_links):
   with open("result.csv", "w", newline = "", encoding = "utf-8") as f: 
      writer = csv.writer(f)

      # csv header
      if fetch_release_date:
         header = [ "Artist", "Album", "Date", "Link" ]  
      else:
         header = [ "Artist", "Album", "Link" ] 
      writer.writerow(header)

      for label_link in label_links:
         # todo if label_link does not end with "/music" or "/music/"
         # append it

         # send a get request
         response_label = requests.get(label_link, proxies = proxies, timeout = 2)
         # parse html 
         soup = BeautifulSoup(response_label.text, "html.parser")

         def parse_grid(grid):
            album_containers = grid.find_all("li")

            for container in album_containers:
               link = container.a.get("href")
               link = link.split("?")[0]    # remove everything after the "?"
               if link[0] == "/":
                  link = label_link + link

               artist = container.a.p.span.text.strip()
               title = container.a.p.find(text=True, recursive=False).strip()

               row = [ artist, title, link ]
               print(f"writing new row... {row} \n")
               writer.writerow(row) 

         featured_grid = soup.find("ol", class_="featured-grid featured-items featured-music occupied")
         if featured_grid:
            parse_grid(featured_grid)

         music_grid = soup.find(id = "music-grid")
         parse_grid(music_grid)

         # wait a random interval before sending the next label request
         interval = random.randint(2, 5) 
         print(f"sleeping for {interval} seconds... \n")
         time.sleep(interval)


if __name__ == '__main__':
   write_to_csv(label_links)