# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import ItjuziItem

class JuziSpiderSpider(scrapy.Spider):
    name = 'juzi_spider'
    allowed_domains = ['itjuzi.com']

    start_urls = ["http://radar.itjuzi.com/company/" + str(offset) for offset in range(1,10)]

    headers = {
        "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": " gzip, deflate",
        "Accept-Language": " zh-CN,zh;q=0.9",
        "Connection": " keep-alive",
        "Host": " radar.itjuzi.com",
        "Upgrade-Insecure-Requests": " 1",
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }

    cookies = {
        "gr_user_id": "5f1f43ee-bd51-4214-8fab-7aef4978383a",
        "_ga": "GA1.2.192564878.1531916742",
        "MEIQIA_EXTRA_TRACK_ID": "160mMc8qpSeUp6d0UgvFjsTQXvn",
        "acw_tc": "AQAAAOSqN210IQsArR4S2jddA3EWCi44",
        "_gid": "GA1.2.486192863.1532005333",
        "Hm_lvt_1c587ad486cdb6b962e94fc2002edf89": "1531917288,1531917673,1531917750,1532005333",
        "Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89": "1532005333",
        "identity": "695464823%40qq.com",
        "remember_code": "4IFy3oRatz",
        "unique_token": "597521",
        "paidtype": "vip",
        "user-radar.itjuzi.com": "%7B%22n%22%3A%22%5Cu6854%5Cu53cb4606020a44132%22%2C%22v%22%3A2%7D",
        "Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b": "1531917030,1532005348",
        "MEIQIA_VISIT_ID": "17bUXTA3fXZqzKBTJaiOcVxvxSa",
        "gr_session_id_eee5a46c52000d401f969f4535bdaa78": "8f2825b9-be41-42f8-b81f-58a7b4b08483",
        "gr_cs1_8f2825b9-be41-42f8-b81f-58a7b4b08483": "user_id%3A597521",
        "gr_session_id_eee5a46c52000d401f969f4535bdaa78_8f2825b9-be41-42f8-b81f-58a7b4b08483": "true",
        "session": "8ff4e4f3a753ce7183eaa6322df778e6fb8fd38b",
        "Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b": "1532014189",
    }
    def parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url,headers=self.headers,cookies=self.cookies,
                                 callback=self.parse_data, dont_filter=True)

    def parse_data(self,response):
        if response.status == 200:
            item = ItjuziItem()
            soup = BeautifulSoup(response.body, 'lxml')
            try:
                item['name'] = soup.select_one('div[class="company-title"]').select_one('h2').contents[0].strip()
            except:
                item['name'] = None
            item['type'] = soup.select_one('p[class="company-industry"]').select('a')[0].get_text().strip() if soup.select_one('p[class="company-industry"]') else None
            item['home_page'] = soup.select_one('div[class="company-title"]').select_one('h2').contents[1].get_text().strip()
            tag_list = [tag.get_text().strip() for tag in soup.select_one('ul[class="company-tit-tags"]').select('li')[1:]]
            item['tag'] = ", ".join(tag_list)
            item['fullname'] = soup.select("p[class='cont-Introduction']")[0].get_text()[5:]
            item['time'] = soup.select_one('ul[class="cont-news-list"]').select('li')[-1].select('p')[-1].get_text()
            item['size'] = soup.select_one('ul[class="cont-lable"]').select('li')[-2].select_one('span').get_text().strip()

            financing_url = soup.select_one('ul[class="sub-nav"]').select('li')[1].select_one('a').attrs['href']
            if financing_url:
                yield scrapy.Request("http://radar.itjuzi.com"+financing_url,callback=self.parse_financing,meta={"item":item})


    def parse_financing(self,response):
        item = response.meta['item']
        if response.status == 200:
            soup = BeautifulSoup(response.body, 'lxml')
            li_list = soup.select_one('ul[class="financing-list"]').select("li")
            if li_list:
                item_list = []
                for li in li_list:
                    fn = {}
                    fn['info_time'] = li.select_one('span').get_text()
                    fn['info_round'] = li.select_one('p[class="financing-info"]').select_one(
                        'span[class="info-round"]').get_text().strip()
                    fn['info_invest'] = li.select_one('p[class="financing-info"]').select_one(
                        'span[class="info-invest"]').get_text().strip()
                    item_list.append(fn)
                item['financing'] = item_list
            else:
                item['financing'] = None

            team_url = soup.select_one('ul[class="sub-nav"]').select('li')[3].select_one('a').attrs['href']
            if team_url:
                yield scrapy.Request("http://radar.itjuzi.com"+team_url,callback=self.parse_team,meta={'item':item})

    def parse_team(self,response):
        item = response.meta['item']
        if response.status == 200:
            soup = BeautifulSoup(response.body,'lxml')
            li_list = soup.select_one('ul[class="team-list"]').select('li')
            if li_list:
                item_list = []
                for li in li_list:
                    team = {}
                    team['name'] = li.select_one('p[class="team-name"]').contents[0].strip()
                    team['title'] = li.select_one('p[class="team-name"]').contents[1].get_text()
                    team['info'] = li.select_one('p[class="team-note"]').contents[0].strip()
                    item_list.append(team)

                item['team'] = item_list
                print(item)
                yield item
            else:
                item['team'] = None



