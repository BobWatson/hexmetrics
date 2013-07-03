from flask import Flask, url_for, render_template, flash,request, redirect
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
