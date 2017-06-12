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
            //라즈베리파이를 키면 자동으로 연결되는 IP주소 두개를 설정 해놓았다. 핫스팟을 사용했기 때문에 지정해놓았고 TCP SERVER에서 반응이있으면 연결 성공으로 해야 한다 
            Intent intent = new Intent(getApplicationContext(), StartActivity.class);
            intent.putExtra("ipaddress", adress.getText().toString());
            startActivity(intent);
            System.exit(1);
            //새로운 Activity로 넘어가고 현재 Activity는 종료
        }else Toast.makeText(this, "틀린 IP주소 입니다.", Toast.LENGTH_SHORT).show();
    }

}
