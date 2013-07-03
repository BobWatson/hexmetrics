from models import SnippetLibrary

class Snippets():
    
    @staticmethod
    def getSnippetByName(name):
        return SnippetLibrary.query.filter(SnippetLibrary.name==name).first();
    
    @staticmethod
    def getSnippetsForPage(name):
        try:
            return SnippetLibrary.query.filter(SnippetLibrary.for_page==name).all();
        except:
            return None