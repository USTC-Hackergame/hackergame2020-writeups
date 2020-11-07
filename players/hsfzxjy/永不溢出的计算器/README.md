# 永不溢出的计算器

思路基本同官方。鉴于本题没有提供 TCP 接口，这里给出一个在浏览器里搜索不同二次剩余的脚本。

将以下代码贴在浏览器控制台运行即可。如果脚本停了，最后输出的两个数即是所要的 x 和 y。

此处的原理是利用页面暴露在全局的 WebSocket 对象 `socket` 直接收发数据。

```javascript
(() => {
    function rand(a, b) {
        return Math.round(Math.random() * (b - a) + a)
    }

    function selectLargeNum() {
        const len = Math.round(rand(154, 307))
        let ret = ''
        for (let i = 0; i < len; i++) ret += rand(0, 9)
        return ret.replace(/^0+/, '')
    }

    class Result {
        constructor() {
            this.reset()
        }
        reset() {
            this.promise = new Promise(resolve => this.resolve = resolve)
            this.text = ''
        }
    }

    let result = new Result
    socket.addEventListener('message', (msg) => {
        result.text += msg.data
        if (! /\r\n>\s+$/.test(result.text)) return
        result.resolve(/(\d+)\r\n>\s+$/.exec(result.text)[1])
    })


    async function loop() {
        let num = selectLargeNum()
        result.reset()
        socket.send(num + ' ^ 2\n')
        let res = await result.promise
        result.reset()
        socket.send('sqrt(' + res + ')\n')
        res = await result.promise
        console.log(res)
        console.log(num)
        if (num !== res) return
        setTimeout(loop, 100)
    }

    loop()
})()
```