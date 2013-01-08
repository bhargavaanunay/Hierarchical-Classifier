from toi_crawler import Crawler

def main():
    print "Enter seed URL (URL of the topic page and not a specific article):",
    seed = raw_input()
    print "Enter ABSOLUTE path to top folder of Corpus:",
    root_path = raw_input()
    print "Enter specific category:",
    sp_category = raw_input()
    print "Enter limit (0 for infinite):",
    limit_ = int(raw_input())
    sp_crawler = Crawler(seed, sp_category, root_path)
    if limit_ == 0:
        sp_crawler.crawl()
    else:
        sp_crawler.crawl(limit=limit_)

if __name__ == '__main__':
    main()