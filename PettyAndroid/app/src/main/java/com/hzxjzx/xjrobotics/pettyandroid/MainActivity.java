package com.hzxjzx.xjrobotics.pettyandroid;

import android.content.DialogInterface;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    private static final String TAG="MainActivity";
    public boolean automode = false;
    public MenuItem gMenuItem=null;
    public String add;
    public String foreAddress;
    public WebView server = findViewById(R.id.sender);
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
    inputDialog.setTitle("请输入识别码:").setView(editText);
    inputDialog.setPositiveButton("确定",
            new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    String input = editText.getText().toString();
                    add = "http://192.168.0."+input+":8888/?action=stream";
                    foreAddress = "http://192.168.0."+input+"/controls/";
                    WebView a = (WebView) findViewById(R.id.webview_1);
                    a.loadUrl(add);
                    Toast.makeText(MainActivity.this,add,Toast.LENGTH_SHORT).show();

                }
            }).show();
}

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()){
            case R.id.refresh:
                WebView a = findViewById(R.id.webview_1);a.loadUrl(add);
                Toast.makeText(MainActivity.this, "刷新成功", Toast.LENGTH_SHORT).show();
                break;
            case R.id.exit:
                finish();
                break;
            case R.id.automode:
                assert gMenuItem!=null;
                if (automode){
                    gMenuItem.setTitle("启动自动模式");
                    server.loadUrl(foreAddress+"ad");
                    automode=false;
                    Toast.makeText(MainActivity.this,"自动模式已关闭！",Toast.LENGTH_SHORT);
                }else{
                    gMenuItem.setTitle("关闭自动模式");
                    server.loadUrl(foreAddress+"au");
                    automode=true;
                    Toast.makeText(MainActivity.this,"自动模式已开启！",Toast.LENGTH_SHORT);
                }
            default:
        }
        return true;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main,menu);
        gMenuItem = menu.findItem(R.id.automode);
        return true;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        WebView a = findViewById(R.id.webview_1);
        a.getSettings().setJavaScriptEnabled(true);
        a.setWebViewClient(new WebViewClient());
//        Button u = (Button) findViewById(R.id.floatingActionButton4);
//        Button d = (Button) findViewById(R.id.floatingActionButton6);
//        Button l = (Button) findViewById(R.id.floatingActionButton5);
//        Button r = (Button) findViewById(R.id.floatingActionButton3);
//        u.setOnClickListener(new View.OnClickListener(){
//            @Override
//            public void onClick(View v){
//                server.loadUrl(foreAddress+"f");
//            }
//        });
//        d.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                server.loadUrl(foreAddress+"b");
//            }
//        });
//        l.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                server.loadUrl(foreAddress+"l");
//            }
//        });
//        r.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                server.loadUrl(foreAddress+"r");
//            }
//        });
        Log.d(TAG,"InputDialog Exec");
        showInputDialog();
        Log.d(TAG,"Exec complete.");
    }
}
