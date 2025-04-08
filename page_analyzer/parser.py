from bs4 import BeautifulSoup


def parse_seo(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.h1.get_text() if soup.h1 else ''
    title = soup.title.get_text() if soup.title else ''
    meta_tag = soup.find("meta", attrs={"name": "description"})
    description = meta_tag.get('content') if meta_tag else ''
    return h1, title, description
