package communicate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import adapter.AssistListViewAdapter;
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.view.ViewPager;
import client.ui.R;
import fragment.MessageFragment;

public class PushImport {
	private Activity activity;
	private BroadcastReceiver receiver;
	
	public PushImport(Activity activity) {
		this.activity = activity;
	}
	
	public void controlOnCreate(final List<Fragment> controlFragments, final ViewPager mViewPager) {
		receiver = new BroadcastReceiver() {
			@Override
			public void onReceive(Context context, Intent intent) {
				Bundle bundle = intent.getExtras();
				MessageFragment f = (MessageFragment) controlFragments.get(1);
				f.addItem(bundle.getString("username"), bundle.getString("time"), bundle.getString("content"), bundle.getString("eventid"));
				if (bundle.getBoolean("locate"))
					mViewPager.setCurrentItem(1);
			}
		};
		IntentFilter filter = new IntentFilter("helpmessage");
		activity.registerReceiver(receiver, filter);
		if (activity.getIntent().getAction() != null && activity.getIntent().getAction().equals("helpmessage")) {
			mViewPager.setCurrentItem(1);
		}
	}
	
	public void controlOnResume() {
		PushConfig.helpmessage = PushConfig.aidmessage = 0;
		PushConfig.endevents.clear();
		PushConfig.clearNotification(activity, PushConfig.NOTIFICATION_EVENT);
		PushConfig.notifyevent = false;
	}
	
	public void controlOnPause() {
		PushConfig.notifyevent = true;
	}
	
	public void controlOnDestroy() {
		activity.unregisterReceiver(receiver);
	}
	
	public void detailOnCreate(final List<Map<String, Object>> datalist, final AssistListViewAdapter assistListViewAdapter) {
		receiver = new BroadcastReceiver() {

			@Override
			public void onReceive(Context context, Intent intent) {
				Bundle bundle = intent.getExtras();
				if (activity.getIntent().getExtras().getString("eid").equals(bundle.getString("eventid")))
					return;
				Map<String, Object> map = new HashMap<String, Object>();
				map.put("image",  R.drawable.img01);
				map.put("name", bundle.getString("username"));
				map.put("time", bundle.getString("time"));
				map.put("content", bundle.getString("content"));
				datalist.add(0, map);
				assistListViewAdapter.notifyDataSetChanged();
			}
		};
		IntentFilter filter = new IntentFilter("aidmessage");
		activity.registerReceiver(receiver, filter);
		
	}
	
	public void detailOnResume(Bundle bundle) {
		PushConfig.eventid = Integer.parseInt(bundle.getString("eid"));
		PushConfig.helpmessage = PushConfig.aidmessage = 0;
		PushConfig.clearNotification(activity, PushConfig.NOTIFICATION_EVENT);
	}
	
	public void detailOnPause() {
		PushConfig.eventid = -1;
	}
	
	public void detailOnDestroy() {
		activity.unregisterReceiver(receiver);
	}
	
}