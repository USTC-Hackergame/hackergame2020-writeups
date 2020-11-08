package org.hydev.experiment

import com.google.zxing.BarcodeFormat.QR_CODE
import com.google.zxing.BinaryBitmap
import com.google.zxing.DecodeHintType.*
import com.google.zxing.client.j2se.BufferedImageLuminanceSource
import com.google.zxing.common.BitSource
import com.google.zxing.common.GlobalHistogramBinarizer
import com.google.zxing.multi.GenericMultipleBarcodeReader
import com.google.zxing.qrcode.QRCodeReader
import org.apache.commons.io.FileUtils
import java.io.File
import java.lang.System.err
import java.nio.charset.Charset
import javax.imageio.ImageIO

// 这个是要改 ZXing 源码才会把解析的 byte[] 加进来啦w
var parsedBytes = byteArrayOf();

/**
 * TODO: Write a description for this class!
 *
 * @author HyDEV Team (https://github.com/HyDevelop)
 * @author Hykilpikonna (https://github.com/hykilpikonna)
 * @author Vanilla (https://github.com/VergeDX)
 * @since 2020-11-05 18:27
 */
fun main(args: Array<String>)
{
    var rawBytes = byteArrayOf()
    var utfBytes = byteArrayOf()
    var iso8859Bytes = byteArrayOf()

    File("/Users/hykilpikonna/Downloads/CTF/qr-frames").listFiles()!!.sorted().forEach {

            try
            {
                val source = BufferedImageLuminanceSource(ImageIO.read(it))
                val bitmap = BinaryBitmap(GlobalHistogramBinarizer(source))
                val reader = GenericMultipleBarcodeReader(QRCodeReader())
                val hints = mapOf(TRY_HARDER to true, POSSIBLE_FORMATS to QR_CODE, PURE_BARCODE to true)

                val result = reader.decodeMultiple(bitmap, hints)[0]

                rawBytes += result.rawBytes
                utfBytes += result.text.toByteArray(Charset.forName("UTF-16"))
                iso8859Bytes += result.text.toByteArray(Charset.forName("ISO-8859-1"))
            }
            catch (e: Exception)
            {
                err.println(it)
                e.printStackTrace()
            }
        }

    val bits = BitSource(rawBytes)
    val readBytes = ByteArray(rawBytes.size)
    for (i in rawBytes.indices)
    {
        readBytes[i] = bits.readBits(8).toByte()
    }

    FileUtils.writeByteArrayToFile(File("./qr_bytes_raw_processed"), parsedBytes)
}
