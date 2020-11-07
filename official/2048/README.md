# 2048

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

这正是游戏失败时的提示信息，如果访问 `/getflxg?my_favorite_fruit=banana`，则可以得到正确的 flag。

有的同学可能会好奇为什么 `('b'+'a'+ +'a'+'a').toLowerCase()` 的计算结果是 `banana`，这个问题可以参考：https://stackoverflow.com/questions/57456188/why-is-the-result-of-ba-a-a-tolowercase-banana 。
