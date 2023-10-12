import json
import random
import datetime

from bs4 import BeautifulSoup

import sys
sys.path.append("../")
from log.log import CustomLogger

custom_logger = CustomLogger(log_file_name="summary.log")
logger = custom_logger.get_logger()


class AnswerInfo:
    def __init__(
        self,
        author_name,
        author_url_token,
        author_type,
        author_follower_count,
        author_headline,
        answer_can_comment_reason,
        answer_can_comment_status,
        answer_comment_count,
        answer_comment_permission,
        answer_content,
        answer_voteup_count,
        answer_updated_time,
        answer_created_time
    ):

        self.author_name = author_name
        self.author_url_token = author_url_token
        self.author_type = author_type
        self.author_follower_count = author_follower_count
        self.author_headline = author_headline
        self.answer_can_comment_reason = answer_can_comment_reason
        self.answer_can_comment_status = answer_can_comment_status
        self.answer_comment_count = answer_comment_count
        self.answer_comment_permission = answer_comment_permission
        self.answer_content = answer_content
        self.answer_voteup_count = answer_voteup_count
        self.answer_updated_time=answer_updated_time
        self.answer_created_time=answer_created_time

    def read_files():
        answer_infos = []
        data = ""
        with open('../spider/spider/test.json', 'r') as file:
            data = json.load(file)
        for item in data:
            if 'data' in item:
                data_content = item['data']
                for answer in data_content:
                    if 'target' in answer:
                        author_name = answer['target']['author']['name']
                        author_url_token = answer['target']['author']['url_token']
                        author_type = answer['target']['author']['type']
                        author_follower_count = answer['target']['author']['follower_count']
                        author_headline = answer['target']['author']['headline']
                        answer_can_comment_reason = answer['target']['can_comment']['reason']
                        answer_can_comment_status = answer['target']['can_comment']['status']
                        answer_comment_count = answer['target']['comment_count']
                        answer_comment_permission = answer['target']['comment_permission']
                        soup = BeautifulSoup(
                            answer['target']['content'], 'html.parser')
                        answer_content = soup.get_text().replace("\n","")
                        answer_voteup_count = answer['target']['voteup_count']
                        timestamp=answer['target']['updated_time']
                        answer_updated_time= datetime.datetime.utcfromtimestamp(timestamp)
                        timestamp=answer['target']['created_time']
                        answer_created_time=datetime.datetime.utcfromtimestamp(timestamp)
                        # logger.info(author_name)
                        # logger.info(author_url_token)
                        # logger.info(author_type)
                        # logger.info(author_follower_count)
                        # logger.info(author_headline)
                        # logger.info(answer_can_comment_reason)
                        # logger.info(answer_can_comment_status)
                        # logger.info(answer_comment_count)
                        # logger.info(answer_comment_permission)
                        # logger.info(answer_content)
                        # logger.info(answer_voteup_count)
                        # logger.info(answer_updated_time)
                        # logger.info(answer_created_time)
                        answer_info = AnswerInfo(
                            author_name=author_name,
                            author_url_token=author_url_token,
                            author_type=author_type,
                            author_follower_count=author_follower_count,
                            author_headline=author_headline,
                            answer_can_comment_reason=answer_can_comment_reason,
                            answer_can_comment_status=answer_can_comment_status,
                            answer_comment_count=answer_comment_count,
                            answer_comment_permission=answer_comment_permission,
                            answer_content=answer_content,
                            answer_voteup_count=answer_voteup_count,
                            answer_updated_time=answer_updated_time,
                            answer_created_time=answer_created_time,
                        )
                        answer_infos.append(answer_info)
        sorted_answer_infos = sorted(
            answer_infos, key=lambda x: x.answer_voteup_count, reverse=True)
        return sorted_answer_infos


class QuestionInfo:
    def __init__(
            self,
            answer_cnt,
            sum_comment_cnt,
            max_comment,
            max_comment_answer,
            sum_vote_count,
            max_vote_count,
            max_vote_count_answer):
        self.answer_cnt = answer_cnt
        self.sum_comment_cnt = sum_comment_cnt
        self.max_comment = max_comment
        self.max_comment_answer = max_comment_answer
        self.sum_vote_count = sum_vote_count
        self.max_vote_count = max_vote_count
        self.max_vote_count_answer = max_vote_count_answer

    def sum_count(answer_infos):

        answert_cnt = len(answer_infos)
        sum_comment_cnt = 0
        sum_vote_count = 0
        max_comment = 0
        max_comment_answer = ""
        max_vote_count = 0
        max_vote_count_answer = ""
        logger.info(answert_cnt)

        for answer in answer_infos:
            sum_comment_cnt += answer.answer_comment_count
            sum_vote_count += answer.answer_voteup_count
            if (answer.answer_comment_count > max_comment):
                max_comment = answer.answer_comment_count
                max_comment_answer = answer.author_name
            if (answer.answer_voteup_count > max_vote_count):
                max_vote_count = answer.answer_voteup_count
                max_vote_count_answer = answer.author_name

        questioninfo = QuestionInfo(answer_cnt=answert_cnt, sum_comment_cnt=sum_comment_cnt, max_comment=max_comment,
                                    max_comment_answer=max_comment_answer, sum_vote_count=sum_vote_count,
                                    max_vote_count=max_vote_count, max_vote_count_answer=max_vote_count_answer)
        return questioninfo
        

    def stratify_answers_by_votes(answer_infos):
        # get votes and sort by 4% 1/1,26% 1/5,70% 1/7
        if (len(answer_infos)<50):
            return answer_infos
        answer_cnt = len(answer_infos)
        high_answer_cnt = int(answer_cnt*0.04)
        middle_answer_cnt = int(answer_cnt*0.26)-high_answer_cnt
        middle_answer_samplecnt = int(middle_answer_cnt/5)
        low_answer_cnt = answer_cnt-high_answer_cnt-middle_answer_cnt
        low_answer_smaplecnt = int(low_answer_cnt/7)

        answer_id = []
        index = 0
        while (index <= high_answer_cnt):
            answer_id.append(index)
            index += 1
        middle_index = 0
        while (middle_index <= middle_answer_samplecnt):
            random_integer = random.randint(high_answer_cnt, middle_answer_cnt)
            answer_id.append(random_integer)
            middle_index += 1

        low_index = 0
        while (low_index <= low_answer_smaplecnt):
            random_integer = random.randint(middle_answer_cnt, low_answer_cnt)
            answer_id.append(random_integer)
            low_index += 1
        sorted_answer_id = sorted(answer_id)
        sorted_answer_id=list(set(sorted_answer_id))
        result_answer_infos = [answer_infos[i] for i in sorted_answer_id]
        logger.info(len(result_answer_infos))
        return result_answer_infos


if __name__ == "__main__":
    pass
