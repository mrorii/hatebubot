# -*- coding: utf-8 -*-
import scrapy


class HatebuSpider(scrapy.Spider):
    name = "hatebu"
    allowed_domains = ["b.hatena.ne.jp"]
    start_urls = (
        'http://www.b.hatena.ne.jp/',
    )

    def parse(self, response):
        pass
