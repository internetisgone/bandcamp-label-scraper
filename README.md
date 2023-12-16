# bandcamp-label-scraper
saves a label's catalogue to a csv file<br>
currently supports artist name, album title, release date, and album link<br>

## usage

### set up
in `main.py`,
- put label(s) to scrape in `label_links`
- adjust proxy port and address accordingly
- set `include_release_date` to `True` to include release date in the result csv

### run
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
<br>
or double click run.cmd for windows