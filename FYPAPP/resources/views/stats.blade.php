
@extends('layouts.fyp')

@section('javascript')
<script src="https://cdn.zoomcharts-cloud.com/1/latest/zoomcharts.js"></script>
<script>
    $( document ).ready(function() {

        $('#deviceName').change(function() {

            if ($('#deviceName').val() != "None")
            {
                console.log($('#deviceName').val());
                console.log("http://localhost:8000/getDeviceTime/"+$('#deviceName').val());
                //checkboxes = $('input');
                //$.each( checkboxes, function( index, value ) {
                // checkboxes[index].checked = false;
                //});
                var t = new TimeChart(
                    {
                        container: document.getElementById("demo"),
                        data:
                        {
                            units:["m"],
                            url: "http://localhost:8000/getDeviceTime/"+$('#deviceName').val(),
                            timestampInSeconds: true
                        },
                        valueAxisDefault:{ title:$('#deviceName').val().toUpperCase()+": Time, Turn On" },
                        series:[
                            {
                                name:$('#deviceName').val().toUpperCase(),
                                id:"series1",
                                type:"columns",
                                data:{
                                    index:1
                                },
                                style:
                                {
                                    fillColor : "#8c939f",
                                    lineColor: "#727b8a",
                                    lineWidth : 1,
                                    padding: [1,1]
                                }
                            }
                        ]
                    }
                );
            }
        });
    });
</script>
@endsection

@section('header')
Device Statistics
@endsection

@section('content')
    @if (session('status'))
        <div class="alert alert-success" role="alert">
            {{ session('status') }}
        </div>
    @endif
    </div>
    <center>
    <p><select id="deviceName">
    <option value="None">-- Select a Device for Stats --</option>
    @foreach ($devices as $device)
       <option style="text-align-last: center;" value="{{$device->name}}">{{strtoupper($device->name)}}</option>
    @endforeach
    </select>
    </p>

    <content>
        <div id="demo" width="80%">
        </div>
    </content>
    </center>
@endsection

