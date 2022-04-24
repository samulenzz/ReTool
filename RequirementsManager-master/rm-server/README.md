# Requirement Manager Server

## 准备工作

+ 准备一台装有并开启`MongoDB`的服务器
+ 准备好运行各微服务的服务器，装好Python，版本>=3.7
+ 准备部署并启动的gRPC算法服务器

## 配置

在`gateway`等文件夹下的`config.py`文件中，可以配置各个服务的地址、数据库的地址等。

## 安装/部署/启动

+ 网关：

  ```
  cd gateway
  pip3 install [-e] .
  python3 gateway/main.py flask | tornado
  ```

+ 用户管理服务：

  ```
  cd usermanager
  pip3 install [-e] .
  python3 usermanager/main.py flask | tornado
  ```

+ 项目管理服务：

  ```
  cd projectmanager
  pip3 install [-e] .
  python3 projectmanager/main.py flask | tornado
  ```

+ 需求管理服务：

  ```
  cd requirementmanager
  pip3 install [-e] .
  python3 requirementmanager/main.py flask | tornado
  ```

+ 模糊检测服务：

  ```
  cd filemanager
  pip3 install [-e] .
  python3 filemanager/main.py flask | tornado
  ```
  ```
  此外，由于模糊检测需要通过stanza调用Stanford CoreNLP，所以需要额外安装CoreNLP软件包，具体可参考如下链接
  https://stanfordnlp.github.io/stanza/client_setup.html
  ```
+ 模板管理服务：

  ```
  cd templatemanager
  pip3 install [-e] .
  python3 templatemanager/main.py flask | tornado
  ```

## 初始化/格式化数据库

```
cd usermanager
python3 scripts/create_user.py
python3 scripts/clear.py
```

```
cd projectmanager
python3 scripts/create_project.py
python3 scripts/clear.py
```

```
cd requirementmanager
python3 scripts/clear.py
```

```
cd templatemanager
python3 scripts/create_template.py
python3 scripts/clear.py
```

```
cd filemanager
python3 scripts/clear.py
```