from tools_cardHoverJS import CardLibrary
import os

cl = CardLibrary('http://hextcg.gamepedia.com/List_of_all_cards', rebase_url='http://hextcg.gamepedia.com/', rebase_img_url='http://hexmetrics.ni.tl/static/img/card-icons')

print 'CardLibrary Initialised...'

cl.commitTable()

print 'Emptying Cache...'

from config import CACHE_FILE_LOCATION

for the_file in os.listdir(CACHE_FILE_LOCATION):
    file_path = os.path.join(CACHE_FILE_LOCATION, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception, e:
        print e
        
print 'Done.\n'