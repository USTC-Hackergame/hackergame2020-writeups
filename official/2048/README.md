# 2048

- 题目分类：web

- 题目分值：100

> 路漫漫其修远兮，FLXG 永不放弃！

要实现 FLXG，你需要过人的智慧，顽强的意志，和命运的眷属。只有在 2048 的世界里证明自己拥有这些宝贵的品质，实现「大成功」，你才有资格扛起 FLXG 的大旗。

[打开/下载题目](http://202.38.93.111:10005/?token={token})

---

本题是根据 https://github.com/volltin/flxg-2048/ 改变，所有方块的名称来自于某位老学长的长篇连载小说。


## 简单做法

通关，合并出「大成功」，就能得到 flag。

注意：如果在合并出「大成功」的同时方块无法移动了，算输 qwq。

## 复杂做法

查看网页源代码，发现提示：

```html
  <!-- 
    changelog:
    - 2020/10/31 getflxg @ static/js/html_actuator.js
  -->
```

进而打开 `static/js/html_actuator.js` 这个文件，找到和游戏胜利有关的逻辑：

```javascript
var url;
  if (won) {
    url = "/getflxg?my_favorite_fruit=" + ('b'+'a'+ +'a'+'a').toLowerCase();
  } else {
    url = "/getflxg?my_favorite_fruit=";
  }

  let request = new XMLHttpRequest();
  request.open('GET', url);
```

如果访问 `/getflxg?my_favorite_fruit=` 可以得到返回信息：

> 还没有大成功，不能给你 flxg。

这正是游戏失败时的提示信息。

我们打开 Chrome 浏览器的开发者工具，切换到 Console 标签页，执行一下 `('b'+'a'+ +'a'+'a').toLowerCase()`，得到正确的应该填入的值为 `banana`，访问 `/getflxg?my_favorite_fruit=banana`，则可以得到正确的 flag。

有的同学可能会好奇为什么 `('b'+'a'+ +'a'+'a').toLowerCase()` 的计算结果是 `banana`，这个问题可以参考：https://stackoverflow.com/questions/57456188/why-is-the-result-of-ba-a-a-tolowercase-banana 。
