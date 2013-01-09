class Crawler:
    
    '''This is a crawler for http://timesofindia.indiatimes.com (Times of India).
    
    This crawler is topic-oriented and its purpose is to crawl and fetch only
    those articles that belong to the topic passed as argument. It takes
    advantage of the topic-oriented URL structure of TOI and specific markup
    tags for the news content. The topic is to be passed as sp_category.
    Its structure should be broad-classification/specific-classification.
    For example: sports/cricket
    The crawler requires the root directory of the Corpus as root_path and
    assumes that the directory root_path/sp_category exists.
    The fetched articles are stored as txt files including the title and
    the body of the article.
    The names of the txt files will be 1.txt, 2.txt, etc.
    A limit on the number of articles can be specified. By default, it is 100.
    The file number and the title of the article are printed on the console
    as they get saved.
    The title is marked-up with [TITLE] and [/TITLE] in the saved files. 
    
    '''
    
    def __init__(self, seed, sp_category, root_path):
        self.__seed = seed
        self.__links = set([seed])
        self.__sp_category = sp_category
        self.__path = root_path
        if self.__path[-1] != '/':
                self.__path = self.__path + '/'
        
    def __get_page(self, url):
        '''Fetches the contents of the page associated with the URL.
        
        If an exception occurs, "" is returned.
        Otherwise, the contents of the page is returned as str.
        
        '''
        try:
            import urllib
            return urllib.urlopen(url).read()
        except:
            return ""
    
    def __union(self, to_crawl, outlinks):
        '''Adds only new links to the list of URLs to be crawled'''
        for x in outlinks:
            if x not in self.__links:
                to_crawl.append(x)
                self.__links.add(x)
            
    def __get_all_links(self, content):
        '''Returns the list of links on a page that satisfy the criteria given to the crawler.'''
        p = []
        idx = content.find("href=")
        while idx != -1:
            start_link = content.find("\"", idx)
            end_link = content.find("\"", start_link + 1)
            start_link = start_link + 1
            link = content[start_link:end_link]
            if link.find(self.__sp_category) != -1 and link.find('articleshow') != -1 and link.endswith('.cms'):
                if link.find("http", start_link) == -1:
                    link = "http://timesofindia.indiatimes.com" + link
                p.append(link)
            content = content[end_link:]
            idx = content.find("href=")
        return p
    
    def __output(self, content, file_counter):
        '''Stores the extracted news article to a file and prints its title on the screen.
        
        returns True if content is present and is successfully saved on a file;
        returns False otherwise.
        
        '''
        start_title = content.find('<title>')
        end_title = content.find('</title>', start_title + 1)
        title = '[TITLE]' + content[(start_title + 7):end_title] + '[/TITLE]'
        text = title + '\n\n'
        start_tmp = content.find('<tmp>')
        news = None
        if start_tmp != -1:
            end_tmp = content.find('</tmp>', start_tmp + 1)
            news = content[(start_tmp + 5):end_tmp]
        else:
            start_normal = content.find('<div class="Normal"')
            if start_normal != -1:
                end_normal = content.find('</div>', start_normal + 1)
                news = content[(start_normal + 20):end_normal]
        if news is not None:
            text = text + news + '\n'
            file_name = self.__path + self.__sp_category + '/' + str(file_counter) + '.txt'
            f = open(file_name, 'w')
            with f:
                f.write(text)
                print str(file_counter) + "\t" + title
                return True
        return False
    
    def crawl(self, limit=100): # limit = no. of pages to crawl, else will go infinitely
        '''Use this function to start crawling the website.'''
        file_counter = 1
        to_crawl = [self.__seed]
        crawled = set([])
        i = 0
        while i < len(to_crawl) and limit > 0:
            page = to_crawl[i]
            i = i + 1
            if page not in crawled:
                content = self.__get_page(page)
                outlinks = self.__get_all_links(content)
                self.__union(to_crawl, outlinks)
                if i == 1:
                    continue # Assuming that the seed URL is a topic page and not an article page
                if self.__output(content, file_counter):
                    file_counter = file_counter + 1
                    limit = limit - 1
                crawled.add(page)