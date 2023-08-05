#!/usr/bin/env python3
import mechanicalsoup

def go_onion(query):
    output = []
    # Connecting to torch
    browser = mechanicalsoup.StatefulBrowser()
    browser.set_user_agent('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0')
    browser.open(f"https://vidalia.io/search?query={query}")

    # Crawler
    def read_urls():
        urls = browser.get_current_page().select('div.result a')
        if len(urls) > 0:
            for link in urls:
                output.append(link.get('href'))
            return output

    read_urls()
    return output


