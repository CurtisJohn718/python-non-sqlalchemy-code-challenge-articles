class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)


    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if hasattr(self, "_title"):
            return  
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            self._title = "Untitled"  


    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        from classes.many_to_many import Author

        if not isinstance(value, Author):
            raise TypeError("Author must be an instance of the Author class.")
        self._author = value


    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        from classes.many_to_many import Magazine

        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be an instance of the magazine class.")
        self._magazine = value 

        
class Author:
    def __init__(self, name):
        self.name = name

    
    @property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self, value):
        if hasattr(self, "_name"):
            return
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters.")
        self._name = value
        

    def articles(self):
        from classes.many_to_many import Article
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        from classes.many_to_many import Article
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles():
            return None
        return list({article.magazine.category for article in self.articles()})

class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value


    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value 


    def articles(self):
        from classes.many_to_many import Article
        return [article for article in Article.all if article.magazine ==self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        author_counts = {}

        for article in self.articles():
            author = article.author
            if author in author_counts:
                author_counts[author] += 1
            else:
                author_counts[author] = 1
        
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None