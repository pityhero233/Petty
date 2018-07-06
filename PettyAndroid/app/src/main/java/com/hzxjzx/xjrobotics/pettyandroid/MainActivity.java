package com.hzxjzx.xjrobotics.pettyandroid;

import android.content.DialogInterface;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.Window;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.Toast;
import android.os.Build.VERSION;
import android.view.WindowManager;
import android.os.Build.VERSION_CODES;
import android.graphics.Color;

public class MainActivity extends AppCompatActivity {
    private static final String TAG="MainActivity";
    public boolean automode = false;
    public MenuItem gMenuItem=null;
    public String add;
    public String foreAddress;
    //public WebView server;

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
                    WebView a = findViewById(R.id.webview_1);
                    a.loadUrl(add);
                    Toast.makeText(MainActivity.this,add,Toast.LENGTH_SHORT).show();

                }
            }).show();
}
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        WebView server = findViewById(R.id.sender);
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
                    server.loadUrl(foreAddress+"__AutoModeDown");
                    automode=false;
                    Toast.makeText(MainActivity.this,"自动模式已关闭！",Toast.LENGTH_SHORT).show();
                }else{
                    gMenuItem.setTitle("关闭自动模式");
                    server.loadUrl(foreAddress+"__AutoModeUp");
                    automode=true;
                    Toast.makeText(MainActivity.this,"自动模式已开启！",Toast.LENGTH_SHORT).show();
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
        //requestWindowFeature(Window.FEATURE_NO_TITLE);
//        if(VERSION.SDK_INT >= VERSION_CODES.LOLLIPOP) {
//            Window window = getWindow();
//            window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS
//                    | WindowManager.LayoutParams.FLAG_TRANSLUCENT_NAVIGATION);
//            window.getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
//                    | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
//                    | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
//            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
//            window.setStatusBarColor(Color.TRANSPARENT);
//            window.setNavigationBarColor(Color.TRANSPARENT);
//        }
        setContentView(R.layout.activity_main);
        Log.e(TAG,"load complete.");
        final WebView server = findViewById(R.id.sender);
        WebView a = (WebView) findViewById(R.id.webview_1);
        a.getSettings().setJavaScriptEnabled(true);
        a.setWebViewClient(new WebViewClient());
        FloatingActionButton u = (FloatingActionButton) findViewById(R.id.floatingActionButton4);
        FloatingActionButton d = (FloatingActionButton) findViewById(R.id.floatingActionButton6);
        FloatingActionButton l = (FloatingActionButton) findViewById(R.id.floatingActionButton5);
        FloatingActionButton r = (FloatingActionButton) findViewById(R.id.floatingActionButton3);
        u.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                server.loadUrl(foreAddress+"__MoveForward");
            }
        });
        d.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                server.loadUrl(foreAddress+"__MoveBackward");
            }
        });
        l.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                server.loadUrl(foreAddress+"__MoveLeft");
            }
        });
        r.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                server.loadUrl(foreAddress+"__MoveRight");
            }
        });
        Log.d(TAG,"InputDialog Exec");
        showInputDialog();
        Log.d(TAG,"Exec complete.");
    }
}
