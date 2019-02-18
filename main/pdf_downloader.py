import os
from urllib.request import urlopen, Request
import re
from bs4 import BeautifulSoup
import urllib.parse

base_url = 'https://www.infosys.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                  'Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

regex = r"(investors|investorrelations|investor-relations)"
pdf_urls = []
level = 0


def get_pfd_files(url):
    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        html_text = response.read()
        soup = BeautifulSoup(html_text, 'html.parser')
        a_tags = soup.findAll('a', href=True)

        compile_regex = re.compile(regex, re.I)
        if a_tags:
            for a_tag in a_tags:
                match = compile_regex.search(a_tag['href'])
                if a_tag['href'].endswith('.pdf') and 'javascript' not in a_tag['href'] and len(
                        a_tag['href']) > 20 and match is not None:
                    pdf_urls.append(urllib.parse.urljoin(base_url, a_tag['href']))

    except Exception as e:
        raise e


def download_pdf(download_url):
    try:
        print("Download Url  :::", download_url)
        response = urlopen(download_url)
        for title in download_url.split('/'):
            if title.endswith('.pdf'):
                pdf_title = title
        if not os.path.exists('pdf'):
            os.makedirs('pdf')
        file = open("pdf/{}".format(pdf_title), 'wb')
        file.write(response.read())
        file.close()
        print("Completed")
    except Exception as e:
        raise e


def main():
    get_pfd_files(base_url)
    for url in pdf_urls:
        download_pdf(url)
        exit(0)


if __name__ == "__main__":
    main()
