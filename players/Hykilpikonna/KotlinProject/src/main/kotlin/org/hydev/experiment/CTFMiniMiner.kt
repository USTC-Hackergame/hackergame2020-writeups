package org.hydev.experiment

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonConfiguration
import org.apache.http.client.methods.HttpPost
import org.apache.http.client.protocol.HttpClientContext
import org.apache.http.impl.client.BasicCookieStore
import org.apache.http.impl.client.HttpClients
import org.apache.http.util.EntityUtils
import org.hydev.logger.HyLoggerConfig
import org.hydev.logger.appenders.FileAppender
import java.io.File
import java.net.URLEncoder


/**
 * TODO: Write a description for this class!
 *
 * @author HyDEV Team (https://github.com/HyDevelop)
 * @author Hykilpikonna (https://github.com/hykilpikonna)
 * @author Vanilla (https://github.com/VergeDX)
 * @since 2020-11-03 16:19
 */
fun main(args: Array<String>)
{
    // Json
    val json = Json(JsonConfiguration(isLenient = true))

    // HyLogger
    HyLoggerConfig.appenders.add(FileAppender("./logs", "ctf-mini-miner.log"))
    HyLoggerConfig.installSysOut()

    // Create http client
    val builder = HttpClients.custom()
    val context = HttpClientContext.create()
    val cookies = BasicCookieStore()
    context.cookieStore = cookies
    builder.setDefaultCookieStore(cookies)
    val client = builder.build()

    // API stuff
    val baseUrl = "http://localhost:8088/api/"
    val token = File("mini-miner-token.txt").readText().replace("\n", "")

    fun post(api: String, params: String): String
    {
        // Create post
        val url = "$baseUrl$api?token=${token.urlEncode()}$params"
        val post = HttpPost(url).apply {
            addHeader("accept", "*/*")
            addHeader("content-type", "application/json;charset=UTF-8")
        }

        // Execute
        val response = client.execute(post)
        val responseBody = EntityUtils.toString(response.entity, "UTF-8")
        response.close()

        // Error
        if (response.statusLine.statusCode != 200)
        {
            println("Error $api - Params: $params ; Status code: ${response.statusLine.statusCode} ; Response body: $responseBody")
        }

        // Return body
        return responseBody
    }
    fun state() = json.parse(StateReturn.serializer(), post("state", "&x=0&y=0"))
    fun reset() = json.parse(ResetReturn.serializer(), post("reset", ""))
    fun damage(x: Int, y: Int) = json.parse(DamageReturn.serializer(), post("damage", "&x=$x&y=$y&material=OBSIDIAN"))


    // Actual code begins


    while (true)
    {
        // Reset and get current state
        println(reset())
        val state = state()

        // Find flag
        var flagX = 0
        var flagY = 0
        for (x in 0..state.materials.size)
        {
            if (state.materials[x].contains("FLAG"))
            {
                flagX = x
                flagY = state.materials[x].indexOf("FLAG")
                break
            }
        }

        println("$flagX,$flagY")

        // Destroy block, wait for it to complete (long = 5s)
        damage(flagX, flagY)
        Thread.sleep(5500)

        // Destroy air, have roughly 3s until it checks the flag again
        Thread {
            val result = damage(flagX, flagY)
            println(result)
        }.start()

        Thread.sleep(500)
        reset() // Reset the flag block

    }
}

@Serializable
data class ResetReturn(
    val expiration: String,
    val user: String
)

@Serializable
data class StateReturn(
    val materials: List<List<String>>,
    val min: List<Int>
)

@Serializable
data class DamageReturn(
    val dropped: String,
    val flag: String
)

fun String.urlEncode(): String = URLEncoder.encode(this, "UTF-8")
