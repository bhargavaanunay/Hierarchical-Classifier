class Crawler:
    
    '''This is a crawler for http://timesofindia.indiatimes.com (Times of India).
    This crawler is topic-oriented and its purpose is to crawl
    and fetch only those articles that belong to the topic passed as argument.
    It takes advantage of the topic-oriented URL structure of TOI
    and specific markup tags for the news content. The topic to be passed as sp_category.
    Its structure should be broad-classification/specific-classification.
    For example: sports/cricket
    The crawler requires the root directory of the Corpus as root_path
    and assumes that the directory root_path/sp_category exists.
    The fetched articles are stored as txt files including the title and the body of the article.
    The names of the txt files will be 1.txt, 2.txt, etc.
    A limit on the number of articles can be specified. By default, it is 100.
    The file number and the title of the article are printed on the console as they get saved.
    The title is marked-up with [TITLE] and [/TITLE] in the saved files. 
    
    '''
    
    def __init__(self, seed, sp_category, root_path):
        self.seed = seed
        self.links = set([seed])
        self.sp_category = sp_category
        self.path = root_path
        if self.path[-1] != '/':
                self.path = self.path + '/'
        
    def get_page(self, url):
        try:
            import urllib
            return urllib.urlopen(url).read()
        except:
            return ""
    
    def union(self, p, links):
        for x in links:
            if x not in self.links:
                p.append(x)
                self.links.add(x)
            
    def get_all_links(self, content):
        p = []
        idx = content.find("href=")
        while idx != -1:
            start_link = content.find("\"", idx)
            end_link = content.find("\"", start_link + 1)
            start_link = start_link + 1
            link = content[start_link:end_link]
            if link.find(self.sp_category) != -1 and link.find('articleshow') != -1 and link.endswith('.cms'):
                if link.find("http", start_link) == -1:
                    link = "http://timesofindia.indiatimes.com" + link
                p.append(link)
            content = content[end_link:]
            idx = content.find("href=")
        return p
    
    def output(self, content, file_counter):
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
            file_name = self.path + self.sp_category + '/' + str(file_counter) + '.txt'
            f = open(file_name, 'w')
            with f:
                f.write(text)
                print str(file_counter) + "\t" + title
                return True
        return False
    
    def crawl(self, limit=100): # limit = no. of pages to crawl, else will go infinitely
        file_counter = 1
        to_crawl = [self.seed]
        crawled = set([])
        i = 0
        while i < len(to_crawl) and limit > 0:
            page = to_crawl[i]
            i = i + 1
            if page not in crawled:
                content = self.get_page(page)
                outlinks = self.get_all_links(content)
                self.union(to_crawl, outlinks)
                if i == 1:
                    continue # Assuming that the seed URL is a topic page and not an article page
                if self.output(content, file_counter):
                    file_counter = file_counter + 1
                    limit = limit - 1
                crawled.add(page)