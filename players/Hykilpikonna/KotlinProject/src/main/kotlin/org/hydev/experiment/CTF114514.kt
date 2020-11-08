package org.hydev.experiment

import org.hydev.logger.HyLogger
import org.hydev.logger.HyLoggerConfig
import org.hydev.logger.appenders.FileAppender
import javax.script.ScriptEngine
import javax.script.ScriptEngineManager
import kotlin.math.abs
import kotlin.math.roundToInt

val symbols = "+-*/%^&| ".toCharArray()

val scriptEngineManager = ScriptEngineManager()
val engine: ScriptEngine = scriptEngineManager.getEngineByName("AviatorScript")

// Combination presets for the prime method
fun getCombs(vararg strs: String) = strs.map { str -> str.split(" ").map { it.toInt() } }
val comb1 = getCombs("114514")
val comb2 = getCombs("1 14514", "11 4514", "114 514", "1145 14", "11451 4")
val comb3 = getCombs("1 1 4514", "1 14 514", "1 145 14", "1 1451 4", "11 4 514", "11 45 14", "11 451 4", "114 5 14", "114 51 4", "1145 1 4")
val comb4 = getCombs("1 1 4 514", "1 1 45 14", "1 1 451 4", "1 14 5 14", "1 14 51 4", "11 4 5 14", "11 4 51 4", "11 45 1 4", "114 5 1 4")
val comb5 = getCombs("1 1 4 5 14", "1 1 4 51 4", "1 1 45 1 4", "1 14 5 1 4", "11 4 5 1 4")
val comb6 = getCombs("1 1 4 5 1 4")
val combs = listOf(getCombs(), comb1, comb2, comb3, comb4, comb5, comb6)

val clipboard = ClipboardTools()

/**
 * TODO: Write a description for this class!
 *
 * @author HyDEV Team (https://github.com/HyDevelop)
 * @author Hykilpikonna (https://github.com/hykilpikonna)
 * @author Vanilla (https://github.com/VergeDX)
 * @since 2020-11-03 21:44
 */
fun main(args: Array<String>)
{
    // HyLogger
    HyLoggerConfig.appenders.add(FileAppender("./logs", "ctf-mini-miner.log"))
    //HyLoggerConfig.installSysOut()

    // Actual program starts
    val lastClip = clipboard.clipboardContents
    while (true)
    {
        print("\n")
        println("Waiting for clipboard...")

        // Wait for clipboard
        while (clipboard.clipboardContents == lastClip || clipboard.getInt() == null) { Thread.sleep(200) }
        println("Clipboard received!")
        val target = clipboard.getInt()!!
        findEquation(target)
    }
}

fun findEquation(target: Int)
{
    for (offsetIndex in 2..220)
    {
        val primeTotalOffset = if (offsetIndex % 2 == 0) offsetIndex / 2 else -offsetIndex / 2

        var expr = findEquationHelper(target - primeTotalOffset)

        // Apply total offset
        expr = if (primeTotalOffset >= 0) "${"-~".repeat(primeTotalOffset)}($expr)"
        else "${"~-".repeat(-primeTotalOffset)}($expr)"

        // Check expression length
        if (expr.length < 255)
        {
            println("Found! $expr")

            clipboard.clipboardContents = expr

            // Check correct
            if (engine.eval(expr).toString().toInt() == target) println("Checked, correct!")
            else error("Equation does not match :(")

            return
        }
        else continue
    }

    error("Failed to find expression :(")

//
//    // If a short enough expression is not found, use the prime number method
//    var originalPrimes = target.getPrimeFactors()
//    var primeTotalOffset = 0
//
//    // Reduce prime targets to the least "prime" number around it (Eg. 3347 -> 3346)
//    for (offset in -searchRange..searchRange)
//    {
//        if (target + offset < 0) continue
//
//        val primes = (target - offset).getPrimeFactors()
//
//        // New least "prime" number found!
//        if (primes.size > originalPrimes.size)
//        {
//            originalPrimes = primes
//            primeTotalOffset = offset
//        }
//    }
}

