from django.shortcuts import render
from article import Scraper
# Create your views here.
# Very hard-coded, but it'll do for now
def scrape():
    HC_PREDEFINED = ['https://www.theguardian.com/politics']
    scraper = Scraper(HC_PREDEFINED[0], "Coronavirus")
    scraper.search()