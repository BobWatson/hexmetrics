from flask import Flask, url_for, render_template, redirect, request, abort
from flask.ext.classy import FlaskView, route

from flask.ext.login import current_user, login_required

from models import BlogPosts, BlogCategory
from SnippetView import Snippets

import twitter

from main import app

def getTweetsForUser(user, count):
    import datetime
    api = twitter.Api(consumer_key=app.config['TWITTER_CONSUMER_KEY'],
                      consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
                      access_token_key=app.config['TWITTER_ACCESS_TOKEN_KEY'],
                      access_token_secret=app.config['TWITTER_ACCESS_TOKEN_SECRET']
                      )
    statuses = api.GetUserTimeline('HEXMetrics', count=count)
    ret = []
    for tweet in statuses:
        time = datetime.datetime.fromtimestamp(int(tweet.created_at_in_seconds))
        ret.append({'text': tweet.text,
                    'time': time,
                    'id': tweet.id,
                    })
    return ret

class BlogData():
    @staticmethod
    def topPosts(num):
        posts=BlogPosts.query.order_by('created_date desc').paginate(1,num,False).items;
        return posts
    
    @staticmethod
    def categories():
        categories = BlogCategory.query.order_by('name asc');
        list = []
        for category in categories:
            item = {'name': category.name,
                    'id': int(category.id)
                    }
            list.append(item)
        return list

class BlogView(FlaskView):
    snippets = None
    tweets = getTweetsForUser('HEXMetrics', 5)
    
    def __init__(self):
        super(BlogView, self).__init__()
        self.snippets = Snippets.getSnippetsForPage(u'BlogView:index')
    
    def index(self):
        posts=BlogPosts.query.order_by('created_date desc').paginate(1,5,True)
        return render_template('blog.html', posts=posts, snippets=self.snippets, title='Blog', categories=BlogData.categories(), tweets=self.tweets);
    
    @route('p/<int:num>')
    def page(self,num):
        if num == 1:
            return redirect(url_for('BlogView:index'))
        posts=BlogPosts.query.order_by('created_date desc').paginate(num,5,True)
        return render_template('blog.html', posts=posts, snippets=self.snippets, title='Blog :: %s' % num, categories=BlogData.categories(), tweets=self.tweets);
    
    @route('n/<string:slug>')
    def postBySlug(self, slug):
        posts=BlogPosts.query.filter(BlogPosts.slug==slug).order_by('created_date desc').paginate(1,1,True)
        if len(posts.items) == 0:
            abort(404)
        return render_template('blog.html', posts=posts, snippets=self.snippets, title=posts.items[0].title, categories=BlogData.categories(), tweets=self.tweets);
    
    @route('c/<cat>')
    def postsByCategory(self, cat, num = 1):
        posts=BlogPosts.query.filter(BlogPosts.category_id==cat).order_by('created_date desc').paginate(num,5,True)
        if len(posts.items) == 0:
            abort(404)
        return render_template('blog.html', posts=posts, snippets=self.snippets, title='Blog', categories=BlogData.categories(), cat=cat, tweets=self.tweets);
    
    @route('c/<cat>/<num>')
    def postsByCategoryPage(self, cat, num):
        return self.postsByCategory(cat, num=int(num))
    
    @route('atom')
    def atom(self):
        posts=BlogPosts.query.order_by('created_date desc').paginate(1,10,True)
        return render_template('atom.xml', posts=posts)