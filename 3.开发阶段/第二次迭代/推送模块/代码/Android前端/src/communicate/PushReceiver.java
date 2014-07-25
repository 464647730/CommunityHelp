package communicate;

import org.json.JSONException;
import org.json.JSONObject;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import com.igexin.sdk.PushConsts;
import com.igexin.sdk.PushManager;

public class PushReceiver extends BroadcastReceiver {
	
	@Override
	public void onReceive(Context context, Intent intent) {
		Bundle bundle = intent.getExtras();
		Log.d("GetuiSdk", "onReceive() action=" + bundle.getInt("action"));
		switch (bundle.getInt(PushConsts.CMD_ACTION)) {
		
		case PushConsts.GET_MSG_DATA:
			// ��ȡ͸������
			// String appid = bundle.getString("appid");
			byte[] payload = bundle.getByteArray("payload");
			
			String taskid = bundle.getString("taskid");
			String messageid = bundle.getString("messageid");
			
			// smartPush��������ִ���ýӿڣ�action��ΧΪ90000-90999���ɸ���ҵ�񳡾�ִ��
			boolean result = PushManager.getInstance().sendFeedbackMessage(context, taskid, messageid, 90001);
			System.out.println("��������ִ�ӿڵ���" + (result ? "�ɹ�" : "ʧ��"));
			
			if (payload != null) {
				String data = new String(payload);
				
				Log.d("GetuiSdk", "Got Payload:" + data);
				//����͸����Ϣ
				try {
					JSONObject json = new JSONObject(data);
					String type = json.getString("type");
					JSONObject message = json.getJSONObject("data");
					Intent i = new Intent();
					if (type.equals("help")) {
						// ������Ϣ
						i.setAction("helpmessage");
						i.putExtra("username", message.getString("username"));
						i.putExtra("content", message.getString("content"));
						i.putExtra("time", message.getString("time"));
						i.putExtra("kind", message.getInt("kind"));
						i.putExtra("audio", message.getInt("audio"));
						i.putExtra("video", message.getInt("video"));
						i.putExtra("eventid", message.getInt("eventid"));
						i.putExtra("userid", message.getInt("userid"));
					} else if (type.equals("aid")) {
						// Ԯ����Ϣ
						i.setAction("aidmessage");
						i.putExtra("username", message.getString("username"));
						i.putExtra("content", message.getString("content"));
						i.putExtra("time", message.getString("time"));
						i.putExtra("audio", message.getString("audio"));
						i.putExtra("video", message.getString("video"));
						i.putExtra("eventid", message.getInt("eventid"));
						i.putExtra("userid", message.getInt("userid"));
					} else if (type.equals("endhelp")) {
						// ���������¼�
						i.setAction("finishevent");
						i.putExtra("eventid", message.getInt("eventid"));
						i.putExtra("time", message.getString("time"));
					} else if (type.equals("invite")) {
						// ��Ӻ�������
						i.setAction("addfriend");
						i.putExtra("username", message.getString("username"));
						i.putExtra("info", message.getString("info"));
						i.putExtra("userid", message.getInt("userid"));
					} else if (type.equals("remove")) {
						// �Ƴ����ѣ��������������
						i.setAction("removefriend");
						i.putExtra("userid", message.getInt("userid"));
					}
					context.sendBroadcast(i);
				} catch (JSONException e) {
					e.printStackTrace();
				}
			}
			break;
		case PushConsts.GET_CLIENTID:
			//��ȡClientID(CID)
			//������Ӧ����Ҫ��CID�ϴ��������������������ҽ���ǰ�û��˺ź�CID���й������Ա��պ�ͨ���û��˺Ų���CID������Ϣ����
			PushConfig.clientId = bundle.getString("clientid");
			PushSender.sendClientId();
			break;
		default:
			break;
		}
	}
	
}