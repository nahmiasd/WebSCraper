# Web Scraper
## Requirements
This project requires Python 3.10.
To install all other required package use:
```bash
pip install -r requirements.txt
```
## Run Instructions
The main script is located at src/main.py. 

Use the argument ``` -i ``` to specify a full path to a text file containing seed urls.
If not specified, the program will use the default "example_seed_urls.txt"

User the argument ```-s``` to specify a maximum number of urls to scrape (optional but recommended).

## Run Example
```bash
WebScraper/src/main.py -i "path/to/seed_ulrs.txt" -s 300
```