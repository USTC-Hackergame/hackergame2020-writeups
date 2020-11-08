package org.hydev.experiment

import org.apache.http.client.entity.UrlEncodedFormEntity
import org.apache.http.client.methods.HttpGet
import org.apache.http.client.methods.HttpPost
import org.apache.http.client.protocol.HttpClientContext
import org.apache.http.impl.client.BasicCookieStore
import org.apache.http.impl.client.HttpClients
import org.apache.http.impl.cookie.BasicClientCookie
import org.apache.http.message.BasicNameValuePair
import org.apache.http.util.EntityUtils
import org.hydev.logger.HyLoggerConfig
import org.hydev.logger.appenders.FileAppender
import java.awt.Robot
import java.awt.event.KeyEvent.*
import java.io.File

/**
 * TODO: Write a description for this class!
 *
 * @author HyDEV Team (https://github.com/HyDevelop)
 * @author Hykilpikonna (https://github.com/hykilpikonna)
 * @author Vanilla (https://github.com/VergeDX)
 * @since 2020-11-02 15:51
 */
fun main(args: Array<String>)
{
    // HyLogger
    HyLoggerConfig.appenders.add(FileAppender("./logs", "ctf.log"))
    HyLoggerConfig.installSysOut()

    // Create http client
    val builder = HttpClients.custom()
    val context = HttpClientContext.create()
    val cookies = BasicCookieStore()
    context.cookieStore = cookies
    builder.setDefaultCookieStore(cookies)
    val client = builder.build()

    // Constants
    val regex = """(?<=<p> \$).*(?=\$)""".toRegex()
    val numberRegex = """(?<= )[0-9]*(?= 题)""".toRegex()

    // CTF session
    val sessionFile = File("session")
    cookies.addCookie(BasicClientCookie("session", sessionFile.readText().replace("\n", ""))
        .apply { domain = "202.38.93.111" })

    // Clipboard
    val clipboard = ClipboardTools()

    // Robot: Keyboard control
    val robot = Robot()
    fun press(vararg events: Int)
    {
        events.forEach { robot.keyPress(it) }
        robot.delay(100)
        events.forEach { robot.keyRelease(it) }
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

        // Get request
        val get = HttpGet("http://202.38.93.111:10190/")
        val response = client.execute(get)
        val html = EntityUtils.toString(response.entity, "UTF-8")
        val questionsRemaining = numberRegex.find(html)!!.value.toInt()
        println("Questions remaining: $questionsRemaining")
        val tex = regex.find(html)!!.value
        response.close()

        // Do the last one on the website by yourself
        if (questionsRemaining == 1)
        {
            println("===============FINISH================")
            println("Now copy the session and override your browser cookie, " +
                "then complete the last question in your browser to get the flag.")
            return
        }

        // Tex to function, copy
        val eq = toEquation(tex)
        println(eq)
        clipboard.clipboardContents = eq

        // Robot: Auto paste and enter (META is the macOS command key. IF you're on Windows, change this to CONTROL)
        press(VK_META, VK_V)
        robot.delay(100)
        press(VK_ENTER)
        Thread.sleep(1000)

        // Robot: Auto copy result
        press(VK_UP)
        robot.delay(100)
        press(VK_META, VK_C) // META: same here :)
        robot.delay(100)
        press(VK_DOWN)

        // Wait for clipboard
        while (clipboard.getDouble() == null) { Thread.sleep(200) }
        println("Clipboard received!")
        val ans = clipboard.getDouble()

        // Send response
        val post = HttpPost("http://202.38.93.111:10190/submit")
        post.addHeader("content-type", "application/x-www-form-urlencoded")
        post.entity = UrlEncodedFormEntity(listOf(BasicNameValuePair("ans", String.format("%.6f", ans))), "UTF-8")
        val result = client.execute(post)
        result.close()
    }
}

fun toEquation(originalTex: String): String
{
    val tex = originalTex
        .replace("\\left(", "(").replace("\\right)", ")").replace("\\,", " ")
        .replace("{", "(").replace("}", ")")
        .replace("\\", "")
        .shortenSpaces()
    return toEquationHelper(tex)
        .replace("x (", "x * (").replace("x(", "x * (") // Fix implied multiplication error
}

fun toEquationHelper(originalTex: String): String
{
    var tex = originalTex

    if (tex.startsWith("int_("))
    {
        tex = tex.substring(5, tex.length - 6)
        val upper = tex.substring(0, tex.findBracket())
        tex = tex.substring(upper.length + 3)
        val lower = tex.substring(0, tex.findBracket())
        tex = tex.substring(lower.length + 2)
        return "integral(${toEquation(tex)},x,${toEquation(upper)},${toEquation(lower)})"
    }

    // Change fractions
    while (tex.contains("frac("))
    {
        // frac(1)(2) -> (1)/(2)
        val loc = tex.indexOf("frac(")
        val endBrack = tex.findBracket(start = loc + 5)
        tex = tex.substring(0, loc) + tex.substring(loc + 4, endBrack + 1) + "/" + tex.substring(endBrack + 1)
    }

    return tex
}

/**
 * Find the index of the end bracket
 *
 * @param bracket { or (
 * @param start Start index
 * @return
 */
fun String.findBracket(bracket: Boolean = false, start: Int = 0): Int
{
    val open = if (bracket) '{' else '('
    val close = if (bracket) '}' else ')'

    var level = 0
    var i = start

    while (i < length)
    {
        val c = this[i]

        if (c == close)
        {
            if (level == 0) return i
            else level--
        }
        if (c == open) level++;

        i++
    }

    return -1
}

/**
 * Reduce double spaces to single spaces
 *
 * @return Shortened string
 */
fun String.shortenSpaces(): String
{
    var s = this
    while (s.contains("  ")) s = s.replace("  ", " ")
    return s
}
