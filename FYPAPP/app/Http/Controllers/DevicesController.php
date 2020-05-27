<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Devices;
use App\DevicesHistory;
class DevicesController extends Controller
{
    public function index()
    {
        #return view('home');
        return view('index');
    }
}
