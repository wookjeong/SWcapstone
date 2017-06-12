package com.jeongwook.test;


import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {
    EditText adress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }
    public void button(View v){
        adress = (EditText) findViewById(R.id.ipaddress);
        if(adress.getText().toString().equals("192.168.0.13") || adress.getText().toString().equals("172.20.10.6")){
            Intent intent = new Intent(getApplicationContext(), StartActivity.class);
            intent.putExtra("ipaddress", adress.getText().toString());
            startActivity(intent);
            System.exit(1);
        }else Toast.makeText(this, "틀린 IP주소 입니다.", Toast.LENGTH_SHORT).show();
    }

}
