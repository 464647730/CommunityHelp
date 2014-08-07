package routeplan;

import android.content.Context;
import android.util.Log;

import com.baidu.location.BDLocation;
import com.baidu.location.BDLocationListener;
import com.baidu.location.LocationClient;
import com.baidu.location.LocationClientOption;

public class Location {

	
	
	public double mLat1=1.1;
	public double mLon1;

	LocationClient mLocClient;
	public MyLocationListenner myListener;
	boolean isFirstLoc = true;
	public Location(Context context) {

		myListener = new MyLocationListenner();
		mLocClient = new LocationClient(context);
		mLocClient.registerLocationListener(myListener);
		LocationClientOption option = new LocationClientOption();
		option.setOpenGps(true);
		option.setCoorType("bd09ll"); 
		option.setScanSpan(1000);
		Log.i("test","1111");
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
	
	public void Close(){
		mLocClient.stop();
	}
	
}
