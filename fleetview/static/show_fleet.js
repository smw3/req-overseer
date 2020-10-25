function handleError(data) {
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

$(document).ready(function(){
	$.getJSON('/api/fleet', function (data) {
		if (handleError(data)) {
			return;
		}
		var member_table = $('<table>').attr('class','table');
		member_table.append(
			$('<tr>').append(
				$('<th>').text('Pilot').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort'))),
				$('<th>').text('Ship').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort'))),
				$('<th>').text('Type').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort')))));
		$.each(data["members"], function (index, value) {
			console.log(index);
			var row = $('<tr>');
			row.append($('<td>').text(value["name"]));
			row.append($('<td>').text(value["ship_info"]["name"]));
			row.append($('<td>').text(value["ship_info"]["type"]));
			member_table.append(row);
		});
		console.log("Done!");
		
		$("#members").append(member_table);
		member_table.tablesort();
		
		var fleetcomp_table = $('<table>').attr('class','table');
		fleetcomp_table.append(
			$('<tr>').append(
				$('<th>').text('Type').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort'))),
				$('<th>').text('Number').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort')))));
						
		$.each(data["fleet_comp"], function (index, value) {
			console.log(index);
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			fleetcomp_table.append(row);
		});
		console.log("Done!");
		
		$("#fleetcomp").append(fleetcomp_table);	
		fleetcomp_table.tablesort();		
				
		var ships_table = $('<table>').attr('class','table');
		ships_table.append(
			$('<tr>').append(
				$('<th>').text('Name').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort'))),
				$('<th>').text('Number').append(
					$('<span>').attr("class","icon").append(
						$('<i>').attr('class','fas fa-sort')))));
		$.each(data["ships"], function (index, value) {
			console.log(index);
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table.append(row);
		});
		console.log("Done!");
		
		$("#ships").append(ships_table);
		ships_table.tablesort();
	});
});