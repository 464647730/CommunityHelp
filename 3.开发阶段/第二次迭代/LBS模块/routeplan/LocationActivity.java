package routeplan;

import android.app.Activity;
import android.os.Bundle;

import com.baidu.location.BDLocation;
import com.baidu.location.BDLocationListener;
import com.baidu.location.LocationClient;
import com.baidu.location.LocationClientOption;

public class LocationActivity extends Activity {

	
	
	public double mLat1=1.1;
	public double mLon1;

	LocationClient mLocClient;
	public MyLocationListenner myListener;
	boolean isFirstLoc = true;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		myListener = new MyLocationListenner();
		mLocClient = new LocationClient(this);
		mLocClient.registerLocationListener(myListener);
		LocationClientOption option = new LocationClientOption();
		option.setOpenGps(true);
		option.setCoorType("bd09ll"); 
		option.setScanSpan(1000);
		mLocClient.setLocOption(option);
		mLocClient.start();

	}
	/**
	 * 定位SDK监听函数
	 */
	public class MyLocationListenner implements BDLocationListener {

		@Override
		public void onReceiveLocation(BDLocation location) {
			
			  mLat1=location.getLatitude();
			  mLon1=location.getLongitude();
		}

		public void onReceivePoi(BDLocation poiLocation) {
		}
	}
	
	public double GetLatitude(){
		return mLat1;
	}
	
	public double Getlongtitude(){
		return mLon1;
	}
	
}
