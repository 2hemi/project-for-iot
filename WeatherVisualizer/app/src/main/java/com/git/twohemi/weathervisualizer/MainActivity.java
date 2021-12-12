package com.git.twohemi.weathervisualizer;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.content.Context;
import android.os.Bundle;
import android.renderscript.Allocation;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    TextView temp,humd;
    ImageView weather;
    Button button;
    String response1 = "";
    String temperature;
    String humidity;
    String rain;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        temp = findViewById(R.id.temp);
        humd = findViewById(R.id.humd);
        weather = findViewById(R.id.rain);
        button = findViewById(R.id.butt);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getRequest();
                //textView.setText(string);
            }
        });
    }

    public void getRequest() {

        StringRequest stringRequest = new StringRequest(Request.Method.GET, "http://192.168.43.35:5000/weather",

                response -> {
                    System.out.println("Fuuuuuuuuck 3 "+ response);
                    //parseItems(response);
                    jsonParser(response);

                },

                error -> System.out.println("Fuuuuuuuuck 2 "+ error))
                ;

        RequestQueue queue = Volley.newRequestQueue(this);
        queue.add(stringRequest);

        //return response1;
    }

    private void jsonParser(String response) {
        JSONObject reader;
        try {
            reader = new JSONObject(response);

            temperature = reader.getString("temperature");
            humidity = reader.getString("humidity");
            rain = reader.getString("rain");
            temp.setText(reader.getString("temperature"));
            humd.setText(reader.getString("humidity"));
            System.out.println("Fuuuuuuck "+rain);
            if (rain.equals("rain"))
                weather.setBackground(getResources().getDrawable( R.mipmap.ic_rain_round));
            else if (rain.equals("clear"))
                weather.setBackground(getResources().getDrawable(R.mipmap.ic_sun_round));
            else
                weather.setBackground(getResources().getDrawable(R.mipmap.ic_cloud_round));
        } catch (JSONException e) {
            e.printStackTrace();
        }






    }
}