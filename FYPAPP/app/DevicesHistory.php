<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class DevicesHistory extends Model
{
    protected $table = "devices_history";
    protected $fillable = [
        'status',
    ];
}
