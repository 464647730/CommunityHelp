package client.ui;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.res.Resources.NotFoundException;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import communicate.PushSender;


public class SendHelpMsgActivity extends Activity{

	private static final String[] sen={"�������", "�Ż���","��С͵��","������","��ǿ����","���Ӷ���"};
	private EditText edt;
	private Spinner spinner;
	private Button sendmessage;
	private ArrayAdapter<String> adapter;
    private Send send;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		requestWindowFeature(Window.FEATURE_NO_TITLE);
		setContentView(R.layout.sendhelpmsg_activity);
		
		edt = (EditText) findViewById(R.id.send_msg);
		spinner = (Spinner) findViewById(R.id.common_sentence);
		sendmessage=(Button)findViewById(R.id.sendmessage);
		adapter = new ArrayAdapter<String>(this,android.R.layout.simple_spinner_item, sen);

		//���������б�ķ��
	    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

	    //��adapter ��ӵ�spinner��
	    spinner.setAdapter(adapter);
	    
	    //����¼�Spinner�¼����� 
	    spinner.setOnItemSelectedListener(new SpinnerSelectedListener());
	    
	    sendmessage.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				// TODO Auto-generated method stub
			    //send=new Send();
			    //send.execute();
				
			}
		});
	}
	
	//ʹ��������ʽ����

	class SpinnerSelectedListener implements OnItemSelectedListener{

	    public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
	    	
	    	if (arg2 != 0)
	    		edt.setText(edt.getText().toString() + sen[arg2] + "...");
	    	
	    }

	    public void onNothingSelected(AdapterView<?> arg0) {

	    }
	}
	
	private class Send extends AsyncTask<Void, Void, String> {

        @Override
        protected String doInBackground(Void... params) { 
        	Map<String,Object> a=new HashMap<String, Object>();
			a.put("audio", new File("/����/audio.amr"));
			a.put("video", new File("/����/video.3gp"));
			
            return PushSender.sendMessage("login", a);
        }
        @Override
        protected void onPreExecute() {   
        	
        }
        @Override
        protected void onPostExecute(String result) {   	
        	
            super.onPostExecute(result);
        }
    }

}
