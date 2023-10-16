# Zhihu_question
爬取知乎某个问题下的所有回答

## 参考


本项目参考并使用了如下项目：

https://github.com/IDEA-CCNL/Fengshenbang-LM



@misc{Fengshenbang-LM,
  title={Fengshenbang-LM},
  author={IDEA-CCNL},
  year={2021},
  howpublished={\url{https://github.com/IDEA-CCNL/Fengshenbang-LM}},
}






## 依赖


### chrome driver


https://chromedriver.chromium.org/downloads


根据chrome浏览器版本下载相对应的chrome driver,在./spider/spider/zhihu.py中的类ZhihuSpider的__init__函数中配置：

+ chrome_options.binary_location  chrome浏览器路径
+ chromedriver_path  chrome driver路径





**TODO:**

根据回答的内容进行可视化