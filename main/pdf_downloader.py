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

import xlrd
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

pdf_types = {'annual': 'AR', 'Corporate': 'AR', 'Transcripts': 'TR', 'Quarterly': 'QR',
             'Presentations': 'IP', 'Filings': 'FL'}


def get_pdf_type(text):
    result = ''
    for pdf_type in pdf_types.items():
        if re.search(pdf_type[0], text, re.IGNORECASE):
            result = pdf_type[1]
    if result:
        return result
    else:
        return 'OTH'


def get_pfd_urls_and_type(url, filtering=False):
    pdf_urls = []
    try:
        url = convert_url(url)
        logging.info("\n")
        logger.info("Fetching pdf url's for : {}".format(url))
        request = Request(url, headers=headers)
        response = urlopen(request, context=ssl_context)
        html_text = response.read()
        soup = BeautifulSoup(html_text, 'html.parser')
        title_text = soup.find('title').text
        doc_type = get_pdf_type(text=title_text)
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
        logging.info("PDF download url's found : {}\n".format(len(pdf_urls)))
        return doc_type, pdf_urls
    except Exception as e:
        logging.exception(e)
        return 'Oth', []


def get_pdf_meta(pdf_type, company_name, company_id, download_url):
    pdf_title = str(company_id) + '_' + str(company_name).replace(' ', '_')
    if pdf_type and pdf_type == 'OTH':
        doc_type = get_pdf_type(text=download_url)
        pdf_title = pdf_title + '_' + doc_type
    for title in download_url.split('/'):
        if title.endswith('.pdf'):
            match = re.match(r'.*([1-3][0-9]{3})', title)
            if match is not None:
                year = match.group(1)
                pdf_title = pdf_title + '_' + year
            pdf_title = pdf_title + '.pdf'
    pdf_folder = company_name.replace(' ', '_')
    return pdf_title, pdf_folder


def download_pdf(download_url, pdf_title, pdf_folder):
    try:
        logging.info("PDF download url : {} ".format(download_url))
        logging.info("Downloading pdf ...")
        response = urlopen(download_url, context=ssl_context)
        if not os.path.exists('pdf'):
            os.makedirs('pdf')
        if not os.path.exists('pdf/{}'.format(pdf_folder)):
            os.makedirs('pdf/{}'.format(pdf_folder))
        if int(response.headers['content-length']) > 0 and response.headers['content-type'].count('application/pdf'):
            file = open("pdf/{}/{}".format(pdf_folder, pdf_title), 'wb')
            file.write(response.read())
            file.close()
            logging.info(
                "Downloaded PDF Name : {} || PDF-size : {} KB\n".format(pdf_title, response.headers['content-length']))
    except Exception as e:
        logging.exception(e)


# read excel data and parse inputs for pdf extraction url's
def read_excel(excel_file):
    try:
        rows = []
        header_list = []
        links_data = []
        wb = xlrd.open_workbook(excel_file)
        sheet = wb.sheet_by_index(0)
        logging.info("Reading file-name: {} || sheet-name: {}\n".format(excel_file, sheet.name))
        col = sheet.row(0)

        for header in col:
            header_list.append(header.value)
        for index in range(sheet.nrows):
            if not index == 0:
                rows.append(sheet.row_values(index))
        for row in rows:
            links_data.append(dict(zip(header_list, row)))
        return links_data
    except Exception as e:
        logging.exception(e)


def convert_url(url):
    if url.startswith('http://'):
        return url
    if url.startswith('https://'):
        return url
    if url.startswith('www'):
        return 'http://' + url
    else:
        return 'http://' + url


def main(excel_file):
    try:
        input_data = read_excel(excel_file)
        for data in input_data:
            pdf_type, pdf_urls = get_pfd_urls_and_type(url=data['FilingsLink'], filtering=False)

            if len(pdf_urls):
                for pdf_url in pdf_urls:
                    pdf_title, pdf_folder = get_pdf_meta(pdf_type=pdf_type, company_name=data['CompanyName'],
                                                         company_id=str(data['CompanyId']).rstrip('0').rstrip('.'),
                                                         download_url=pdf_url)
                    download_pdf(download_url=pdf_url, pdf_title=pdf_title, pdf_folder=pdf_folder)

    except Exception as e:
        logging.exception(e)

