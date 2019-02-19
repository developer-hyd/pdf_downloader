# ------------------------------------------------------------------
# FileName    : pdf_downloader.py
# Input       : List of urls's in main() routine
# Description : Crawl all links from given url and check
#               against regex to get relevant pdf links.
#               Downloaded pdf are store in pdf directory
# -------------------------------------------------------------------

import os
from urllib.request import urlopen, Request
import re
from bs4 import BeautifulSoup
import urllib.parse
import logging
import ssl

# Logger configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Downloader")

ssl_context = ssl._create_unverified_context()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                  'Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

regex = r"(investors|investorrelations|investor-relations)"
level = 0


def get_pfd_urls(url, filtering=False):
    pdf_urls = []
    try:
        url = convert_url(url)
        logger.info("Fetching pdf url's for : {}".format(url))
        request = Request(url, headers=headers)
        response = urlopen(request, context=ssl_context)
        html_text = response.read()
        soup = BeautifulSoup(html_text, 'html.parser')
        a_tags = soup.findAll('a', href=True)
        compile_regex = re.compile(regex, re.I)
        if a_tags:
            for a_tag in a_tags:
                if filtering:
                    match = compile_regex.search(a_tag['href'])
                    if a_tag['href'].endswith('.pdf') and 'javascript' not in a_tag['href'] and len(
                            a_tag['href']) > 20 and match is not None:
                        pdf_urls.append(urllib.parse.urljoin(url, a_tag['href'].replace(' ', '%20')))
                else:
                    if a_tag['href'].endswith('.pdf') and 'javascript' not in a_tag['href'] and len(
                            a_tag['href']) > 20:
                        pdf_urls.append(urllib.parse.urljoin(url, a_tag['href'].replace(' ', '%20')))
        pdf_urls = list(set(pdf_urls))
        logging.info("PDF download url's found : {}".format(len(pdf_urls)))
        return pdf_urls
    except Exception as e:
        logging.exception(e)


def download_pdf(download_url):
    try:
        pdf_title = download_url + '.pdf'
        logging.info("PDF download url : {} ".format(download_url))
        logging.info("Downloading pdf ...")
        response = urlopen(download_url, context=ssl_context)
        for title in download_url.split('/'):
            if title.endswith('.pdf'):
                pdf_title = title.replace('%20', '-')
        if not os.path.exists('pdf'):
            os.makedirs('pdf')
        if int(response.headers['content-length']) > 0 and response.headers['content-type'].count('application/pdf'):
            file = open("pdf/{}".format(pdf_title), 'wb')
            file.write(response.read())
            file.close()
            logging.info(
                "Downloaded file : {} || file-size : {} KB".format(pdf_title, response.headers['content-length']))
    except Exception as e:
        logging.exception(e)


def convert_url(url):
    if url.startswith('http://'):
        return url
    if url.startswith('https://'):
        return url
    if url.startswith('www'):
        return 'http://' + url


# update url list here ....
def main():
    urls = ['http://www.drdgold.com/investors-and-media',
            'www.gazauto.gazprom.ru/aktsioneram_i_investoram/informatsiya/Godovye_otchety/',
            'https://www.investec.com/en_int/welcome-to-investec/about-us/investor-relations/financial-information.html',
            'http://www.suranatele.com/annual-reports.html',
            'www.cae.com/investors/financial-reports/',
            'https://www.sec.gov/Archives/edgar/data/908259/000119312518119206/0001193125-18-119206-index.htm',
            'investor.telecom.co.nz/phoenix.zhtml?c=91956&p=irol-reportsAnnual',
            'www.lamsoon.co.th/investor/investor_new_en.php',
            'http://www.omholdingsltd.com/ir_report.htm',
            'https://www.borneoaqua.com.my/invest_rel/ann_reports.html',
            'www.b-sophia.co.jp/IR/irinfo/irmaterial.html',
            'http://www.refiningnz.com/investor-centre/reports--announcements/annual-reports.aspx',
            'http://www.accretech.jp/english/ir/library/index.html',
            'tenplay.com.au/corporate/invest',
            'www.smcon.co.jp/en/investor/index.html',
            'www.asahi-kasei.co.jp/asahi/en/ir/library/financial_briefing/',
            'www.acom.co.jp/corp/english/ir_index.html',
            'http://www.mcnex.com/page/sub3_02.html',
            'http://www.cellbiotech.com/en/ir'
            ]
    for url in urls:
        pdf_urls = get_pfd_urls(url, filtering=False)
        if pdf_urls:
            for pdf_url in pdf_urls:
                download_pdf(pdf_url)


if __name__ == "__main__":
    main()
