# 向量搜索(1) Faiss入门、通义千问embedding

[文档](help.aliyun.com/zh/dashscope/developer-reference/text-embedding-quick-start)

https://github.com/facebookresearch/faiss
用于高效相似性搜索和密集向量聚类的库



安装
需要通义千问的dashscope 的key，可以去官网进行申请

```
pip install langchain-community
pip install dashscope
pip install faiss-cpu
pip install faiss-gpu(可以你的电脑支持)
```

# 向量数据库
## faiss

支持CPU和GPU计算可以处理海量的向量数据，支持多种索引方式提供了Python接口，可以与Numpy完美衔接。
FAISS的优点是速度快、灵活、可扩展，缺点是安装依赖复杂、使用门槛高、不支持元数据存储。

## Chroma

本地数据库

chroma是一个用于构建带有嵌入向量的AI应用程序的数据库，内置了入门所需的一切，并提供了简单的API。
它目前只支持CPU计算，但可以利用乘积量化的方法将一个向量的维度切成多段，每段分别进行k-means，从而减少存储空间和提高检索效率。
它还可以与Langchain集成，实现基于语言模型的应用。chroma的优点是易用、轻量、智能，缺点是功能相对简单、不支持GPU加速

FAISS支持L2距离和内积两种相似度度量，chroma支持L2距离、内积和余弦相似度
三种相似度度量。

### 地址
这是github地址
https://github.com/chroma-core/chroma

### 安装
```bash
pip install chromadb
```

## qdrant(推荐)
官方介绍，adrant的优点包括
1. 其高性能和高可扩展性，易于使用的API2、可以内存、硬盘、Docker、cloud等多种模式使用
2. 有效管理计算资源，特别适用云原生部署
3. rust语言编写，性能优秀，支持多种索引方式，支持多种相似度度量
4. 支持多模态数据库/rag（+Aleph Alpha embedding技术）

### 地址
[官方地址](github.com/qdrant/gdrant-client)
### 安装

#### 服务端
```bash
docker pull qdrant/qdrant:v1.10.0

docker run -d --name dqrant -p 6333:6333 \
-v $(pwd)/dqrant_data:/dqrant/storage qdrant/qdrant:v1.10.0
```
在浏览器中输入http://localhost:6333/dashboard 或者公网地址可以看到qdrant的管理界面

如果要添加安全认证，可以使用nginx反向代理，进行安全认证（自行ai搜索）

#### 客户端
```bash
pip install qdrant-client
pip install -U langchain-qdrant
```

#### 如何相对精准搜索
我们在搜索关键词 "golang程序员工资待遇如何" 出来最相似的是最相似的应该是【工资待遇分析】而不是【golang程序员如何看待自己的工资待遇】

要实现相对精度的搜索:
在插入到数据库时候需要人工操作，要先打好标签在插入，比如#薪资#待遇, 在插入的是时候把标签插入到metadata中，在搜索的时候再根据标签进行过滤





