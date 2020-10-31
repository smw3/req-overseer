var sharing = false;

function updateFleetView() {	
	$.getJSON('/api/fleet/snapshot/' + char_id + '/' + snapshot_id, function (data) {
		if (handleError(data)) {
			$("#loading_indicator").hide();
			$("#members_body").empty();
			$("#fleetcomp_body").empty();
			$("#ships_body").empty();
			return;
		}
		
		var time = data["last_refresh"];
		timeSinceLastUpdate = new Date(time).getTime();
		updateTimeSinceUpdate();
				
		var member_table_body = $('#members_body');
		member_table_body.empty();
		$.each(data["members"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').attr("data-sort-value", value["alliance"]).append(
				$('<figure>').addClass("image").addClass("is-32x32").append(
					$('<img>').attr('src','https://images.evetech.net/alliances/' + value["alliance_id"] + '/logo?size=32').attr("title", value["alliance"])
				)
			));
			row.append($('<td>').attr("data-sort-value", value["corp"]).append(
				$('<figure>').addClass("image").addClass("is-32x32").append(
					$('<img>').attr('src','https://images.evetech.net/corporations/' + value["corp_id"] + '/logo?size=32').attr("title", value["corp"])
				)
			));
			row.append($('<td>').text(value["name"]));
			row.append($('<td>').text(value["ship_info"]["name"]));
			row.append($('<td>').text(value["ship_info"]["type"]));
			row.append($('<td>').text(value["solar_system_name"]));
			member_table_body.append(row);
		});
		$('#members_table').tablesort();
		
		var fleetcomp_table_body = $('#fleetcomp_body');
		fleetcomp_table_body.empty();					
		$.each(data["fleet_comp"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			fleetcomp_table_body.append(row);
		});
		$('#fleetcomp_table').tablesort();		
				
		var ships_table_body = $('#ships_body');	
		ships_table_body.empty();		
		$.each(data["ships"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table_body.append(row);
		});
		$('#ships_table').tablesort();
				
		var alliance_table_body = $('#alliance_body');	
		alliance_table_body.empty();		
		$.each(data["alliances"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table_body.append(row);
		});
		$('#alliance_table').tablesort();
		
		var corporation_table_body = $('#corporation_body');	
		corporation_table_body.empty();		
		$.each(data["corporations"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table_body.append(row);
		});
		$('#corporation_table').tablesort();
		
		$("#errors").empty();
		$("#loading_indicator").hide();
	}).fail(function(jqXHR, textStatus, errorThrown) { 
		$("#loading_indicator").show();
		$("#errors").empty();
		
		$("#errors").append(
			$("<div>").attr("class", "container").append(
				$("<div>").attr("class", "notification is-primary").text(textStatus + ":" + errorThrown)
			)
		);
	});
}


$(document).ready(function(){
	updateFleetView();
	
	setInterval(updateTimeSinceUpdate, 1000);
});