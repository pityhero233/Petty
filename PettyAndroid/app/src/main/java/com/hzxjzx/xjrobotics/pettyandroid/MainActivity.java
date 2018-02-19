package com.hzxjzx.xjrobotics.pettyandroid;

import android.content.DialogInterface;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;
import android.widget.EditText;


public class MainActivity extends AppCompatActivity {
    private void InputDialog(){
        final EditText inputServer = new EditText(this);
        inputServer.setFocusable(true);

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("请输入服务器IP").setIcon(R.drawable.ic_launcher_foreground).setView(inputServer).setNegativeButton(getString(R.string.negative),null).setPositiveButton(getString(R.string.positive),
                new DialogInterface.OnClickListener(){
                    public void onClick(DialogInterface dialog,int which){
                        String input = inputServer.getText().toString();
                        String add = "http://192.168.0."+input+":8888/?action=stream";
                        WebView a = (WebView) findViewById(R.id.webview_1);
                        a.loadUrl(add);
                    }
                });

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        InputDialog();
    }
}
