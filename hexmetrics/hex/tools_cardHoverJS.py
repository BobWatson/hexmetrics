from bs4 import BeautifulSoup
import urllib2
import re
from main import db

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
                cell_num = 0
                for td in tr.find_all('td'):
                    row_contents = '%s' % re.sub(r'<td.*?>', r'', td.prettify())
                    row_contents = '%s' % re.sub(r'</td>', r'', row_contents)
                    row_contents = re.sub(r'(<a.*?href=")/(.*?".*?>)', r'\1%s\2'%rebase_url, row_contents)
                    if cell_num == 0:
                        row_contents = row_contents.replace('href', 'class="hex-card" href')
                    row_contents = re.sub(r'(<img .*? src=").*(/.*?".*?>)', r'\1%s\2'%rebase_img_url, row_contents)
                    row_contents = row_contents.strip()
                    row.append(row_contents)
                    cell_num = cell_num + 1
                if len(row) > 0:
                    self.cardtable['cards'].append(row)

    def commitTable(self):
        from models import Cards
        Cards.query.delete()
        i = 0
        print 'CardLibrary Committing...'
        for card in self.cardtable['cards']:
            i = i+1
            
            soup = BeautifulSoup(card[0], 'html5lib')
            name = soup.find('a').get_text().strip()
            url = soup.find('a')['href'].strip()
            img_url = ''
            
            print 'Processing %s of %s (%s)...' % (i, len(self.cardtable['cards']), name)
            
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html5lib')
            for infobox in soup.find_all('table', 'infobox'):
                if infobox.img is not None:
                    img_url = infobox.img['src']
            c = Cards(name=name,colour=card[1],cost=card[2],card_type=card[3],threshold_icons=card[4],rarity=card[5],description=card[6],url=url, img_url=img_url)
            db.session.add(c)
            db.session.commit()