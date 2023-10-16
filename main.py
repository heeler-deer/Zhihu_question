import json
import random
import torch
import numpy as np
import pandas as pd



import os
import sys
sys.path.append("./")
from log.log import CustomLogger
import requests
from spider.spider.zhihu import ZhihuSpider
custom_logger = CustomLogger(log_file_name="main.log")
logger = custom_logger.get_logger()








def crawl():
    logger.info("请输入question id")
    question_id=""
    while True:
        question_id=input("请输入知乎问题的id: ")
        tmp_question_url="https://www.zhihu.com/api/v4/questions/"+question_id+"/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=10&order=default&platform=desktop"
        logger.info(f"尝试向问题{question_id}发送请求")
        response = requests.get(tmp_question_url)
        if response.status_code == 200:
            logger.info("问题存在，开始爬取")
            break
        else:
            logger.info("问题不存在，请重新输入")


    file_path = "./spider/spider/question.json"  # 将文件路径替换为你要删除的文件路径

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"文件 {file_path} 已被删除。")
    else:
        logger.info(f"文件 {file_path} 不存在，无法删除。")
    spider = ZhihuSpider(question_id=question_id)
    spider.start_requests()
    spider.closed()
    logger.info("爬取完毕")
    
    
if __name__ == "__main__":
    crawl()
    










