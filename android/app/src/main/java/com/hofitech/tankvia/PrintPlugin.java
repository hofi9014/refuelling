package com.hofitech.tankvia;

import android.content.Context;
import android.print.PrintAttributes;
import android.print.PrintManager;
import android.webkit.WebView;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * window.print() does nothing in an Android WebView, so the vehicle history report is printed through
 * Android's print service instead. The page's print CSS shows only the report; "Save as PDF" is one of the printers.
 */
@CapacitorPlugin(name = "Printer")
public class PrintPlugin extends Plugin {

    @PluginMethod
    public void print(PluginCall call) {
        String name = call.getString("name", "Tankvia");
        getActivity().runOnUiThread(() -> {
            WebView webView = getBridge().getWebView();
            PrintManager printManager = (PrintManager) getActivity().getSystemService(Context.PRINT_SERVICE);
            printManager.print(name, webView.createPrintDocumentAdapter(name), new PrintAttributes.Builder().build());
            call.resolve();
        });
    }
}
