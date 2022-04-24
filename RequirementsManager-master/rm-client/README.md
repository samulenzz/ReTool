# Requirement Manager Client

## 说明

由于本人前端学习时间较短，水平有限，有的地方写的可能也不是特别好，由于时间原因注释也不是特别细致。但整体上无论命名还是代码风格都还是遵守规则的，具体的代码组织可以参考论文。

## 准备

+ 安装node.js
+ 可以安装cnpm对npm的下载进行加速
+ 安装vue-cli4：` [c]npm install @vue/cli -g`

## 安装依赖

```
[c]npm install
```

## 编译/本地热加载（一般用于本地开发）

```
[c]npm run serve
```

## 编译/压缩（用于生产环境）

```
npm run build
```

## 格式校验

```
[c]npm run lint
```

## 其他配置

See [Configuration Reference](https://cli.vuejs.org/config/).

## 生产环境下客户端的部署

客户端可以直接打包分发给用户，然后在用户本地运行；或者可以建立一个客户端服务器，用户通过浏览器可以直接访问。

对于后者，可以创建node项目，安装express，通过express快速创建web服务器，将vue打包生成的dist文件夹托管为静态资源即可，代码如下：

```
const express = requires('express')

const app = express()

app.use(express.static('./dist'))

app.listen(80, () => {
    console.log('web server running at http://127.0.0.1')
})
```