fun findEquationHelper(target: Int): String
{
    val originalPrimes = target.getPrimeFactors()

    var closestPrimeComb = listOf<Int>()
    var closestPrimePerm = listOf<Int>()
    var closestPrimeOffset = Int.MAX_VALUE

    // Loop through all possible separations for combinations
    for (n in 1..6)
    {
        // Loop through all combinations
        for (combination in combs[n])
        {
            // Loop through all permutations of prime numbers
            for (primePerm in organizePrimes(originalPrimes, n).permute())
            {
                if (primePerm.size != n || combination.size != n)
                {
                    print("EERRRORRR")
                }

                // Count the total offset
                var offset = 0
                for (i in 0 until n)
                {
                    offset += abs(primePerm[i] - combination[i])
                }

                // New closest found
                if (offset < closestPrimeOffset)
                {
                    closestPrimeComb = combination
                    closestPrimePerm = primePerm
                    closestPrimeOffset = offset
                }
            }
        }
    }

    // Found, construct expression
    var expr = ""
    for (i in closestPrimeComb.indices)
    {
        val value = closestPrimePerm[i]
        val actual = closestPrimeComb[i]

        expr += when
        {
            actual == value -> actual
            actual < value -> "${"~-".repeat(value - actual - 1)}~$actual"
            else -> "${"~-".repeat(actual - value)}$actual"
        }

        // Add multiplication symbol
        if (i != closestPrimeComb.size - 1) expr += "*"
    }

    // Fail
    if (expr.length > 255) return expr

    // Evaluate expression and add neg sign if necessary
    val eval = engine.eval(expr).toString().toInt()
    if (eval < 0) expr = "-$expr"
    return expr
}

fun findEquationFallback(target: Int)
{
    // The symbol brute force method
    var closest = ""
    var closestValue = Int.MIN_VALUE
    var closestOffset = Int.MAX_VALUE

    outer@for (one in symbols)
    {
        for (two in symbols)
        {
            for (three in symbols)
            {
                for (four in symbols)
                {
                    for (five in symbols)
                    {
                        val text = "1${one}1${two}4${three}5${four}1${five}4".replace(" ", "")
                        val evalString = engine.eval(text).toString()
                        if (evalString.contains("E")) continue
                        val eval = evalString.toDouble().roundToInt()

                        // New closest found
                        val offset = abs(eval - target)
                        if (offset < closestOffset)
                        {
                            closest = text
                            closestValue = eval
                            closestOffset = offset

                            if (closestOffset < 50) break@outer
                        }
                    }
                }
            }
        }
    }

    HyLogger.general.timing.time().reset()

    // Create expression
    val expr = if (closestValue <= target) "${"-~".repeat(target - closestValue)}($closest)"
    else "-(${"-~".repeat(closestValue - target)}-($closest))"

    // Check expression length
    if (expr.length < 255) println("Found! $expr")
    else findEquation(target)
}

/**
 * Organize a list of primes so that it contains ${count} numbers
 *
 * @param primes
 * @param count
 * @return
 */
fun organizePrimes(primes: List<Int>, count: Int): MutableList<Int>
{
    val new = ArrayList<Int>(primes)

    // Eg. [2, 2, 2].size < 6 -> [1, 1, 1, 2, 2, 2]
    if (primes.size < count)
    {
        for (i in 1..count - primes.size) new.add(0, 1)
        return new
    }

    // Eg. [2, 2, 2, 3, 3, 3, 5, 5, 5].size > 6 -> [2, 3, 3, 3, 4, 5, 5, 5] -> [3, 3, 4, 5, 5, 5, 6] -> [4, 5, 5, 5, 6, 9]
    while (new.size > count) new.apply { add(removeAt(0) * removeAt(0)); sort() }

    return new
}

fun Int.getPrimeFactors(): List<Int>
{
    // It is a prime
    if (this <= 2) return listOf(this)

    // Find prime numbers
    var temp = this
    val primes = ArrayList<Int>()
    for (i in 2 until temp)
    {
        while (temp % i == 0)
        {
            primes.add(i)
            temp /= i
        }
    }
    if(temp > 2) primes.add(temp)

    return primes
}

fun <T> List<T>.permute() = permuteHelper().distinct()

// https://code.sololearn.com/c24EP02YuQx3/#kt
private fun <T> List<T>.permuteHelper(): List<List<T>>
{
    if (size == 1) return listOf(this)

    val perms = mutableListOf<List<T>>()
    val sub = this[0]

    for(perm in drop(1).permuteHelper())
    {
        for (i in 0..perm.size)
        {
            val newPerm = perm.toMutableList()
            newPerm.add(i, sub)
            perms.add(newPerm)
        }
    }
    return perms
}
