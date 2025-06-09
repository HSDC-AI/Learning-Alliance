# HTTP 权威指南边读边写

之前总是针对着接口开发，从没有关注过一个请求发出去之后，服务器（也就是tomecat/jetty 之类的应用服务器)会去做什么，也才从来没有关注过request header 都有哪些用处，以及不同header 在不同的layer的作用，那么从开始读这本书后，就开始慢慢梳理一下书中的某一些关于HTTP，而且是在实际项目中很有用的知识点。


## HTTP WEB的基础

当今不管是WEB还是APP都是建立在HTTP的基础之上，至少绝大多数都是通过HTTP进行通讯（也包括spring cloud之间的一些components的信息传递）

> ##### header
> Content-type 也就是MIME类型，web服务器会给所有资源添加这个header来描述文件的类型，这个header在request/response header中都可以返回，并且指代的文档也有所不一致。如果你返回一个HTML并且response header中标记Content-type是text/html那么浏览器会自动渲染你返回的HTML到页面，但是如果你设置了request header Accept:text/plain， 那么返回的html则不会被渲染
> * HTML text/html
> * ASCII 文本文档 text/plain
> * JPEG image/jpeg
> * json application/json



URI：资源定位符 Uniform Resource Identifier
URL：Uniform Resource Location
URN: Uniform Resource Name

URN目前为止几乎是很少见的，它与URL不同的是URL根据path找资源，URN是根据资源名字，即使资源在服务器中的某一处，URN也能找到。
******

HTTP是一个应用协议，不负责实现，实现是通过TCP/IP来实现的

![http network protocol stack](/Learning-Alliance/docs/H/HTTP/http-network-protocol-stack.png)


之前我面试别人的时候就给别人出过这样一道题目：what's happening when you access an URL on browser bar?

虽然很基础，但是很考验对HTTP的理解

![the process of the browser how to parse the request](/Learning-Alliance/docs/H/HTTP/process-of-parse-request.png)

* 浏览器从URL中解析出服务器的主机名
* 浏览器将服务器的主机名转换成服务器的IP地址
* 浏览器将端口号（如果有）从URL中解析出来
* 浏览器建立一条与web服务器的TCP连接
* 浏览器向服务器发送一条HTTP request
* 服务器向浏览器回送一条HTTP response
* 关闭连接，浏览器显示文档

> HTTP的默认端口是80， HTTPS的默认端口是443


## HTTP 1.0 vs HTTP 1.1 的区别

| 特性 | HTTP 1.0 | HTTP 1.1 |
|------|-----------|-----------|
| 连接方式 | 短连接(每个请求都需要建立TCP连接) | 长连接(默认keep-alive，可复用TCP连接) |
| 带宽优化 | 不支持断点续传 | 支持断点续传，通过Range头实现 |
| 缓存处理 | 支持If-Modified-Since, Expires | 新增Cache-Control, ETag等缓存头 |
| HOST头 | 不支持 | 必须包含HOST头，支持虚拟主机 |
| 状态码 | 较少，不够完善 | 新增了24个状态码，如100(Continue) |
| 请求方法 | GET, POST, HEAD | 新增PUT, DELETE, OPTIONS, TRACE等方法 |
| 带宽优化 | 不支持资源分块传输 | 支持分块传输(chunked transfer) |
| 多语言 | 不支持 | 支持内容协商(可返回最适合客户端的版本) |




******

这小部分来记录一下HTTP的状态码，1xx和2xx暂时不表，个人理解也就一个200是值得记一下的。

![3xx status code](/Learning-Alliance/docs/H/HTTP/3xx.png)

302/303/307 都是表示需要浏览器做一次跳转的，303 是HTTP 1.1中的规范，而且这三个状态码是要配合Location这个response header一起的，Location会记录具体要跳转到哪里，我试过强行把状态码返回200但是也返回Location，这里浏览器会报错，也并不会去真的跳转。

***

![common headers](/Learning-Alliance/docs/H/HTTP/common-headers.png)
![secure headers](/Learning-Alliance/docs/H/HTTP/secure-headers.png)

Authenorization是我在工作中用到的一个重要header，浏览器和winwods生成一个密钥串，由Kerbors进行解析最后实现auto login的功能。

Cookie 更不用说，没有cookie就没有登录，现如今绝大多数的网站登录信息都会被记录到Cookie中，细心的你会发现如果登录一些国外的网站，他们会有cookie consent的功能，因为Cookie中的信息会触犯合规法案。

##
20250609
密码的，公司黄了，学这鸡毛也没用了，网关这种应用如果下次还能碰上再系统学吧。HTTP先告一段落