from tools_cardHoverJS import CardLibrary

cl = CardLibrary('http://hexmetrics.ni.tl/static/all_cards.html', rebase_url='http://hextcg.gamepedia.com/', rebase_img_url='http://hexmetrics.ni.tl/static/img/card-icons')

print cl.cardtable['cards'][0]

cl.commitTable()