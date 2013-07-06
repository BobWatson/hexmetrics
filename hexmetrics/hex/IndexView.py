from flask import Flask, url_for, render_template, flash,request, redirect, send_file, abort
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_user, logout_user, current_user, login_required

from BlogView import BlogData
from SnippetView import Snippets

class IndexView(FlaskView):
    def index(self):
        snippets = Snippets.getSnippetsForPage(request.endpoint)
        posts = BlogData.topPosts(3)
        return render_template('index.html', top_posts=posts, snippets=snippets);

    @route('/favicon.ico')
    def favicon(self):
        return redirect(url_for('static', filename='favicon.ico'))

    @route('page/<snippet_name>')
    def pageForSnippetName(self, snippet_name):
        return render_template('basic.html',snippet=Snippets.getSnippetByName(snippet_name));
    
    @route('/cached_file')
    def returnCachedFile(self):
        import os, hashlib, requests, urlparse
        from config import CACHE_FILE_LOCATION, CACHE_URL_LOCATION
        
        url = request.args.get('url')
        ext = os.path.splitext(urlparse.urlparse(url).path)[1]
        
        if '..' in url or url.startswith('/'):
            abort(500)

        url_name = '%s%s' % (hashlib.sha224(url).hexdigest(),ext)
        file_name = os.path.join(CACHE_FILE_LOCATION,url_name)
        if url is not None:
            try:
                with open(file_name): pass
                return redirect(url_for('static', filename = '%s/%s'%(CACHE_URL_LOCATION,url_name)))
            except IOError:
                req = requests.get(url)
                with open(file_name, "wb") as r:
                    r.write(req.content)

                return redirect(url_for('static', filename = '%s/%s'%(CACHE_URL_LOCATION,url_name)))
                
        abort(404)
            
