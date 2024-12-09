from urllib.request import urlopen
from link_finder import LinkFinder
from general import create_project_dir, create_data_files, file_to_set, set_to_file


class Spider:
    # Class Variables (shared across all instances)
    project_name = ""
    base_url = ""
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        self.boot()
        self.crawl_page("First spider", Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(f"{thread_name} now crawling: {page_url}")
            print(f"Queue: {len(Spider.queue)} | Crawled: {len(Spider.crawled)}")
            try:
                links = Spider.gather_links(page_url)
                Spider.add_links_to_queue(links)
                Spider.queue.remove(page_url)  # Only remove after successfully gathering links
                Spider.crawled.add(page_url)
                Spider.update_files()
            except Exception as e:
                print(f"Error while crawling {page_url}: {e}")

    @staticmethod
    def gather_links(page_url):
        html_string = ""
        try:
            response = urlopen(page_url)
            if "text/html" in response.getheader("Content-Type"):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8", errors="ignore")  # Added error handling for decoding
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(f"Error: Cannot crawl page {page_url} | {e}")
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)  # Corrected to use queue_file
        set_to_file(Spider.crawled, Spider.crawled_file)  # Corrected to use crawled_file
