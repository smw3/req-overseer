var sharing = false;

function handleError(data) {
	$("#errors").empty();
	if (data.hasOwnProperty("error")) {
		$("#errors").append(
			$("<div>").attr("class", "container").append(
				$("<div>").attr("class", "notification is-primary").text(data["error"])
			)
		);
		return true;
	}
	return false;
}

function updateFleetView() {
	$.getJSON('/api/shared_fleet/' + share_id, function (data) {
		if (handleError(data)) {
			$("#loading_indicator").hide();
			$("#members_body").empty();
			$("#fleetcomp_body").empty();
			$("#ships_body").empty();
			return;
		}
		
		var time = data["last_refresh"];
		$("#last_refresh_time").html("<strong>Last updated: " + time + "</strong>");
		
		var member_table_body = $('#members_body');
		member_table_body.empty();
		$.each(data["members"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(value["name"]));
			row.append($('<td>').text(value["ship_info"]["name"]));
			row.append($('<td>').text(value["ship_info"]["type"]));
			row.append($('<td>').text(value["solar_system_name"]));
			member_table_body.append(row);
		});
		$('#members_table').tablesort();
		console.log("members_table!");	
		
		var fleetcomp_table_body = $('#fleetcomp_body');
		fleetcomp_table_body.empty();					
		$.each(data["fleet_comp"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			fleetcomp_table_body.append(row);
		});
		$('#fleetcomp_table').tablesort();	
		console.log("fleetcomp_table!");		
				
		var ships_table_body = $('#ships_body');	
		ships_table_body.empty();		
		$.each(data["ships"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table_body.append(row);
		});
		$('#ships_table').tablesort();
		console.log("ships_table!");
		
		$("#errors").empty();
		$("#loading_indicator").remove();
		console.log("Done!");
	}).fail(function(jqXHR, textStatus, errorThrown) { 
		$("#loading_indicator").show();
		
		$("#errors").append(
			$("<div>").attr("class", "container").append(
				$("<div>").attr("class", "notification is-primary").text(textStatus)
			)
		);
	});
}

$(document).ready(function(){
	updateFleetView();
	var myVar = setInterval(updateFleetView, 1000 * 60);
});