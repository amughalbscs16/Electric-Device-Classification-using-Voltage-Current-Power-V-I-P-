<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Auth::routes();
Route::get('/', 'DevicesController@index')->name('come');
Route::get('/home', 'DevicesController@index')->name('home');
Route::get('/managedevices', 'DevicesController@managedevices')->name('managedevices');
Route::get('/stats', 'DevicesController@stats')->name('stats');
Route::get('/checkTransition', 'DevicesController@checkTransition')->name('checkTransition');
Route::get('/clearTransition', 'DevicesController@clearTransition')->name('clearTransition');
Route::get('/getDeviceTime/{name}', 'DevicesController@getDeviceTime')->name('getDeviceTime');