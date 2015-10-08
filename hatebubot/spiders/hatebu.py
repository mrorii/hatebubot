# -*- coding: utf-8 -*-

import urllib

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from hatebubot.items import HatebuEntry


def convert_to_int_if_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def generate_paginated_urls(params):
    for of in xrange(0, params['num_hits'], params['window']):
        yield 'http://b.hatena.ne.jp/search/tag?{0}'.format(urllib.urlencode({
            'safe': params['safe'],
            'q': params['tag'].encode('utf8'),
            'users': params['users'],
            'of': of,
        }))


class HatebuSpider(CrawlSpider):
    name = "hatebu"
    allowed_domains = ["b.hatena.ne.jp"]
    download_delay = 1.0

    params = {
        'tag': u'ラーメン',
        'users': 30,
        'safe': 'off',
        'num_hits': 5367,
        'window': 40,
    }

    start_urls = generate_paginated_urls(params)

    def parse(self, response):
        selector = Selector(response)

        entries = []

        for result in selector.xpath("//li[@class='search-result']"):
            entry = HatebuEntry()

            is_ad = bool(result.xpath("p[@class='search-native-ad-text']"))
            if is_ad:
                continue

            title = result.xpath(".//h3[1]/a/@title").extract()[0]
            url = result.xpath(".//h3[1]/a/@href").extract()[0]
            tags = result.xpath(".//div/div[@class='tags']/a/text()").extract()
            category = result.xpath(".//div[@class='entryinfo']/a[1]/text()").extract()[0]
            num_users = convert_to_int_if_int(result.xpath(".//span[@class='users']/strong/a/span/text()").extract()[0])
            create_date = result.xpath(".//div[@class='entryinfo']/blockquote/span[@class='created']/text()").extract()[0]

            entry['title'] = title
            entry['url'] = url
            entry['tags'] = tags
            entry['category'] = category
            entry['num_users'] = num_users
            entry['create_date'] = create_date

            entries.append(entry)

        return entries
