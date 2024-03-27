# bandcamp-label-scraper
simple scraper to save a label's catalogue to a csv file<br>
currently supports artist name, album title, release date, and album link<br>

## usage

### set up
in `main.py`,
- put label(s) to scrape in `LABEL_LINKS`
- adjust `PROXY` settings accordingly
- set `INCLUDE_RELEASE_DATE` to `True` to include release date in the csv (date can only be obtained from album page so execution will take longer if set to `True`)

### run
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
<br>
or double click run.cmd for windows