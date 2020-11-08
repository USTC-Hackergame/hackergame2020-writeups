package org.hydev.experiment

import java.awt.Toolkit
import java.awt.datatransfer.*

/**
 * http://www.javapractices.com/topic/TopicAction.do?Id=82
 */
class ClipboardTools : ClipboardOwner
{
    /**
     * Empty implementation of the ClipboardOwner interface.
     */
    override fun lostOwnership(clipboard: Clipboard, contents: Transferable) {}

    fun getDouble() = clipboardContents!!.replace("−", "-").toDoubleOrNull();
    fun getInt() = clipboardContents!!.replace("−", "-").toIntOrNull();

    /**
     * Get and set the clipboard contents
     */
    var clipboardContents: String?
        get()
        {
            var result = ""
            val clipboard = Toolkit.getDefaultToolkit().systemClipboard
            val contents = clipboard.getContents(null)
            val hasTransferableText = contents != null && contents.isDataFlavorSupported(DataFlavor.stringFlavor)
            if (hasTransferableText)
            {
                try
                {
                    result = contents!!.getTransferData(DataFlavor.stringFlavor) as String
                }
                catch (ex: Exception)
                {
                    ex.printStackTrace()
                }
            }
            return result
        }
        set(string)
        {
            val stringSelection = StringSelection(string)
            val clipboard = Toolkit.getDefaultToolkit().systemClipboard
            clipboard.setContents(stringSelection, this)
        }
}
