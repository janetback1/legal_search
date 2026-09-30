package com.legalsearch;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(32, 32, 32, 32);

        TextView title = new TextView(this);
        title.setText("LegalSearch");
        title.setTextSize(28);
        title.setGravity(Gravity.CENTER);
        title.setPadding(0, 0, 0, 32);

        EditText searchBox = new EditText(this);
        searchBox.setHint("搜索法律条文");
        searchBox.setSingleLine(true);

        Button searchButton = new Button(this);
        searchButton.setText("搜索");

        TextView result = new TextView(this);
        result.setText("请输入关键词");
        result.setTextSize(18);
        result.setTextColor(Color.DKGRAY);
        result.setPadding(0, 32, 0, 0);

        searchButton.setOnClickListener(v -> {
            String keyword = searchBox.getText().toString().trim();

            if (keyword.isEmpty()) {
                result.setText("请输入关键词");
            } else {
                result.setText("正在搜索： " + keyword);
            }
        });

        layout.addView(title);
        layout.addView(searchBox);
        layout.addView(searchButton);
        layout.addView(result);

        setContentView(layout);
    }
}
