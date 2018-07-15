import os

import requests
from bs4 import BeautifulSoup, SoupStrainer

_BASE_URL = 'https://easyonhold.com/'
_SAMPLES_BASE = 'http://easyonhold.com/samples/hold-messages/'
_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
_FILE_DIR = os.path.join(_BASE, 'hold_audio')

hold_samples_req = requests.get(_SAMPLES_BASE)
hold_links = BeautifulSoup(hold_samples_req.text, 'html.parser',
                        parse_only=SoupStrainer('a'))
category_links = set()
for link in hold_links:
    if link.has_attr('href') and _SAMPLES_BASE in link['href']:
        category_links.add(link['href'])

audio_file_links = set()

def get_audio_files(cat_link, link_set):
    cat_req = requests.get(cat_link)
    cat_parse = BeautifulSoup(cat_req.text, 'html.parser',
                            parse_only=SoupStrainer('a'))
    for link in cat_parse:
        if link.has_attr('title') and 'Preview Song' in link['title']:
            prefix_len = len('../../../')
            link_set.add(link['data-file_uri'][prefix_len:])

def download_file(link):
    filename = link.split('/')[-1]
    full_path = os.path.join(_FILE_DIR, filename)
    full_link = _SAMPLES_BASE + link
    file_req = requests.get(full_link, stream=True)
    with open(full_path, 'wb') as af:
        for chunk in file_req.iter_content(chunk_size=1024):
            af.write(chunk)

for cl in category_links:
    get_audio_files(cl, audio_file_links)

for afl in audio_file_links:
    download_file(afl)
