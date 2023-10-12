import scrapy
import json
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import sys
sys.path.append("../../")
from log.log import CustomLogger
custom_logger = CustomLogger(log_file_name="zhihu.log")
logger = custom_logger.get_logger()


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    # allowed_domains = ["www.zhihu.com"]

    def __init__(self, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = '/usr/bin/google-chrome-stable'  # 指定Chromium浏览器的路径
        chromedriver_path = '/usr/bin/chromedriver'

        s = Service(executable_path=chromedriver_path,
                    chrome_options=chrome_options)

        
        self.driver = webdriver.Chrome(service=s)
        self.start_urls = ["https://www.zhihu.com/api/v4/questions/625267359/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=10&order=default&platform=desktop"]

    def start_requests(self):

        for url in self.start_urls:
            self.driver.get(url)
            time.sleep(3)
            json_data = self.driver.page_source
            self.parse(json_data)

    def parse(self, json_data):

        soup = BeautifulSoup(json_data, 'html.parser')
        content = soup.find('pre').text
        data = content
        data = json.loads(data)
        is_end = str(data['paging']['is_end'])
        next_url = str(data['paging']['next'])
        logger.info(is_end)
        logger.info(next_url)
        logger.info((len(next_url) != 0 and (
            is_end == "false" or is_end == "False")))
        flag = (len(next_url) != 0 and (
            is_end == "false" or is_end == "False"))
        filename = "test.json"
        with open(filename, 'a', encoding='utf-8') as file:
            if file.tell() == 0:
                file.write('[')
            else:
                file.write(',')
            json.dump(data, file, ensure_ascii=False, indent=4)
        if flag:
            self.driver.get(next_url)
            time.sleep(3)
            json_data = self.driver.page_source
            self.parse(json_data=json_data)

    def closed(self):
        filename = "test.json"
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(']')
        self.driver.quit()


if __name__ == "__main__":
    spider = ZhihuSpider()
    spider.start_requests()
    spider.closed()
