
@extends('layouts.fyp')
@section('javascript')
<script>
$( document ).ready(function() {
$(':checkbox').change(function() {
    if (this.checked == true)
    {
       console.log("http://localhost:5000/classifyDevice/"+this.id);
      $.get("http://localhost:5000/classifyDevice/"+this.id, function(data){
        console.log(data);
      });
    }
}); 
});
</script>
@endsection
@section('header')
Manage Devices
@endsection
@section('content')
    @if (session('status'))
        <div class="alert alert-success" role="alert">
            {{ session('status') }}
        </div>
    @endif
    </div>
        <table style="width:60%;">
            <tr>
                <td align="center">
                    Device Name
                </td>
                <td align="center">
                    State
                </td>
            </tr>
	@foreach ($devices as $device)
    <tr>
        <td align="center">
	       {{strtoupper($device->name)}}
       </td>
       <td align="center">
        <!-- Default checked -->
        <label class="switch">
          <input type="checkbox" id="{{$device->name}}">
          <span class="slider round"></span>
        </label>
       </td>
    </tr>
	@endforeach
	</table>
@endsection

