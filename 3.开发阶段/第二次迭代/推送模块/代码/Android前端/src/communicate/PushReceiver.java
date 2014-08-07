package communicate;

import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import client.ui.ControlActivity;
import client.ui.DetailMessageActivity;
import client.ui.ValidationActivity;

import com.igexin.sdk.PushConsts;
import com.igexin.sdk.PushManager;

import fragment.MessageFragment;

public class PushReceiver extends BroadcastReceiver {
	
	@Override
	public void onReceive(Context context, Intent intent) {
		Bundle bundle = intent.getExtras();
		Log.d("GetuiSdk", "onReceive() action=" + bundle.getInt("action"));
		switch (bundle.getInt(PushConsts.CMD_ACTION)) {
		
		case PushConsts.GET_MSG_DATA:
			// 获取透传数据
			// String appid = bundle.getString("appid");
			byte[] payload = bundle.getByteArray("payload");
			
			String taskid = bundle.getString("taskid");
			String messageid = bundle.getString("messageid");
			
			// smartPush第三方回执调用接口，action范围为90000-90999，可根据业务场景执行
			boolean result = PushManager.getInstance().sendFeedbackMessage(context, taskid, messageid, 90001);
			System.out.println("第三方回执接口调用" + (result ? "成功" : "失败"));
			
			if (payload != null && PushConfig.username != "") {
				String data = new String(payload);
				
				Log.d("GetuiSdk", "Got Payload:" + data);
				//处理透传消息
				try {
					JSONObject json = new JSONObject(data);
					String type = json.getString("type");
					JSONObject message = json.getJSONObject("data");
					Log.i("PushReceiver", data);
					if (PushConfig.username == "")
						return;
					Intent i = new Intent();
					if (type.equals("help")) {
						// 求助信息
						i.setAction("helpmessage");
						i.putExtra("locate", PushConfig.notifyevent);
						i.putExtra("username", message.getString("username"));
						i.putExtra("content", message.getString("content"));
						i.putExtra("time", message.getString("time"));
						i.putExtra("kind", message.getString("kind"));
						i.putExtra("audio", message.getString("audio"));
						i.putExtra("video", message.getString("video"));
						i.putExtra("eventid", message.getString("eventid"));
						
						
						Intent in = new Intent();
						in.setAction("helpmessage");
						if (PushConfig.helpmessage == 0 && PushConfig.aidmessage == 0) {
							//进入DetailMessageActivit
							in.putExtra("needhelp", message.getString("username"));
							in.putExtra("time", message.getString("time"));
							in.putExtra("content", message.getString("content"));
							in.putExtra("eid", message.getString("eventid"));
							in.setClass(context, DetailMessageActivity.class);
							
							PushConfig.toevent = message.getInt("eventid");
						} else {
							//进入ControlActivity
							in.setClass(context, ControlActivity.class);
							
							PushConfig.toevent = -1;
						}

						in.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
						
						PushConfig.helpmessage++;
						String tickerText = "收到一条求助信息\n" + message.getString("content");
						String title;
						String content;
						if (PushConfig.helpmessage == 1 && PushConfig.aidmessage == 0) {
							title = message.getString("username") + "发来求助信息";
							content = message.getString("content");
						} else if (PushConfig.aidmessage == 0) {
							title = "收到" + PushConfig.helpmessage + "条求助信息";
							content = message.getString("content");
						} else {
							title = "收到" + (PushConfig.helpmessage + PushConfig.aidmessage) + "条新信息";
							content = "收到" + PushConfig.helpmessage + "条求助信息和" + PushConfig.aidmessage + "条援助信息";
						}
						PushConfig.sendNotification(context, tickerText, title, content, in, PushConfig.NOTIFICATION_EVENT);
						
						if (!PushConfig.notifyevent) {
							PushConfig.clearNotification(context, PushConfig.NOTIFICATION_EVENT);
							PushConfig.helpmessage = 0;
						}
						
					} else if (type.equals("aid")) {
						// 援助信息
						i.setAction("aidmessage");
						i.putExtra("username", message.getString("username"));
						i.putExtra("content", message.getString("content"));
						i.putExtra("time", message.getString("time"));
						i.putExtra("eventid", message.getString("eventid"));
						
						Intent in = new Intent();
						in.setAction("aidmessage");
						if ((PushConfig.helpmessage == 0 && PushConfig.aidmessage == 0) || PushConfig.toevent == message.getInt("eventid")) {
							//进入DetailMessageActivit
							Map<String, Object> map = MessageFragment.getEventById(message.getString("eventid"));
							if (map != null) {
								in.putExtra("needhelp", (String)map.get("name"));
								in.putExtra("time", (String)map.get("time"));
								in.putExtra("content", (String)map.get("content"));
								in.putExtra("eid", (String)map.get("eid"));
								in.setClass(context, DetailMessageActivity.class);
							} else {
								in.setClass(context, ControlActivity.class);
							}
							
							PushConfig.toevent = message.getInt("eventid");
						} else {
							//进入ControlActivity
							in.setClass(context, ControlActivity.class);
							
							PushConfig.toevent = -1;
						}

						in.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP|Intent.FLAG_ACTIVITY_NEW_TASK);
						
						PushConfig.aidmessage++;
						String tickerText = "收到一条援助信息\n" + message.getString("content");
						String title;
						String content;
						if (PushConfig.helpmessage == 0) {
							title = "收到" + PushConfig.aidmessage + "条援助信息";
							content = message.getString("content");
						} else {
							title = "收到" + (PushConfig.helpmessage + PushConfig.aidmessage) + "条新信息";
							content = "收到" + PushConfig.helpmessage + "条求助信息和" + PushConfig.aidmessage + "条援助信息";
						}
						PushConfig.sendNotification(context, tickerText, title, content, in, PushConfig.NOTIFICATION_EVENT);
						if (!PushConfig.notifyevent || PushConfig.eventid == message.getInt("eventid")) {
							PushConfig.clearNotification(context, PushConfig.NOTIFICATION_EVENT);
							PushConfig.aidmessage = 0;
						}
					} else if (type.equals("endhelp")) {
						// 结束求助事件
						i.setAction("finishevent");
						i.putExtra("eventid", message.getString("eventid"));
						i.putExtra("username", message.getString("username"));
						i.putExtra("time", message.getString("time"));
						
						Intent in = new Intent();
						in.setAction("endhelp");
						PushConfig.endevents.add(message.getString("username"));
						String tickerText = message.getString("username") + "发送的求助事件已结束\n事件结束于" + message.getString("time");
						String title = "您参与的" + PushConfig.endevents.size() + "个事件已结束";
						String content = PushConfig.endevents.get(0);
						for (int n = 1; n < PushConfig.endevents.size(); n++) {
							content += "、" + PushConfig.endevents.get(n);
						}
						content += "发送的求助事件已结束";
						PushConfig.sendNotification(context, tickerText, title, content, in, PushConfig.NOTIFICATION_END_EVENT);
						if (!PushConfig.notifyevent) {
							PushConfig.clearNotification(context, PushConfig.NOTIFICATION_END_EVENT);
							PushConfig.endevents.clear();
						}
					} else if (type.equals("invite")) {
						// 添加好友请求
						Intent in = new Intent(context, ValidationActivity.class);
						Bundle bun = new Bundle();
						bun.putString("username", message.getString("username"));
						bun.putString("info", message.getString("info"));
						in.putExtras(bun);
						
						PushConfig.sendNotification(context, "收到一条好友请求", 
								"收到1条好友请求", message.getString("info"), in, PushConfig.NOTIFICATION_FRIEND);
						
						i.setAction("addfriend");
						i.putExtra("username", message.getString("username"));
						i.putExtra("info", message.getString("info"));
						i.putExtra("type", message.getString("type"));

					} else if (type.equals("agree")) {
						//通过好友验证
						i.setAction("becomefriends");
						i.putExtra("username", message.getString("username"));
						i.putExtra("type", message.getString("type"));
						i.putExtra("agree", message.getString("agree"));
					} else if (type.equals("remove")) {
						// 移除好友
						i.setAction("removefriend");
						i.putExtra("username", message.getString("username"));
					}
					context.sendBroadcast(i);
				} catch (JSONException e) {
					e.printStackTrace();
				}
			}
			break;
		case PushConsts.GET_CLIENTID:
			//获取ClientID(CID)
			//第三方应用需要将CID上传到第三方服务器，并且将当前用户账号和CID进行关联，以便日后通过用户账号查找CID进行消息推送
			PushConfig.clientId = bundle.getString("clientid");
			Log.i("PushReceiver", "cid=" + PushConfig.clientId);
			PushSender.sendClientId();
			break;
		default:
			break;
		}
	}
	
}