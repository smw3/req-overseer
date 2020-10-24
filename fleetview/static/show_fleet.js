$(document).ready(function(){
	$.getJSON('/api/fleet', function (data) {
		$("#fleetcomp").text(data);
	});
});