package communicate;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.app.Notification;
import android.app.Notification.Builder;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.graphics.BitmapFactory;
import client.ui.R;

import com.igexin.sdk.PushManager;

public class PushConfig {
	public static final String SERVICEURL = "http://114.215.133.61:8080/api/"; // 服务器地址
	public static final int CONNECTION_TIMEOUT_INT = 8000; // 默认连接服务器超时时间
	public static final int READ_TIMEOUT_INT = 5000; // 默认读取服务器数据超时时间
	
	// 用户名，未登录时指定为空字符串
	public static String username = "";
	
	public static final int NOTIFICATION_EVENT = 0; // 事件系列通知
	public static final int NOTIFICATION_FRIEND = 1; // 好友系列通知
	public static final int NOTIFICATION_END_EVENT = 2; // 结束事件通知
	
	public static List<String> endevents = new ArrayList<String>();
	
	public static int helpmessage = 0; // 未读求助信息的条数，用于在通知栏显示
	public static int aidmessage = 0; // 未读援助信息的条数，用于在通知栏显示
	public static boolean notifyevent = true; // 收到求助或援助信息后是否在通知栏显示
	public static int eventid = -1; // 当前事件详情页的事件id，不在该页面则为-1
	public static int toevent = -1; // 要跳转的event的id
	
	// 以下变量自动维护
	public static Context applicationContext = null;
	public static String clientId = "";
	
	/**
	 * 初始化推送服务
	 * @param mContext
	 */
	public static void init(Activity mContext) {
		PushConfig.applicationContext = mContext.getApplicationContext();
        PushManager.getInstance().initialize(mContext.getApplicationContext());
	}
	
	/**
	 * 停止推送服务
	 * @param mContext
	 */
	public static void stop(Activity mContext) {
		PushManager.getInstance().stopService(mContext.getApplicationContext());
	}
	
	/**
	 * 显示通知
	 * @param context
	 * @param tickerText
	 * @param title
	 * @param content
	 * @param intent
	 */
	public static void sendNotification(Context context, String tickerText, String title, String content, Intent intent, int NOTIFY_ID) {
		NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
		
		Builder builder = new Notification.Builder(context);
		PendingIntent contentIntent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
		builder.setContentIntent(contentIntent);
		builder.setSmallIcon(R.drawable.notification_small)
		.setLargeIcon(BitmapFactory.decodeResource(context.getResources(), R.drawable.notification))
		.setTicker(tickerText)
		.setContentTitle(title)
		.setContentText(content)
		.setWhen(System.currentTimeMillis())
		.setAutoCancel(true);
		
		Notification notice = builder.getNotification();
		notice.defaults |= Notification.DEFAULT_SOUND;
		nm.notify(NOTIFY_ID, notice);
	}
	
	/**
	 * 清除通知
	 * @param context
	 */
	public static void clearNotification(Context context, int NOTIFY_ID) {
		NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
		nm.cancel(NOTIFY_ID);
	}
}