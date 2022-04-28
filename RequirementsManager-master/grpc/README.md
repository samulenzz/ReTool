# GRPC服务构建

## 获取模型

通过[百度网盘](https://pan.baidu.com/s/1wZa3u2tWGlfS15tpDYu93A)（提取码56au）直接下载，存储在models文件夹中

## 准备CoreNLP工具包

下载CoreNLP[中文资源包](https://search.maven.org/remotecontent?filepath=edu/stanford/nlp/stanford-corenlp/4.4.0/stanford-corenlp-4.4.0-models-chinese.jar) 改名为“stanford-chinese-corenlp-yyyy-MM-dd-models.jar”，日期任选，存在CoreNLP文件夹中

下载CoreNLP[工具包](https://nlp.stanford.edu/software/stanford-corenlp-latest.zip)，解压缩，将压缩包里的内容全部放入CoreNLP文件夹中

准备jdk 1.8，且添加至环境变量，启动CoreNLP服务需要jdk

## 启动服务

安装相应依赖

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install grpcio
pip install protobuf
pip install psutil
pip install requests
pip install jieba
pip install gensim
pip install grpcio-tools
```

启动服务

```shell
python Server.py
```

会监听50051端口，提供GRPC server服务
