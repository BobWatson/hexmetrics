from flask import Flask, url_for, render_template, flash,request, redirect
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_user, logout_user, current_user, login_required

from SnippetView import Snippets

class ToolsView(FlaskView):
    
    def __init__(self):
        super(ToolsView, self).__init__()
    
    def index(self):
        snippets = Snippets.getSnippetsForPage(request.endpoint)
        return render_template('tools.html', snippets=snippets);
    
    @route('resourceDraw', methods=['GET', 'POST'])
    def resourceDraw(self):
        from tools_resourceDraw import ResourceForm, ResourceCalculator
        form = ResourceForm()
        snippets = Snippets.getSnippetsForPage(request.endpoint)

        if request.method == 'POST' and form.validate_on_submit():
            types = []
            for x in range(0,len(form.resource_types)):
                types.append({'name': form.resource_types_names[x].data,
                              'num': form.resource_types[x].data,
                              })
            table = ResourceCalculator.resourceTable(
                                                     form.decksize.data, 
                                                     form.resourcesInDeck.data, 
                                                     form.turns.data, 
                                                     form.turn_one_draw.data, 
                                                     types, 
                                                     form.accumulate.data,
                                                     form.elim_unplayable.data
                                                     )
            return redirect(url_for('ToolsView:resourceLink', string=ResourceCalculator.resourceLinkfromForm(form)))
            
        return render_template('tools/resource_draw.html', snippets=snippets, form = form, table=None);

    @route('r/<string>')
    def resourceLink(self, string):
        from tools_resourceDraw import ResourceCalculator
        snippets = Snippets.getSnippetsForPage('ToolsView:resourceDraw')
        return ResourceCalculator.urlFromResourceLink(string, snippets)
        
    @route('cardJS')
    def cardJS(self):
        from tools_cardHoverJS import CardLibrary
        cl = CardLibrary('http://hexmetrics.ni.tl/static/all_cards.html', rebase_url='http://hextcg.gamepedia.com/', rebase_img_url=url_for('static', filename='img/card-icons'))
        return render_template('tools/card_hover_js.html', table=cl.cardtable)
    
    @route('cardJSFrame')
    def getSingleCardFrame(self):
        url = request.args.get('url')
        from models import Cards
        card = Cards.query.filter_by(url = url).first() 
        return render_template('tools/card_frame.html', card=card)