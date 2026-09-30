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

    private JSONObject index;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        loadIndex();

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

            try {

                JSONArray ids =
                        index.getJSONArray(keyword);


                for (int i = 0; i < ids.length(); i++) {

                    int id = ids.getInt(i);

                    JSONObject law =
                            loadArticle(id);


                    output.append("第")
                            .append(law.getInt("article_number"))
                            .append("条\n")
                            .append(law.getString("text"))
                            .append("\n\n");
                }


                if (output.length() == 0) {
                    output.append("没有找到相关条文");
                }


            } catch (Exception e) {

                output.append("没有找到相关条文");

            }


            result.setText(output.toString());

        });


        layout.addView(title);
        layout.addView(searchBox);
        layout.addView(searchButton);
        layout.addView(result);

        setContentView(layout);

    }


    private void loadIndex() {

        try {

            InputStream input =
                    getAssets().open("index.json");


            byte[] data =
                    new byte[input.available()];


            input.read(data);
            input.close();


            String json =
                    new String(data,
                    StandardCharsets.UTF_8);


            index =
                    new JSONObject(json);


        } catch (Exception e) {

            index =
                    new JSONObject();

        }

    }


    private JSONObject loadArticle(int id)
            throws Exception {


        InputStream input =
                getAssets()
                .open("laws/" + id + ".json");


        byte[] data =
                new byte[input.available()];


        input.read(data);
        input.close();


        String json =
                new String(data,
                StandardCharsets.UTF_8);


        return new JSONObject(json);

    }

}
