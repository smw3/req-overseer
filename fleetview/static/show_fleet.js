$(document).ready(function(){
	$.getJSON('/api/fleet', function (data) {
		console.log(data);
		var member_table = $('<table>').attr('class','table');
		member_table.append(
			$('<tr>').append(
				$('<th>').text('Pilot'),
				$('<th>').text('Ship'),
				$('<th>').text('Type')));
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
		
		var fleetcomp_table = $('<table>').attr('class','table');
		fleetcomp_table.append(
			$('<tr>').append(
				$('<th>').text('Type'),
				$('<th>').text('Number')));
		$.each(data["fleet_comp"], function (index, value) {
			console.log(index);
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			fleetcomp_table.append(row);
		});
		console.log("Done!");
		
		$("#fleetcomp").append(fleetcomp_table);		
				
		var ships_table = $('<table>').attr('class','table');
		ships_table.append(
			$('<tr>').append(
				$('<th>').text('Name'),
				$('<th>').text('Number')));
		$.each(data["ships"], function (index, value) {
			console.log(index);
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			ships_table.append(row);
		});
		console.log("Done!");
		
		$("#ships").append(ships_table);
	});
});