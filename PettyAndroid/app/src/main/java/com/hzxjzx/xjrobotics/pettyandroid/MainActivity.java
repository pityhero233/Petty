package com.hzxjzx.xjrobotics.pettyandroid;

import android.content.DialogInterface;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    private static final String TAG="MainActivity";
//    private void InputDialog(){
//        final EditText inputServer = new EditText(this);
//        inputServer.setFocusable(true);
//
//        AlertDialog.Builder builder = new AlertDialog.Builder(this);
//        builder.setTitle("请输入服务器IP").setIcon(R.drawable.ic_launcher_foreground).setView(inputServer).setNegativeButton(getString(R.string.negative),null).setPositiveButton(getString(R.string.positive),
//                new DialogInterface.OnClickListener(){
//                    public void onClick(DialogInterface dialog,int which){
//                        String input = inputServer.getText().toString();
//                        String add = "http://192.168.0."+input+":8888/?action=stream";
//                        WebView a = (WebView) findViewById(R.id.webview_1);
//                        a.loadUrl(add);
//                    }
//                }).show();
//    }
    private void showInputDialog() {
    /*@setView 装入一个EditView
     */
    final EditText editText = new EditText(MainActivity.this);
    editText.setText(getText(R.string.ipdefault));
    AlertDialog.Builder inputDialog =
            new AlertDialog.Builder(MainActivity.this);
    inputDialog.setTitle("请输入ip:").setView(editText);
    inputDialog.setPositiveButton("确定",
            new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    String input = editText.getText().toString();
                    String add = "http://192.168.0."+input+":8888/?action=stream";
                    WebView a = (WebView) findViewById(R.id.webview_1);
                    a.loadUrl(add);
                    Toast.makeText(MainActivity.this,add,Toast.LENGTH_SHORT).show();

                }
            }).show();
}
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        WebView a = findViewById(R.id.webview_1);
        a.getSettings().setJavaScriptEnabled(true);
        a.setWebViewClient(new WebViewClient());
        Log.d(TAG,"InputDialog Exec");
        showInputDialog();
        Log.d(TAG,"Exec complete.");
    }
}
