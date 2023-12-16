# bandcamp-label-scraper
saves a label's catalogue to a csv file<br>
currently includes artist name, album title, release date, and album link<br>

## usage

### set up
- put label(s) to scrape in `label_links`
- adjust proxy config accordingly
- if u want release date included in the result, set `include_release_date` to `True` 

### run
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
<br>
or double click run.cmd for windows