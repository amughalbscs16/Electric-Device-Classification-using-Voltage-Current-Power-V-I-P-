
@extends('layouts.fyp')
@section('javascript')
<script>
$( document ).ready(function() {
	function checkbox(){
	$(':checkbox').change(function() {
    if (this.checked == true)
    {
      console.log("http://localhost:5000/userSelection/"+this.id);
      $.get("http://localhost:5000/userSelection/"+this.id, function(data){
        console.log(data);
      });
      $('#modal').modal('hide');
    }
	}); 
	}
	var url = "http://localhost:8000"+"/checkTransition";
	var url2 = "http://localhost:8000"+"/clearTransition";
	console.log( url );
	function openModal(deviceName)
	{
		//For loop to display each device and a checkbox when checked, update it in the database.
		if (deviceName.length == 1){
			$('.modal-body').html(deviceName[0].toUpperCase()+" Transition.");
			$('#openmodal').click();
		}
		else{
			body = "<table width=\"90%\">";

			$( deviceName ).each(function( index ) {
			  body += "<tr><td>" + deviceName[index].toUpperCase() + "</td> <td><label class=\"switch\"> <input type=\"checkbox\" id="+deviceName[index]+
			  "><span class=\"slider round\"></span></label></td></tr>";
			});
			body += "</table>";
			$('.modal-body').html(body);
			$('#openmodal').click();
			checkbox();
		}
	}
	function clearUpdate(url)
	{
		$.get( url , function(data){
	    	console.log("Notification Cleared from Database");
      	});
	}

	function getUpdate(url)
	{	setTimeout(function() {

	    $.get( url , function(data){
	        if (data != '0')
	        {
	        	//alert(data);
	        	openModal(data);
	        	clearUpdate(url2);
	        }
	        getUpdate(url);
      	});
      	  //your code to be executed after 3 second
		}, 3000);
	}
	getUpdate(url);
});
</script>
@endsection
@section('header')
Event Updates
@endsection
@section('content')
    @if (session('status'))
        <div class="alert alert-success" role="alert">
            {{ session('status') }}
        </div>
    @endif
    </div>
    This page provides, notifications of devices.
    <button id="openmodal" type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal" style="visibility:hidden;">Open Modal</button>

	<!-- Modal -->
	<div id="myModal" class="modal fade" role="dialog">
	  <div class="modal-dialog">

	    <!-- Modal content-->
	    <div class="modal-content">
	      <div class="modal-header">
	        
	        <h4 class="modal-title" align="center">Device Transition</h4>
	        <button type="button" class="close" data-dismiss="modal">&times;</button>
	      </div>
	      <div class="modal-body">

	      </div>
	      <div class="modal-footer">
	        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
	      </div>
	    </div>

	  </div>
</div>
@endsection

