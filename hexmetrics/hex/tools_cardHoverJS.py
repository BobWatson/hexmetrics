from bs4 import BeautifulSoup
import urllib2
import re

class CardLibrary():
    
    cardtable = {'headers': None,'cards': []};
    
    def __init__(self, url, rebase_url, rebase_img_url):

        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html5lib')
        
        for table in soup.find_all('table', 'sortable'):
            headers = []
            for th in table.find_all('th'):
                headers.append(th.get_text().strip())
            self.cardtable['headers'] = headers
            
            for tr in table.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    row_contents = '%s' % re.sub(r'<td.*?>', r'', td.prettify())
                    row_contents = '%s' % re.sub(r'</td>', r'', row_contents)
                    row_contents = re.sub(r'(<a href=")/(.*?".*?>)', r'\1%s\2'%rebase_url, row_contents)
                    row_contents = re.sub(r'(<img .*? src=").*(/.*?".*?>)', r'\1%s\2'%rebase_img_url, row_contents)
                    row.append(row_contents)
                    print row_contents
                if len(row) > 0:
                    self.cardtable['cards'].append(row)