# 2048

好熟悉啊，但我真的不会玩 2048，还是右键看一下游戏代码好了。

看了一圈代码，发现游戏胜利之后执行的逻辑代码在 `static/js/html_actuator.js` 中：

```js
HTMLActuator.prototype.message = function (won) {
  var type    = won ? "game-won" : "game-over";
  var message = won ? "FLXG 大成功！" : "FLXG 永不放弃！";

  var url;
  if (won) {
    url = "/getflxg?my_favorite_fruit=" + ('b'+'a'+ +'a'+'a').toLowerCase();
  } else {
    url = "/getflxg?my_favorite_fruit=";
  }

  let request = new XMLHttpRequest();
  request.open('GET', url);
  request.responseType = 'text';

  request.onload = function() {
    document.getElementById("game-message-extra").innerHTML = request.response;
  };

  request.send();

  this.messageContainer.classList.add(type);
  this.messageContainer.getElementsByTagName("p")[0].textContent = message;

  this.clearContainer(this.sharingContainer);
  this.sharingContainer.appendChild(this.scoreTweetButton());
  twttr.widgets.load();
};
```

看来是经典 js 字符串拼接，于是 `'b'+'a'+ +'a'+'a'` 会变成 `"baNaNa"`（直接粘贴到下面 console 里回车也能给出来），那么直接请求 `/getflxg?my_favorite_fruit=banana` 就可以看到 flag。（这里略微 cheese 了一下，因为后端并没有验证参数大小写所以小写香蕉也可以

（……果然这道题的 flag 格式还是变成了 `废理兴工{...}`