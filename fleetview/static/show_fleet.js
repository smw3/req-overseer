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

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable2");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
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
				
		var ships_table = $('<table>').attr('class','table');
		fleetcomp_table.append(
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
	});
});