# -*- coding: utf-8 -*-
# FeedCrawler
# Projekt von https://github.com/rix1337

import feedcrawler.sites.shared.content_all as shared_blogs
from feedcrawler.config import CrawlerConfig
from feedcrawler.db import FeedDb
from feedcrawler.sites.shared.internal_feed import add_decrypt_instead_of_download
from feedcrawler.sites.shared.internal_feed import ww_feed_enricher
from feedcrawler.sites.shared.internal_feed import ww_get_download_links
from feedcrawler.sites.shared.internal_feed import ww_post_url_headers


class BL:
    _SITE = 'WW'
    SUBSTITUTE = r"[&#\s/]"

    def __init__(self, filename):
        self.hostnames = CrawlerConfig('Hostnames')
        self.url = self.hostnames.get('ww')
        self.password = self.url.split('.')[0]

        if "List_ContentAll_Seasons" not in filename:
            self.URL = 'https://' + self.url + "/ajax" + "|/cat/movies|p=1&t=c&q=5"
        else:
            self.URL = 'https://' + self.url + "/ajax" + "|/cat/series|p=1&t=c&q=9"
        self.FEED_URLS = [self.URL]

        self.config = CrawlerConfig("ContentAll")
        self.feedcrawler = CrawlerConfig("FeedCrawler")
        self.filename = filename
        self.pattern = False
        self.db = FeedDb('FeedCrawler')
        self.hevc_retail = self.config.get("hevc_retail")
        self.retail_only = self.config.get("retail_only")
        self.hosters = CrawlerConfig("Hosters").get_section()
        self.hoster_fallback = self.config.get("hoster_fallback")

        search = int(CrawlerConfig("ContentAll").get("search"))
        i = 2
        while i <= search:
            if "List_ContentAll_Seasons" not in filename:
                page_url = self.URL.replace("|p=1", "|p=" + str(i))
                if page_url not in self.FEED_URLS:
                    self.FEED_URLS.append(page_url)
                i += 1
            else:
                page_url = self.URL.replace("|p=1", "|p=" + str(i))
                if page_url not in self.FEED_URLS:
                    self.FEED_URLS.append(page_url)
                i += 1
        self.cdc = FeedDb('cdc')

        self.last_set_all = self.cdc.retrieve("ALLSet-" + self.filename)
        self.headers = {'If-Modified-Since': str(self.cdc.retrieve(self._SITE + "Headers-" + self.filename))}

        self.last_sha = self.cdc.retrieve(self._SITE + "-" + self.filename)
        settings = ["quality", "search", "ignore", "regex", "cutoff", "enforcedl", "crawlseasons", "seasonsquality",
                    "seasonpacks", "seasonssource", "imdbyear", "imdb", "hevc_retail", "retail_only", "hoster_fallback"]
        self.settings = []
        self.settings.append(self.feedcrawler.get("english"))
        self.settings.append(self.feedcrawler.get("surround"))
        self.settings.append(self.hosters)
        for s in settings:
            self.settings.append(self.config.get(s))
        self.search_imdb_done = False
        self.search_regular_done = False
        self.dl_unsatisfied = False

        self.get_feed_method = ww_feed_enricher
        self.get_url_method = ww_post_url_headers
        self.get_url_headers_method = ww_post_url_headers
        self.get_download_links_method = ww_get_download_links
        self.download_method = add_decrypt_instead_of_download

        try:
            self.imdb = float(self.config.get('imdb'))
        except:
            self.imdb = 0.0

    def periodical_task(self):
        shared_blogs.periodical_task(self)
