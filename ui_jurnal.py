from io import StringIO
import requests
from bs4 import BeautifulSoup

from logzero import logger
from tqdm import tqdm

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

url = "http://jurnalpenyakitdalam.ui.ac.id/index.php/jpdi/issue/archive"

def get_issue_list(url):

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    issue_desc = soup.find_all("div", attrs={"class": "issueDescription"})

    issues = []

    for isd in issue_desc:
        links = isd.find_all("a")
        for li in links:
            issues.append(li.get("href"))
    return issues

def get_download_url(issues):

    logger.info("Get download url")

    for issue in tqdm(issues):
        req = requests.get(issue, headers)
        issue_soup = BeautifulSoup(req.content, "html.parser")
        
        get_link = issue_soup.find_all("div", attrs={"class": "tocGalleys"})
        for gl in get_link:
            link = gl.find_all("a")
            
            for i, li in enumerate(link):
                link_article = li.get("href")
                link_downloads = link_article.replace("view", "download")
                r_url = requests.get(link_downloads, allow_redirects = True)
                pdf_url = r_url.url.replace("/", "-")
                
                filename = "jurnal/" + str(pdf_url) + ".pdf"
                with open(str(filename), "wb") as f:
                    f.write(r_url.content)

def processing_pdf():
    output_string = StringIO()

    with open("jurnal/http:--jurnalpenyakitdalam.ui.ac.id-index.php-jpdi-article-download-332-206.pdf", "rb") as pf:
        parser = PDFParser(pf)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    print(output_string.getvalue())

processing_pdf()

# issues = get_issue_list(url)
# get_download_url(issues)