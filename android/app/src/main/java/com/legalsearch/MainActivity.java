package com.legalsearch;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {

    private JSONArray articles;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        loadLaw();

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
        result.setPadding(0, 32, 0, 16);
        result.setTextIsSelectable(true);

        searchButton.setOnClickListener(v -> {

            String keyword =
                    searchBox.getText().toString().trim();

            if (keyword.isEmpty()) {
                result.setText("请输入关键词");
                return;
            }

            StringBuilder output =
                    new StringBuilder();

            int count = 0;

            try {

                for (int i = 0; i < articles.length(); i++) {

                    JSONObject article =
                            articles.getJSONObject(i);

                    String text =
                            article.getString("text");

                    if (text.contains(keyword)) {

                        output.append(article.getString("displayNumber"))
                                .append("\n")
                                .append(text)
                                .append("\n\n");

                        count++;
                    }
                }

                if (count == 0) {
                    output.append("没有找到相关条文");
                }

            } catch (Exception e) {

                output.append("搜索出错：")
                        .append(e.getMessage());

            }

            result.setText(output.toString());

        });

        layout.addView(title);
        layout.addView(searchBox);
        layout.addView(searchButton);
        layout.addView(result);

        setContentView(layout);
    }

    private void loadLaw() {

        try {

            InputStream input =
                    getAssets().open("criminal-law.json");

            byte[] data =
                    new byte[input.available()];

            input.read(data);
            input.close();

            String json =
                    new String(
                            data,
                            StandardCharsets.UTF_8
                    );

            JSONObject law =
                    new JSONObject(json);

            articles =
                    law.getJSONArray("articles");

        } catch (Exception e) {

            articles =
                    new JSONArray();

        }
    }
}
