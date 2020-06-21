<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Devices;
use App\DevicesHistory;
use Illuminate\Support\Facades\DB;
class DevicesController extends Controller
{
    public function index()
    {
        $devices = Devices::all();
        //dd($devices);
        return view('index', ['devices' => $devices]);;
        //console.log($devices);
    }
    public function managedevices()
    {
    	$devices = Devices::all();
        //dd($devices);
        return view('managedevices',['devices' => $devices]);;
    }
    public function stats()
    {
        $devices = Devices::all();
        return view('stats',['devices' => $devices, 'name' => "lighting"]);;
    }
    public function checkTransition()
    {
        $device = Devices::select('name')->where('latest_change','=','1')->get()->first();
        #dd($device);
        if ($device){
        $devicename = $device->name;
        $devicedetected = DevicesHistory::where('name','=',$devicename)->get()->first();
        $time =  $devicedetected->created_at;
        str_replace("world","Peter","Hello world!");
        if ($devicedetected)
        {
            $devices = str_replace("[","",$devicedetected->detected_devices);
            $devices = str_replace("]","",$devices);
            $devices = (explode(",",$devices));
            #array_unshift($devices, $time);
            return $devices;
        }
        else
            return 0;
        }
        else
            return 0;
    }
    public function clearTransition()
    {
        $device = Devices::where('latest_change','>', 0)->first();
        $device->latest_change -= 1;
        $device->save();
        return 1;
    }
    public function getDeviceTime(Request $requests, $name)
    {
        $devices = DB::table('devices_history')
                     ->select(DB::raw('UNIX_TIMESTAMP(created_at) as time'))
                     ->where('name', '=', $name)
                     ->get()->all();
        $fStr = '{';
        $fStr = $fStr."\"unit\": \"m\",";
        $fStr = $fStr."\"values\": [";
        for($i=0;$i<count($devices);$i++)
        {
            $fStr = $fStr."[".$devices[$i]->time.",0.5]";
            if ($i != count($devices ) - 1)
                $fStr = $fStr.",";
        }   
        $fStr = $fStr."]";
         $fStr = $fStr."}";
        return $fStr;
    }
}
