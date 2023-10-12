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
    # documents = [
    #     "由于公司领导的要求，所有的软件开发都要将DDD作为指导思想，并且要接受敏捷的思想；迫不得已下拜读了《实现领域驱动设计》这本书，将会在公司的内部系统上全面实践DDD。DDD把领域模型的重要性提高到了数据模型之上，在传统的MVC分层架构下。我们将项目结构分为Controller，Service，DAO 这三个主要的层，所有的业务逻辑都在Service中体现，而我们的实体类Entity却只是充当一个与数据库做ORM映射的数据容器而已，它并没有反映出模型的业务价值。所以又把这种模型称为“贫血模型”。“贫血模型”有什么坏处呢？在我们的代码 中将会到处看到各种的setter方法和各种各样的参数校验的代码，尤其是在Service层，但是这些代码它并没有反映出它的业务价值。这就是事务脚本的架构下，所呈现出来的弊端，这种模式下认为数据模型优先，所以会导致开发人员和产品经理在讨论问题的时候，完全是从两个角度在思考问题。开发人员听到需求后，脑袋里想的并不是如何反应出业务的价值，而是考虑的是数据库表怎么设计，字段该怎么加这些问题。所以DDD中提出了通用语言这么一个概念，并且基本将通用语言的概念贯穿于整个落地的过程。这样会大大的减少成员之间的沟通成本（前提是大家都从心里接受了DDD）。为什么DDD难以落地呢？第一，国内关于DDD的最佳实践还是太少了，除了知名的几个大厂以外很少看到有关于DDD的落地实践。这里附上美团的DDD实践，美团领域驱动设计；最佳实践太少意味着，我们可以参考的资料就少，承担的项目失败的风险就大。第二，DDD中出现了很多的概念和术语，比如 聚合根，值对象，六边形架构，CQRS(命令和查询职责分离)，事件驱动等等概念。很多人看到了这么多概念的时候，心中就开始打退堂鼓了。第三，DDD需要我们在领域建模花费很多的时间和精力，而且还可能导致付出和收益不成正比的情况。因为在界限上下文的划分上是非常考验架构师的业务水平。如果没有将业务模型很好的识别出来，那么可能很快模型就会在迭代的过程中腐败掉了。上面就只是我自己对DDD的一些简单的理解，知识问题有不正确的地方，可以指正交流。（勿喷）" ,
    #     "最近两年有些新的落地体验，回过头来发现，当初对这些概念的理解还是没有深入，重新阐述下。之前理解不到位的点有DDD应用只能是代码落地吗？当前团队、项目不适合落地DDD我们还能做些什么战术设计的各个模块是如何协作的哪些是问题空间问题，哪些是方案空间问题边界没有划分清楚。实体和聚合根的区别理解不不深刻，实体和聚合根建模的方法不对。以上问题将会在下文解释清楚。战术设计拆解DDD的战术设计即设计某个子域的领域模型以及代码落地。领域事件、领域对象、聚合根、实体、值对象、领域服务、工厂、资源库等这些概念都属于这个范畴。笔者将这些概念重新分层组装了下，如下图所示。 首先将整体分成两部分，问题空间和方案空间。问题空间即领域建模。是对业务问题的描述，以及我们如何对这些问题进行抽象。这些是需要在业务、产品、开发都必须达成一致的，与具体的技术方案无关。方案空间即如何用技术手段来解决问题，与具体技术的实现有关。问题空间即领域建模，是通过实体、值对象、领域服务、领域事件来表达。实体和值对象是模型对象，实体是重中之重，包括核心模型数据、行为、状态。之所以要区分实体和值对象，是为了降低复杂度，因为值对象是个常数对象，不需要花太多精力。 注意某个对象在某个领域内是个值对象，在另外的领域可能是个实体，所以脱离领域上下文，说某个对象是值对象，肯定是不对的，比如大家常说的地址是个值对象，这一定是对的吗？  领域事件即实体产生的事件  领域服务包括一些逻辑的计算，和业务策略。比如商业决策逻辑、业务流程等。  方案空间即如何解决问题，实现领域模型与代码的映射。实现设计与实现的一致性。主要通过工厂，聚合，资源库来表达。聚合是对实体、值对象的封装。领域外部对领域对象所有访问都基于聚合来。如基础设施层操作聚合进行数据保存。其他领域引用聚合对象数据。 聚合的设计一般是围绕着技术来的，比如聚合对象事务性。  工厂，复杂对象的创建工厂类  资源库，对聚合的操作。  从笔者的实践角度来说，落地DDD过程中，问题空间比方案空间更重要，收益更大。因为通常我们吐槽的某些代码写的烂，贫血模型。背后并不是因为没有用DDD,而是问题空间没有定义好，对于业务没有深刻理解，导致模型抽象不足。所以从这个角度说，DDD其实是一套建模方法，帮助团队成员快速达成模型认知一致。详细例子可以看:可落地的DDD------------------------2022年更新-------------------------DDD落地为什么这么难敏捷迭代，放弃建模现代互联网产研团队的构成一般是市场/运营、产品、UI交互、前端、后端、测试。这些角色的分工是将一个产品开发上线的各个过程拆分出来，然后每个过程专人负责，可以有效提高生产效率，这一套流程是标准的流水线作业。这样做的好处毋庸置疑，坏处也很明显，每个人只盯着自己那一块，而忽略整体了。再来看DDD,领域建模设计核心有两个统一语言(软件的开发人员/使用人员都使用同一套语言，即对某个概念，名词的认知是统一的）面向领域（以领域去思考问题，而不是模块）为了实现这两个核心，需要一个关键的角色，领域专家。他负责问题域，和问题解决域，他应该通晓研发的这个产品需要解决哪些问题，专业术语，关联关系。这个角色一般团队是没有配备的。最接近这个角色的就是产品了，但实际上产品并不是干这个活的。在我们团队落地过程中，有一段时间苦于没有领域专家，我想push产品成为领域专家，担当起这个角色。 最后不了了之，产品很配合，但是内驱力不强。为什么内驱力不强，因为给他带来的收益不够。前面已经提到敏捷迭代后，每个角色都是流水线上的螺丝钉，大家都只盯着自己这一块。对自己有利的去参与，和自己无关的不管。我们先看统一语言与面向领域的好处因为大家都使用统一的一套通用语言，所以沟通成本会大大减小，不会在讨论A的时候以为是B。对使用产品的用户有好处，他能在产品不断更新过程中，有一套统一流畅的体验。用户不用在每次软件更新时都要抱怨为什么之前的一个数据保存后没有用到了。面向领域去开发产品有助于我们深入分析产品的内在逻辑，专注于解决当前产品的核心问题，而不是冗余的做很多功能模块，或者几个用户/运营反馈的问题就去更改产品逻辑，完了上线后用户不用，你还在那边骂用户朝三暮四，乱提需求。这些好处粗看一下，其实对产品研发的各个角色都有意义。但细看一下呢，沟通成本大大减小，对于运营，产品，UI交互没啥问题。一个问题理解的不一致，组织个会议，大家好好聊聊就行了。用户体验一致对产研团队有啥好处呢，反正用户骂的不是我，是客户和运营。深入分析产品的内在逻辑有啥用呢？一款产品的成功有很多因素，主要靠上面，我只是一个小兵，我管不了那么多。有空我多研究研究我的专业领域，多去看几篇面试文章。产品黄了，我好跳槽。因为本人是后端研发，所以这里不对其他角色过多展开。只想对研发说，你跳槽换个公司就好了吗？还是crud boy。还是重复着写着很多冗余的功能，冗余的代码。需求方让你写什么，你就写什么，最后在一天天的加班中丧失了对代码的兴趣，没有了梦想。 我们都知道改变别人很难，所以先从改变自己开始，先让自己变优秀了，才能影响他人框架易学，思想难学如果抛开其他角色，单从研发角度考虑DDD呢。开发进行领域建模，然后遵从康威定律，将软件架构设计映射到业务模型中。（虽然这个领域，开发可能识别的不对，暂且忽略这个问题）康威（梅尔·康威）定律 任何组织在设计一套系统（广义概念上的系统）时，所交付的设计方案在结构上 都与该组织的沟通结构保持一致。纯研发实施DDD,为什么也这么难呢？没有标准DDD是一套思想，一套领域建模设计，一套在特定上下文环境中使用的。所以在1千个团队中实行DDD,可能有1千套不同的方案。一个实行DDD多年的人，换了一个公司，换了一个团队，把他原有的那套带过去，推行下去，一般都不适用。所以DDD的学习和实践不像学习一个函数，API，框架那样有直接的反馈效果，他需要结合团队的实际情况去实行，才能达到效果。期待DDD解决所有的问题程序员都是很实际的，没有好处的东西是不会去做的。你必须能够有效的帮助他提升，他才会去接受。 比如当初有团队成员提出来，我们实行了这一套后，是不是不用加班了，或者加班时间可以减小。有测试提出实行这一套后，bug率能降低多少。研发需要一个可以量化的效果，抱歉DDD做不到。没有哪个团队实行了DDD后，解决了软件开发的所有问题。关于这一点，可以读一下驱动方法不能改变任何事情",
    #     "靠谱码？ 一群没写过DDD的人，聊理论吹的叮当的，写代码搞的稀得囊的，这就不靠谱！对于研发来说，DDD 你还是给我落地看看代码，我才能知道好不好，别一上来就战术、战略、领域砖家，名词造的不错，代码呢、代码呢，合着你就贡献了一张嘴？1. DDD 架构落地我不想这样，我要把DDD落地，把设计模式结合进来，让我看看它到底优秀在哪！写完了，只能说，真香！整整半年，小傅哥都在做这件事情，直到22年初才完成整个DDD系统的第一期设计实现和落地。在这个《分布式抽奖系统》项目中，以DDD架构和设计模式落地实战的方式，进行代码开发、视频介绍、文档说明的方式讲解和实现分布式抽奖系统，那么这里会涉及到很多DDD的设计思路和设计模式应用，以及互联网大厂开发中所应用到的技术，包括：SpringBoot、Mybatis、Dubbo、MQ、Redis、Mysql、ELK、分库分表、Otter 等。Lottery 抽奖系统 项目是一款互联网面向C端人群营销活动类的抽奖系统，可以提供抽奖活动玩法策略的创建、参与、记账、发奖等逻辑功能。在使用的过程中运营人员通过创建概率类奖品的抽奖玩法，对用户进行拉新、促活、留存，通常这样的系统会用在电商、外卖、出行、公众号运营等各类场景中。此系统架构为 DDD 领域驱动设计的四层架构实现方式，以重视代码实现落地的方式向读者介绍和展示如何开发这样的代码。在 Domain 领域层逐步通过拆解系统流程设计，按照职责边界的领域模块进行设计和开发，最终在应用层进行逻辑功能编排。这个系统中会体现出很多的设计模式思想和最终的实现，只有把 DDD 和设计模式结合起来，才能开发出更加易于扩展和维护的代码结构。2. 分布式工程设计整体系统架构设计包含了6个工程：Lottery：分布式部署的抽奖服务系统，提供抽奖业务领域功能，以分布式部署的方式提供 RPC 服务。Lottery-API：网关API服务，提供；H5 页面抽奖、公众号开发回复消息抽奖。Lottery-Front：C端用户系统，vue H5 lucky-canvas 大转盘抽奖界面，讲解 vue 工程创建、引入模块、开发接口、跨域访问和功能实现Lottery-ERP：B端运营系统，满足运营人员对于活动的查询、配置、修改、审核等操作。DB-Router：分库分表路由组件，开发一个基于 HashMap 核心设计原理，使用哈希散列+扰动函数的方式，把数据散列到多个库表中的组件，并验证使用。Lottery-Test：测试验证系统，用于测试验证RPC服务、系统功能调用的测试系统。3. 凝练流程领域拆解功能流程，提炼领域服务，一步步教会你把一个业务功能流程如何拆解为各个职责边界下的领域模块，在通过把开发好的领域服务在应用层进行串联，提供整个服务链路。通过这样的设计和落地思想，以及在把流程化的功能按照面向对象的思路使用设计模式进行设计，让每一步代码都变得清晰易懂，这样实现出来的代码也就更加易于维护和扩展了。所以，你在这个过程中学会的不只是代码开发，还有更多的落地思想实践在这里面体现出来。也能为你以后开发这样的一个项目或者在面试过程中，一些实际复杂场景问题的设计思路，打下不错的基础。如果你也感兴趣DDD落地，可以加入一起学习：Lottery 抽奖系统 - 基于领域驱动设计的四层架构实践",
    #     "DDD就不是给研发用的。DDD最为一套方法论，其面对的目标至少也是高级/资深架构师，高级/资深产品经理，再加上项目负责人/项目经理的。换个说法，针对的至少是P8+甚至P9+的，总监这一层的老家伙们做顶层设计用的，如果是放在那种靠着一、两个项目吃饭的小公司里，就是CTO和VP们才需要考虑的东西。下面的人别说一线开发了，就连负责带队的Team leader们在领域划分和界限上下文这些点上都没有什么发言权，安心负责好自己的模块/接口/服务就好，别想那么多。",
    #     "DDD就是玄学在没有领域专家的情况下，每个人设计的领域对象肯定大有不同，一个团队里十个开发，能设计出十种不通的领域划分，最后迭代几个版本，代码根本没法维护互联网开发新技术新理念层出不穷，每段时间都会出来一个奇葩东西，最后被淘汰现在DDD就是，随便在知乎上抓个人就能给你长篇大论一套DDD原理，让他写个Demo放Github上，都够呛能写出来我们团队在设计一个非常复杂系统的时候用过DDD，而且一直在用，坑很多，最后还是得看本质1.这个技术用了能提高员工多少效率2.这个技术带来了什么好处3.这个技术维护成本和设备成本是不是增加了用了DDD我花了多久时间构思领域模型，花了多久时间和小伙伴讨论领域模型，花了多少时间打代码，花了多少时间改bug，如果用了DDD，你办公效率反倒下降了，团队间讨论更频繁了，那我强烈建议放弃这个技术，没必要为了追赶潮流而学习技术，计算机技术永远是避繁就简，互联网永远是敏捷开发。DDD这个概念国内已经炒了几年了，好不好用试试就知道了。   我发现很多人还是没明白我的意思一个技术好，必然是有相应指标衡量的，因为这个技术可以带来某些好处，我们才会去用它。如果没有带来任何好处，只是为了用而用，或者跟风用，完全就是本末倒置。换位思考一下，如果你是老板，手下CTO带几百人团队花了两个月重构代码改成DDD，代码效率没增加，并发效率没增加，维护性还多了门槛，根本说不过去。",
    #     "没有什么理论是不靠谱的，不靠谱的是应用理论的人。。。",
    #     "DDD不需要DDD这个单词，DDD更多的时候是管理者的个人需求！",
    #     "代码之道，存乎一心。啥都要看，啥都要学。不同场景有不同的最佳实践，不要迷信权威。",
    #     "个人认为领域驱动的重点应该是领域两个字，每个模块应该有自己的功能和界限，看到很多人写代码的时候最基本的功能界限都没分清楚，在A的模块中放置了B的方法，导致了A提供的功能不单纯是A的功能，这样根本无从谈起领域驱动。另外领域驱动是思想，大家实现的方法和目标不一定一致，清晰概念应该是在需求、产品、研发不同岗位之间要确立的，否则很容易出现歧义。",
    #     "领域驱动设计DDD越来越受到重视，国内有很多团队在使用领域驱动设计DDD，但是每一个团队对DDD的理解可能不一样。如果领域的设计不能很好地指导开发工作，那么DDD的威力就发挥不出来了。我们接触到的“领域驱动”，很有可能是假的“领域驱动”，是别人理解消化后的领域驱动，即使是架构师或者项目经理，他们不一定真正理解领域驱动，人们对领域驱动有很多误解，比如“领域驱动只适合大型项目”，“领域驱动会加大工作量，多加了一层Domain，太多转换”，“领域驱动应该采用贫血模型”等等，这些都是错误的认知。Java项目的架构通常是采用MVC三层架构，MVC全名是Model View Controller，是模型Model－视图View－控制器Controller的缩写，但是MVC跟领域驱动的分层架构是不同。领域驱动的分层架构：用户界面层/表示层Facade用户界面层负责向用户显示信息和解释用户指令。这里指的用户可以是另一个计算机系统，不一定是使用用户界面的人。该层包含与其他应用系统（如Web服务、RMI接口、Web应用程序以及批处理前端）交互的接口与通信设施。它负责Request的解释、验证以及转换。另外，它也负责Response的序列化，如通过HTTP协议向web浏览器或web服务客户端传输HTML或XML，或远程Java客户端的DTO类和远程外观接口的序列化。该层的主要职责是与外部用户（包括Web服务、其他系统）交互，如接受用户的访问，展示必要的数据信息。用户界面层facade目录：（1）api存放Controller类，接受用户或者外部系统的访问，展示必要的数据信息。（2）handle存放GlobalExceptionHandler全局异常处理类或者全局拦截器。（3）model存放DTO（Request、Reponse）、Factory（Assembler）类，Factory负责数据传输对象DTO与领域对象Domain相互转换。应用层Application应用层定义了软件要完成的任务，并且指挥表达领域概念的对象来解决问题。该层所负责的工作对业务来说意义重大，也是与其他系统的应用层进行交互的必要通道。应用层要尽量简单。它不包含任务业务规则或知识，只是为了下一层的领域对象协助任务、分配工作。它没有反映业务情况的状态，但它可以具有反映用户或程序的某个任务的进展状态。应用层主要负责组织整个应用的流程，是面向用例设计的。该层非常适合处理事务，日志和安全等。相对于领域层，应用层应该是很薄的一层。它只是协调领域层对象执行实际的工作。应用层中主要组件是Service，因为主要职责是协调各组件工作，所以通常会与多个组件交互，如其他Service，Domain、Factory等等。应用层application目录：（1）service存放Service类，调用Domain执行命令操作，负责Domain的任务编排和分配工作。（2）external存放ExternalService类，负责与其他系统的应用层进行交互，通常是我们主动访问第三方服务。（3）model存放DTO（ExtRequest、ExtReponse）类。应用层application可以合并到领域层biz目录。领域层/模型层Biz领域层主要负责表达业务概念，业务状态信息和业务规则。Domain层是整个系统的核心层，几乎全部的业务逻辑会在该层实现。领域模型层主要包含以下的内容：实体(Entities):具有唯一标识的对象值对象(Value Objects): 无需唯一标识。领域服务(Domain): 与业务逻辑相关的，具有属性和行为的对象。聚合/聚合根(Aggregates & Aggregate Roots): 聚合是指一组具有内聚关系的相关对象的集合。工厂(Factories): 创建复杂对象，隐藏创建细节。仓储(Repository): 提供查找和持久化对象的方法。领域层biz目录：（1）domain存放Domain类，Domain负责业务逻辑，调用Repository对象来执行数据库操作。Domain没有直接访问数据库的代码，具体的数据库操作是通过调用Repository对象完成的。注意，除了CQRS模式外，Repository都应该是由Domain调用的，而不是由Service调用。（2）repository存放Repository类，调用Dao或者Mapper对象类执行数据库操作。（3）factory存放Factory类，负责Domain和实体Entity的转换。基础设施层Infrastructure基础设施层为上面各层提供通用的技术能力：为应用层传递消息，为领域层提供持久化机制，为用户界面层绘制屏幕组件。基础设施层以不同的方式支持所有三个层，促进层之间的通信。基础设施包括独立于我们的应用程序存在的一切：外部库，数据库引擎，应用程序服务器，消息后端等。基础设施层Infrastructure目录：（1）commons存放通用工具类Utils、常量类Constant、枚举类Enum、BizErrCode错误码类等等。（2）persistence存放Dao或者Mapper类，负责把持久化数据映射成实体Entity对象。注意，领域对象是具有属性和行为的对象，是有状态的，数据和行为都是可以重用的。在很多Java项目中，Service类是无状态的，而且一般是单例，业务逻辑直接写到Service类里面，这种方式本质上是面向过程的编程方式，丢失了面向对象的所有好处，重用性极差。应用“贫血模型”会把属于对象的数据和行为分离，领域对象不再是一个整体，破坏了领域模型。只有对领域驱动有足够的认知，工程师才会正确运用领域的理念去编程，告诉工程师业务逻辑是写在Domain不管用，他们可能还是会在Service里面写业务逻辑代码，创建很多private私有方法。领域驱动开发的关注点在于领域模型，所有的考虑都应该从领域的角度出发，重心放在业务。领域模型必须能够精准地表达业务逻辑，领域模型需要在开发过程中不断被完善，并且能够指导工程师的开发工作。",
    #     "历史和现状价值和前提可能的落地路径前景思考",
    #     "有啊，其实你看到的互联网应用就是DDD，DDD需要一个领域专家，而互联网应用的领域专家是“用户”，只是这个专家的需求不稳定，需要一个代理人（产品经理）进行需求描述，然后建模，然后就是 MVC 的模式了，哈哈。",
    #     "没有什么理论是不靠谱的，不靠谱的是应用理论的人。。",
    #     "领域驱动设计并不是新的架构设计理论，从Eric Evans提出至今已经有十多年历史。由于微服务架构的兴起，DDD常用于指导微服务边界划分，并重新广泛进入软件研发大众的视野。DDD的理念及应用普及在国外相对成熟，在国内尚处于初期发展阶段。国内的很多社区以及企业组织内部近几年对于DDD的探讨和应用逐渐火热，许多架构师以及开发人员对DDD充满了学习和实践的热情。而像敏捷一样，不同团队对其认知水平和实践水平不尽相同，有的成功，大多数可能是失败的，这就是为什么国内感觉没什么人用，领域驱动设计为什么落地这么难？在最后也会解答这个问题。领域驱动设计（Domain Driven Design），简称DDD， Eric Evans 2004年的《Domain-Driven Design: Tackling Complexity in the Heart of Software》一书中第一次提出。领域驱动设计是一种用于指导软件设计的方法论，也是一种设计思维方式，用于解决软件复杂性问题，旨在加速那些必须处理复杂领域的软件项目的开发。实践DDD的第一步不在于如何编写代码，而首先需要拉齐对领域驱动设计的认知。后续的系列文章将围绕领域驱动设计进行不同视角探讨，以期帮助大家对其有更深入的认识，并能应用的实际的研发工作中。聊聊问题空间、解空间、领域模型问题空间和解决方案空间问题空间：Problem Space，是当前环境下业务所面临的一系列问题和问题背后的需求，通常是业务和产品领域专家主导问题、需求的收集描述和分析。问题空间框定了我们要解决的问题的上下文，这种上下文环境不是软件工程或是领域驱动所独有的，而是通用的共性的元素。工程实践必然处于某种上下文环境之下。解决方案空间：Solution Space，解决方案空间是针对问题空间的解决方案，属于工程实现阶段，由技术专家主导方案设计。软件开发过程，本质上可以看作是问题空间到解决方案空间的一个映射转化：问题空间，找出业务挑战及其对相关需求场景用例分析解空间，通过具体的技术工具手段来进行设计实现领域、模型和领域模型领域：Domain“领域”是“知识或活动的集合”，相对于软件系统而言，领域就是软件应用所要解决的现实问题区域。领域对应于问题空间，是一个特定范围边界内的业务需求的总和。领域模型：Domain Model抽象是一种化繁为简的能力，是人类认识世界的利器，也是一种生物本能。在有限的脑容量的前提下，人类不可能存储记忆所有的细节，海量信息已经超出人脑存储限制而无法容纳和有效获取。抽象使得人类可以屏蔽无关细节信息，抽取高层的有效信息进行记忆存储。试想，如果脑机接口技术有所突破，在人脑背后链接的是海量的高效的计算机集群，这种无限的存储、计算和检索能力的增强，“抽象能力也许会被弱化”。模型被用来表述人们所关注的现实或想法的某个方面，本质上是一种抽象过程的产物，把与解决方案密切相关的方面抽象出来，而忽略无关细节。聚焦在软件工程领域，要想构建满足需求的软件系统，开发团队需要软件面向的领域所涉及的知识可能非常庞大和复杂，而模型正是解决这种信息超载问题的有效工具。对领域进行模型设计的过程就是领域建模，领域建模的目的并非是要建立一个百分之百符合“现实”的模型，理论上，我们也无法实现这种对现实的完全建模，而只能是对现实某种程度的模拟。领域建模的输出即领域模型，领域模型是针对特定领域里的关键事物及其关系的可视化表现，属于解决方案空间范畴。为了准确定义需要解决问题而构造的抽象模型，为软件系统的构建目标统一认知，是业务功能场景在软件系统里的映射转化。领域模型并非领域专家头脑中的知识，而是对这些知识进行严格的组织和有选择的抽象。同时，领域模型并非某种特殊的图、文字或者代码，而是他们所传达的思想，图、文字或代码都可以作为模型的表示或传达形式，但他们不是模型，而是不同维度的模型视图。领域驱动设计领域驱动设计强调领域模型的重要性，并通过模型驱动设计来保障领域模型与程序设计的一致。领域驱动设计首先从业务需求中提炼出统一语言，并建立领域模型指导着程序设计以及编码实现；最后，又通过重构来发现隐式概念，并不断解决领域领域模型相关的新问题。本质上，领域驱动设计也是从问题空间映射到解决方案空间。领域驱动设计结合了宏观和微观两个层面的设计，分别对应于领域驱动概念中的战略设计和战术设计。领域驱动设计：战略设计战略设计的初衷是要保持模型的完整性，主要从下面两个方面来考量的：问题域方面：将问题规模进行拆解，划分为不同类型的子域，识别出核心领域与其他子领域。解决方案层面：划分限界上下文和上下文映射对问题域进行合理的分解，确定上下文边界以及它们之间的关系。领域驱动设计：战术设计战略设计的初衷是要保持模型的完整性，通过战略设计将整个软件系统分解为多个限界上下文，然后对每个界限上下文进行战术设计。对每个限界上下文进行战术设计。Eric Evans提供的模型驱动设计的构造要素以及要素间的关系如下图所示：实体：Entity，不同于通过属性进行定义的传统对象，实体对象通过唯一标识进行区分，且具有持续的生命周期。值对象：Value Object，值对象是具有属性且不可变的对象，但没有唯一标识。领域事件：Domain Event，领域事件用于记录系统内的模型活动相关的离散事件，虽然系统内所有事件都应该能够被跟踪，但只有被领域专家关心的事件类型才创建领域事件。聚合：Aggregate，聚合对象是实体和值对象的聚合，聚合具有一个唯一的根，即聚合根。外部对象不再直接访问聚合内部的单个对象或者实体，而是直接访问聚合根，并使用聚合根将指令传递给对应的分组。领域服务：Domain Service，某些领域逻辑不适合分配给某个特定的实体对象，可将其这些操作封装成领域服务资源库：Repositories，资源库不是配置库，它提供一个全局接口来访问特定聚合内部所有的实体类和值对象，应该包括创建，修改，删除聚合内部对象的方法。工厂：Factories，工厂封装了创建复杂对象和聚合的逻辑，对客户端屏蔽创建的复杂性上述DDD战术设计的模式标识了进行设计时的一些关键模式，但并非说是一定要严格使用和遵循的，也不是遵循了所有的战术设计模式就是符合领域驱动设计。因为，实践DDD关键不在于这种战术层面模式的落地，而是在于其宏观的领域驱动设计思想的遵循，比如统一语言、领域模型与代码间的一致、子域及上下文的拆分以及映射、领域模型与技术关注点的分离等等。另外，随着DDD的不断发展，一些新的构建模式已经涌现，老的构造模型不一定能符合团队研发的要求。领域驱动设计为什么落地这么难？需要鲁棒的领域知识，依靠项目中领域专家的支持如果团队中没有熟悉应用所需领域知识的领域专家，即使具备技术再强的开发人员也无济于事。在某些情形下，领域驱动设计需要一个或多个外部人员在整个软件开发生命周期中扮演领域专家的角色。有些情况下，领域驱动设计需要在整个软件开发生命周期中与外部团队成员(充当领域专家角色)进行协作。在创新型业务中应用DDD同样存在挑战，由于业务模式的不确定性，业务需求变化的频率和幅度很大，同样也缺乏新领域的领域专家，整个业务都处于一种探索模式，很难建立起相对稳定、高可复用的领域模型。强调不断迭代和持续集成，对缺乏迭代经验而偏重于瀑布模型的团队可能导致障碍领域驱动设计实践依赖不断迭代和持续集成来构建高可扩展的项目，但是这种基于迭代和持续集成的时间，在某些团队中落地可能会存在阻碍，特别是如果过去经验是建立在僵化的开发模型上，比如瀑布模型。不适合偏向技术型的应用领域驱动设计适合于具有非常高领域复杂性(业务逻辑复杂)的应用，但不适用于领域复杂性很低但技术复杂性很高的领域。DDD着重强调需要领域专家以便构造出项目依赖的统一语言和领域模型，但是如果项目的技术复杂性很高，领域能否理解是一种挑战。当全体团队成员没有完全理解技术需求或限制时可能会导致问题团队过于重视战术设计，导致实践准线和原则的偏离团队对领域驱动设计的认知不够，精力没有聚焦在问题域拆分、统一语言、模型与技术关注点分离等核心原则上，而是一开始便从实现的角度触发，过度强调战术设计模式的落地，从而陷入无尽的技术细节之中作者：倪新明",
    #     "当业务复杂度达到一定程度的时候，DDD的优势才能体现出来~",
    #     "可以看看这篇文章，绝对干货，把DDD讲的很清楚，用DDD的思维写出的技术方案，和平常应付写的天差地别。通过一个业务实例介绍了技术方案的七大维度：四色分领域、用例看功能、流程三剑客、领域与数据、纵横做设计、分层看架构、接口看对接。每个维度描述系统的一个侧面，组合在一起最终描绘出整个系统。长文多图：结合DDD讲清楚编写技术方案的七大维度",
        
    #     ]

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
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(device)
    
    sorted_answer_infos=AnswerInfo.read_files()
    result_answer_infos=QuestionInfo.stratify_answers_by_votes(sorted_answer_infos)
    documents=[]
    for answer_info in result_answer_infos:
        content=answer_info.answer_content
        documents.append(content)
    model = PegasusForConditionalGeneration.from_pretrained("IDEA-CCNL/Randeng-Pegasus-523M-Summary-Chinese").to(device)
    tokenizer = PegasusTokenizer.from_pretrained("IDEA-CCNL/Randeng-Pegasus-523M-Summary-Chinese")

    # tokenizer=AutoTokenizer.from_pretrained('IDEA-CCNL/Randeng-BART-139M-SUMMARY')
    # model=BartForConditionalGeneration.from_pretrained('IDEA-CCNL/Randeng-BART-139M-SUMMARY')
    sum_texts=[]
    for content in documents:
        inputs = tokenizer(content, max_length=1024, return_tensors="pt").to(device)
        summary_ids = model.generate(inputs["input_ids"])
        sum_text = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        print(sum_text)
        # text=content
        # text2text_generator = Text2TextGenerationPipeline(model, tokenizer)
        # sum_text=text2text_generator(text, max_length=50, do_sample=False)
        # # print(type(sum_text))
        # sum_text=sum_text[0]['generated_text']
        # print(sum_text)
        # exit(0)
        sum_texts.append(str(sum_text))
    with open("summary.txt", "w") as file:
    # 使用循环遍历列表中的元素，并将它们写入文件
        for item in sum_texts:
            file.write(str(item) + "\n")
    pass






def cluster_bert(num_clusters):
    model_name = "bert-base-chinese"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    text_data = []



    # sorted_answer_infos=AnswerInfo.read_files()
    # result_answer_infos=QuestionInfo.stratify_answers_by_votes(sorted_answer_infos)
        
    # for answer_info in result_answer_infos:
    #     content=answer_info.answer_content
    #     text_data.append(content)


    with open('./summary.txt', 'r') as file:
        text_data = file.readlines()


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

    for cluster_label, cluster_texts in clusters.items():
        print(f"Cluster {cluster_label}:")
        for text in cluster_texts:
            print(text)
        print("\n")







if __name__ == "__main__":
    summary()
    cluster_bert(4)
    pass
