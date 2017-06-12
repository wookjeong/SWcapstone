package com.jeongwook.test;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Toast;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import static java.lang.Thread.sleep;

public class StartActivity extends AppCompatActivity {

    Button exitBtn, forwardBtn, backwardBtn, homeBtn, leftBtn, rightBtn;
    Button cameraUp,cameraDown,cameraLeft,cameraRight, cameraHome;
    Button autoBtn,manualBtn;
    SeekBar speed, timesleep, leftPWM, rightPWM, homePWM;
    String address;
    public static boolean stop_auto = true;
    public static int time = 10;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);

        Intent intent = getIntent();
        address = intent.getStringExtra("ipaddress");
        /*String url = "http://" + address + ":8080/javascript_simple.html";
        WebView v = (WebView) findViewById(R.id.video);
        v.setPadding(0,0,0,0);
        v.setInitialScale(100);
        v.getSettings().setBuiltInZoomControls(false);
        v.getSettings().setJavaScriptEnabled(true);
        v.getSettings().setLoadWithOverviewMode(true);
        v.getSettings().setUseWideViewPort(true);
        v.getSettings().setLayoutAlgorithm(WebSettings.LayoutAlgorithm.NORMAL);
        v.loadUrl(url);*/

        exitBtn = (Button) findViewById(R.id.Exit);
        forwardBtn = (Button) findViewById(R.id.forward);
        backwardBtn = (Button) findViewById(R.id.backward);
        homeBtn = (Button) findViewById(R.id.home);
        leftBtn = (Button) findViewById(R.id.left);
        rightBtn = (Button) findViewById(R.id.right);
        cameraUp = (Button)findViewById(R.id.CameraUp);
        cameraLeft = (Button)findViewById(R.id.CameraLeft);
        cameraHome = (Button)findViewById(R.id.CameraHome);
        cameraRight = (Button)findViewById(R.id.CameraRight);
        cameraDown = (Button)findViewById(R.id.CameraDown);
        speed = (SeekBar)findViewById(R.id.seekBar);
        autoBtn  = (Button)findViewById(R.id.auto);
        manualBtn = (Button)findViewById(R.id.manual);
        timesleep = (SeekBar)findViewById(R.id.timesleep);
        leftPWM = (SeekBar)findViewById(R.id.LeftPWM);
        homePWM = (SeekBar)findViewById(R.id.HomePWM);
        rightPWM = (SeekBar)findViewById(R.id.RightPWM);


        forwardBtn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                int action = motionEvent.getAction();
                if (action == MotionEvent.ACTION_DOWN) {
                    new SendMessage().execute(forwardBtn.getText().toString());
                } else if (action == MotionEvent.ACTION_UP) {
                    new SendMessage().execute("stop");
                }
                return false;
            }
        });
        backwardBtn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                int action = motionEvent.getAction();
                if (action == MotionEvent.ACTION_DOWN) {
                    new SendMessage().execute(backwardBtn.getText().toString());
                } else if (action == MotionEvent.ACTION_UP) {
                    new SendMessage().execute("stop");
                }
                return false;
            }
        });

        leftBtn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                int action = motionEvent.getAction();
                if (action == MotionEvent.ACTION_DOWN) {
                    new SendMessage().execute(leftBtn.getText().toString());
                    new SendMessage().execute(forwardBtn.getText().toString());
                } else if (action == MotionEvent.ACTION_UP) {
                    new SendMessage().execute("stop");
                }
                return false;
            }
        });
        rightBtn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                int action = motionEvent.getAction();
                if (action == MotionEvent.ACTION_DOWN) {
                    new SendMessage().execute(rightBtn.getText().toString());
                    new SendMessage().execute(forwardBtn.getText().toString());
                } else if (action == MotionEvent.ACTION_UP) {
                    new SendMessage().execute("stop");
                }
                return false;
            }
        });
        homeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {new SendMessage().execute(homeBtn.getText().toString());}
        });
        exitBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                System.exit(1);
            }
        });
        cameraUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new SendMessage().execute("y+");
            }
        });
        cameraDown.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new SendMessage().execute("y-");
            }
        });
        cameraHome.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {new SendMessage().execute("xy_home");}
        });
        cameraRight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {new SendMessage().execute(cameraRight.getText().toString());}
        });
        cameraLeft.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){new SendMessage().execute("cameraleft");}
        });
        autoBtn.setOnClickListener(new View.OnClickListener() {
            @Override
                public void onClick(View v) {
                new SendMessage().execute("auto");
                stop_auto = false;/*
                while (stop_auto==false) {
                    new SendMessage().execute("auto");
                    try{
                        Thread.sleep(2000);
                    }catch(InterruptedException e){
                        e.printStackTrace();
                    }
                   ;*/


            }
        });
        manualBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stop_auto = true;
                Log.e("stop auto 내용: ", "확인 "+stop_auto);
            }



        });

        speed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            int Changedprogress =0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                Changedprogress = progress;
            }
            public void onStartTrackingTouch(SeekBar seekBar){

            }
            public void onStopTrackingTouch(SeekBar seekBar){
                Toast.makeText(StartActivity.this, "Speed is : " + Changedprogress, Toast.LENGTH_SHORT).show();
                new SendMessage().execute("speed"+Changedprogress);
            }
        });

        timesleep.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){


            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                time = progress;
            }
            public void onStartTrackingTouch(SeekBar seekBar){

            }
            public void onStopTrackingTouch(SeekBar seekBar){
                Toast.makeText(StartActivity.this, "Time auto is : " + time, Toast.LENGTH_SHORT).show();
            }
        });
        leftPWM.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
                int leftpwm = 350;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                leftpwm = progress * 10 + 200;
            }
            public void onStartTrackingTouch(SeekBar seekBar){

            }
            public void onStopTrackingTouch(SeekBar seekBar){
                Toast.makeText(StartActivity.this, "Left Pwm is : " + leftpwm, Toast.LENGTH_SHORT).show();
            }
        });
        homePWM.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            int homepwm = 450;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                homepwm = progress * 10 + 400;
            }
            public void onStartTrackingTouch(SeekBar seekBar){

            }
            public void onStopTrackingTouch(SeekBar seekBar){
                Toast.makeText(StartActivity.this, "Home Pwm is : " + homepwm, Toast.LENGTH_SHORT).show();
            }
        });
        rightPWM.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            int rightpwm = 550;
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                rightpwm = progress * 10 + 500;
            }
            public void onStartTrackingTouch(SeekBar seekBar){

            }
            public void onStopTrackingTouch(SeekBar seekBar){
                Toast.makeText(StartActivity.this, "Right Pwm is : " + rightpwm, Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    protected void onStart() {
        super.onStart();
        Thread myThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while(true){
                    try{
                        while(stop_auto);
                        Thread.sleep(600);
                        new SendMessage().execute("auto\n");
                    }catch (Exception e){

                    }

                }
            }
        });
   myThread.start();
    }

    public class SendMessage extends AsyncTask<String, Void, Void> {
        private Exception exception;

        @Override
        protected Void doInBackground(String... params) {
            try {
                try {
                    Socket socket = new Socket(address, 21567);
                    PrintWriter out = new PrintWriter(
                            new OutputStreamWriter(
                                    socket.getOutputStream()));
                    out.print(params[0]);
                    Log.w("PARAMS내용", params[0]);
                    out.flush();
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } catch (Exception e) {
                this.exception = e;
                return null;
            }
            return null;
        }
    }
}
