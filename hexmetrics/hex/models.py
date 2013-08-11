from main import db
from config import TABLE_PREFIX

#
# import the CryptContext class, used to handle all hashing...
#
from passlib.context import CryptContext

#
# create a single global instance for your app...
#
pwd_context = CryptContext(
    # replace this list with the hash(es) you wish to support.
    # this example sets pbkdf2_sha256 as the default,
    # with support for legacy des_crypt hashes.
    schemes=["pbkdf2_sha256", "des_crypt" ],
    default="pbkdf2_sha256",

    # vary rounds parameter randomly when creating new hashes...
    all__vary_rounds = 0.1,

    # set the number of rounds that should be used...
    # (appropriate values may vary for different schemes,
    # and the amount of time you wish it to take)
    pbkdf2_sha256__default_rounds = 8000,
    )

ROLE_USER = 0
ROLE_ADMIN = 1

USER_ACTIVE = 1
USER_INACTIVE = 0

class User(db.Model):
    __tablename__ = 'users' if (TABLE_PREFIX == '') else '%s_users' % TABLE_PREFIX
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), index = True, unique = True)
    realname = db.Column(db.String(128), index = True)
    email = db.Column(db.String(128), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    _password = db.Column('password', db.String(128))
    signUpDetails = db.relationship("UserSignupDetails", backref=db.backref('usersignups' if (TABLE_PREFIX == '') else '%s_usersignups' % TABLE_PREFIX))
    active = db.Column(db.SmallInteger, default = USER_INACTIVE)
    
    @property
    def displayname(self):
        if self.username != '':
            return self.username;
        else:
            return ''
    
    @property
    def password(self):
        return '<hashed>';
    
    @password.setter
    def password(self, value):
        self._password = pwd_context.encrypt(value)
    
    def is_admin(self):
        if self.role == ROLE_ADMIN:
            return True
        else:
            return False
        
    def checkPassword(self, inp):
        return pwd_context.verify(inp,self._password);

    def __repr__(self):
        return '<User %r>' % (self.username)
    
    def is_authenticated(self):
        return True; 

    def is_active(self):
        if self.active == USER_ACTIVE:
            return True
        return False;

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    
class UserSignupDetails(db.Model):
    __tablename__ = 'usersignups' if (TABLE_PREFIX == '') else '%s_usersignups' % TABLE_PREFIX
    id = db.Column(db.Integer, primary_key = True)
    detailsFor = db.Column(db.Integer, db.ForeignKey('users' if (TABLE_PREFIX == '') else '%s_users' % TABLE_PREFIX+'.id'))
    signupKey = db.Column(db.String(32))
    destPage = db.Column(db.String(128))

class BlogPosts(db.Model):
    from datetime import datetime
    __tablename__ = 'blogposts' if (TABLE_PREFIX == '') else '%s_blogposts' % TABLE_PREFIX
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Unicode(128))
    body = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime)
    slug = db.Column(db.String(128), unique=True)
    
    category_id = db.Column(db.Integer, db.ForeignKey('blogcategory' if (TABLE_PREFIX == '') else '%s_blogcategory' % TABLE_PREFIX+'.id'))
    category = db.relationship('BlogCategory',
                               backref=db.backref('blogcategory' if (TABLE_PREFIX == '') else '%s_blogcategory' % TABLE_PREFIX, lazy='dynamic'))
    
    def __init__(self, title = '', body = '', created_date=datetime.utcnow(), category_id=1, slug=''):
        self.title = title
        self.slug = slug
        self.body = body
        self.created_date = created_date
        self.category_id = category_id
    
    def __repr__ (self):
        return self.title;
        
class BlogCategory(db.Model):
    __tablename__ = 'blogcategory' if (TABLE_PREFIX == '') else '%s_blogcategory' % TABLE_PREFIX
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique = True)
    
    def __init__(self, name = ""):
        self.name = name

    def __repr__ (self):
        return self.name;
    
class SnippetLibrary(db.Model):
    from datetime import datetime
    __tablename__ = 'snippets' if (TABLE_PREFIX == '') else '%s_snippets' % TABLE_PREFIX
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(128), unique = True)
    for_page = db.Column(db.Unicode(128)) 
    title = db.Column(db.Unicode(128))
    body = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime)
    
    def __init__(self, title = '', body = '', created_date=datetime.utcnow(), name = ''):
        self.name = name
        self.title = title
        self.body = body
        self.created_date = created_date
    
    def __repr__ (self):
        return self.name;
    
class Cards(db.Model):
    __tablename__ = 'cards' if (TABLE_PREFIX == '') else '%s_cards' % TABLE_PREFIX
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText)
    colour = db.Column(db.Unicode(80))
    cost = db.Column(db.Integer)
    card_type = db.Column(db.Unicode(80))
    threshold_icons = db.Column(db.UnicodeText)
    rarity = db.Column(db.Unicode(80))
    description = db.Column(db.UnicodeText)
    url = db.Column(db.UnicodeText)
    img_url = db.Column(db.UnicodeText)
    
    def __init__ (self, name='',colour='',cost='',card_type='',threshold_icons='',rarity='',description='',url='', img_url=''):
        import urllib
        self.name = name
        self.colour = colour
        self.cost = cost
        self.card_type = card_type
        self.threshold_icons = threshold_icons
        self.rarity = rarity
        self.description = description
        self.url = url = '%s%s' % (url[0:url.rfind('/')],urllib.quote(url[url.rfind('/'):]))
        self.img_url = img_url
        
    def __repr__ (self):
        return self.name;