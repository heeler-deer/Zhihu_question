import json
import random
import torch
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from transformers import BartForConditionalGeneration, AutoTokenizer, Text2TextGenerationPipeline
from transformers import PegasusForConditionalGeneration
from tokenizers_pegasus import PegasusTokenizer
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import jieba
from transformers import AutoTokenizer, AutoModel


import sys
sys.path.append("../")
from log.log import CustomLogger
from parse.summary import AnswerInfo,QuestionInfo

custom_logger = CustomLogger(log_file_name="extract.log")
logger = custom_logger.get_logger()




def cluster():
    documents=[]
    with open('./summary.txt', 'r') as file:
    # 逐行读取文件内容并将每一行作为一个字符串写入列表
        documents = file.readlines()
    # sorted_answer_infos=AnswerInfo.read_files()
    # result_answer_infos=QuestionInfo.stratify_answers_by_votes(sorted_answer_infos)
    
    # for answer_info in result_answer_infos:
    #     content=answer_info.answer_content
    #     documents.append(content)
    logger.info(len(documents))
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)


    linkage_matrix = linkage(tfidf_matrix.toarray(), method='ward', metric='euclidean')

    silhouette_scores = []

    for num_clusters in range(2, min(5, len(documents) + 1)):
        clusterer = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
        clusters = clusterer.fit_predict(tfidf_matrix.toarray())
        silhouette_avg = silhouette_score(tfidf_matrix.toarray(), clusters)
        silhouette_scores.append(silhouette_avg)

    # plt.plot(range(2, min(10, len(documents) + 1)), silhouette_scores)
    # plt.xlabel('Number of Clusters')
    # plt.ylabel('Silhouette Score')
    # plt.show()

    optimal_num_clusters = silhouette_scores.index(max(silhouette_scores)) + 2 


    clusterer = AgglomerativeClustering(n_clusters=optimal_num_clusters, linkage='ward')
    clusters = clusterer.fit_predict(tfidf_matrix.toarray())


    clustered_data = pd.DataFrame({'Text': documents, 'Cluster': clusters})


    for cluster_id in range(optimal_num_clusters):
        print(f"Cluster {cluster_id + 1}:")
        cluster_members = clustered_data[clustered_data['Cluster'] == cluster_id]
        for text in cluster_members['Text']:
            print(text+"\n")
        print()

    print(f"Optimal number of clusters: {optimal_num_clusters}")








def summary():
    logger.info("*****************Begin summary*****************")
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    logger.info(device)
    
    sorted_answer_infos=AnswerInfo.read_files()
    result_answer_infos=QuestionInfo.stratify_answers_by_votes(sorted_answer_infos)
    summary_result_answer_infos=[]
    sum_texts=[]
    model = PegasusForConditionalGeneration.from_pretrained("IDEA-CCNL/Randeng-Pegasus-523M-Summary-Chinese").to(device)
    tokenizer = PegasusTokenizer.from_pretrained("IDEA-CCNL/Randeng-Pegasus-523M-Summary-Chinese")
    for answer_info in result_answer_infos:
        content=answer_info.answer_content
        print(content)
        
        
        

    
    
    
        inputs = tokenizer(content, max_length=1024, return_tensors="pt").to(device)
        summary_ids = model.generate(inputs["input_ids"])
        sum_text = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        print(sum_text)
        
        
        summary_result_answer_info=answer_info
        summary_result_answer_info.sumtext=sum_text
        summary_result_answer_infos.append(summary_result_answer_info)
        sum_texts.append(str(sum_text))
    with open("summary.txt", "w") as file:
        for item in sum_texts:
            file.write(str(item) + "\n")
    return summary_result_answer_infos






def cluster_bert(num_clusters,summary_result_answer_infos):
    logger.info("*****************Begin cluster*****************")
    model_name = "bert-base-chinese"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    text_data = []



    # with open('./summary.txt', 'r') as file:
    #     text_data = file.readlines()


    def get_text_embeddings(text_data):
        embeddings = []
        model.to(device)
        for text in text_data:
            tokens = tokenizer(text, padding=True,
                            truncation=True, return_tensors="pt")
            tokens.to(device)
            with torch.no_grad():
                outputs = model(**tokens)
            pooled_output = outputs.last_hidden_state.mean(
                dim=1).squeeze().cpu().numpy()
            embeddings.append(pooled_output)
        return np.array(embeddings)

    for summary_result_answer_info in summary_result_answer_infos:
        text_data.append(summary_result_answer_info.sumtext)
    text_embeddings = get_text_embeddings(text_data)

    num_clusters = num_clusters 
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(text_embeddings)
    cluster_labels = kmeans.labels_
    clusters = {}
    for i, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(text_data[i])
    label_summary_result_answer_infos=[]
    for cluster_label, cluster_texts in clusters.items():
        print(f"Cluster {cluster_label}:")
        for text in cluster_texts:
            print(text)
            for summary_result_answer_info in summary_result_answer_infos:
                if summary_result_answer_info.sumtext==text:
                    label_summary_result_answer_info=summary_result_answer_info
                    label_summary_result_answer_info.label=cluster_label
                    label_summary_result_answer_infos.append(label_summary_result_answer_info)
    return label_summary_result_answer_infos







if __name__ == "__main__":
    summary_result_answer_infos=summary()
    label_summary_result_answer_infos=cluster_bert(4,summary_result_answer_infos)
    data = []
    for info in label_summary_result_answer_infos:
        data.append(
            [
                info.author_name,
                info.author_url_token,
                info.author_type,
                info.author_follower_count,
                info.author_headline,
                info.answer_can_comment_reason,
                info.answer_can_comment_status,
                info.answer_comment_count,
                info.answer_comment_permission,
                info.answer_content,
                info.answer_voteup_count,
                info.answer_updated_time,
                info.answer_created_time,
                info.label,
                info.sumtext,
            ]
        )

    df = pd.DataFrame(
        data,
        columns=[
            "Author",
            "Author_url",
            "Author_tpye",
            "Author_follower_count",
            "Author_headline",
            "Answer_can_comment_reason",
            "Asnwer_can_comment_status",
            "Asnwer_comment_count",
            "Answer_comment_permission",
            "Answer_content",
            "Answer_voteup_count",
            "Answer_updated_time",
            "Answer_created_time",
            "label",
            "sumtext"
        ],
    )

    csv_filename = "Answer_info.csv"
    file_exists = pd.io.common.file_exists(csv_filename)
    df.to_csv(csv_filename, mode='w', header=not file_exists, index=False)
