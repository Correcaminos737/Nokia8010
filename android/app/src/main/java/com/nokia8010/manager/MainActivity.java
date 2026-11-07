package com.nokia8010.manager;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(Tv8010BridgePlugin.class);
        super.onCreate(savedInstanceState);
    }
}
