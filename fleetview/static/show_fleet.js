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
	$.getJSON('/api/fleet?sharing=' + sharing + '&participants=' + encodeURIComponent($( "#share_participants" ).val()), function (data) {
		if (handleError(data)) {
			$("#loading_indicator").remove();
			$("#members").empty();
			$("#fleetcomp").empty();
			$("#ships").empty();
			return;
		}
		
		var time = data["last_refresh"];
		$("#last_refresh_time").html("<strong>Last updated: " + time + "</strong>")
				
		var member_table_body = $('#members');
		member_table_body.empty();
		$.each(data["members"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(value["name"]));
			row.append($('<td>').text(value["ship_info"]["name"]));
			row.append($('<td>').text(value["ship_info"]["type"]));
			row.append($('<td>').text(value["solar_system_name"]));
			member_table_body.append(row);
		});
		
		var fleetcomp_table = $('<table>').attr('class','table');
		var fleetcomp_table_body = $('<tbody>');
		fleetcomp_table.append(
			$('<thead>').append(
				$('<tr>').append(
					$('<th>').text('Type').append(
						$('<span>').attr("class","icon").append(
							$('<i>').attr('class','fas fa-sort'))),
					$('<th>').text('Number').append(
						$('<span>').attr("class","icon").append(
							$('<i>').attr('class','fas fa-sort'))))));
						
		$.each(data["fleet_comp"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			fleetcomp_table_body.append(row);
		});
		fleetcomp_table.append(fleetcomp_table_body);

		fleetcomp_table.tablesort();		
				
		var ships_table = $('<table>').attr('class','table');
		var ships_table_body = $('<tbody>');
		ships_table.append(
			$('<thead>').append(
				$('<tr>').append(
					$('<th>').text('Name').append(
						$('<span>').attr("class","icon").append(
							$('<i>').attr('class','fas fa-sort'))),
					$('<th>').text('Number').append(
						$('<span>').attr("class","icon").append(
							$('<i>').attr('class','fas fa-sort'))))));
							
		$.each(data["ships"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table_body.append(row);
		});
		ships_table.append(ships_table_body);
		ships_table.tablesort();
		
		$("#loading_indicator").remove();
		
		$("#fleetcomp").empty();
		$("#fleetcomp").append(fleetcomp_table);
		$("#ships").empty();
		$("#ships").append(ships_table);
	});
}

function toggleSharing() {
	if (sharing) {
		sharing = false;
		$( "#share_button" ).text("Start Sharing").removeClass("is-danger");
		$( "#share_participants" ).prop( "disabled", false );
		$( "#share_link" ).html("");
	} else {
		sharing = true;
		$( "#share_button" ).text(" Stop Sharing").addClass("is-danger");
		$( "#share_participants" ).prop( "disabled", true );
		$( "#share_link" ).html("Sharing at <a href=\"/show_shared/" + authedCharId + "\">LINK</a>");
		updateFleetView();
	}
}

$(document).ready(function(){
	$( "#share_button" ).click(function() {
		toggleSharing();
	});
	
	updateFleetView();
	var myVar = setInterval(updateFleetView, 1000 * 60);
	
	
});