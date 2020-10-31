var sharing = false;
var timeSinceLastUpdate = undefined;

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

function formatDate(d) {
	const year = d.getFullYear() // 2019
	const date = d.getDate() // 23
	
	const months = [
	  'January',
	  'February',
	  'March',
	  'April',
	  'May',
	  'June',
	  'July',
	  'August',
	  'September',
	  'October',
	  'November',
	  'December'
	]
	
	const monthName = months[d.getMonth()]
	
	const days = [
	  'Sun',
	  'Mon',
	  'Tue',
	  'Wed',
	  'Thu',
	  'Fri',
	  'Sat'
	]
	
	const dayName = days[d.getDay()] // Thu
	
	const formatted = `${dayName}, ${date} ${monthName} ${year} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}`
	
	return formatted
}	

function updateTimeSinceUpdate() {
	if (timeSinceLastUpdate === undefined)
		return;
	
	var now = new Date().getTime();
	var distance = timeSinceLastUpdate - now;
	
	var timeSinceText = "";
	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	if (days > 0)
		timeSinceText = timeSinceText + days + " days";
	
	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	if (hours > 0)
		timeSinceText = timeSinceText + days + " hours";
	
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	if (minutes > 0)
		timeSinceText = timeSinceText + days + " minutes";
	
	var seconds = Math.floor((distance % (1000 * 60)) / 1000);
	timeSinceText = timeSinceText + days + " seconds";
	
	timeSinceText = timeSinceText + " ago";
	
	$("#last_refresh_time").html("<strong>Last updated: " + formatDate(new Date(timeSinceLastUpdate)) + " (" + timeSinceText + ")</strong>")
}

function updateFleetView() {
	$.getJSON('/api/fleet?sharing=' + sharing + '&participants=' + encodeURIComponent($( "#share_participants" ).val()), function (data) {
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
			alliance_table_body.append(row);
		});
		$('#alliance_table').tablesort();
		
		var corporation_table_body = $('#corporation_body');	
		corporation_table_body.empty();		
		$.each(data["corporations"], function (index, value) {
			var row = $('<tr>');
			row.append($('<td>').text(index));
			row.append($('<td>').text(value));
			corporation_table_body.append(row);
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
		$( "#share_link" ).html(" Sharing at <a href=\"/show_shared/" + authedCharId + "\">LINK</a>");
		updateFleetView();
	}
}

function createSnapshot() {
	$( "#snapshot_button" ).addClass("is-loading");
	
	$.getJSON('/api/fleet/take_snapshot', function (data) {
		if (handleError(data)) {
			$( "#share_button" ).removeClass("is-loading");
			return;
		}
		$( "#snapshot_link" ).append(
			$("<a>").attr("href", "/show_snapshot/" + data["char_id"] + "/" + data["snapshot_id"]).text("LINK")
		);
		$( "#snapshot_button" ).remove();		
	}).fail(function() { 
		$( "#snapshot_button" ).removeClass("is-loading");
	});
}

$(document).ready(function(){
	$( "#share_button" ).click(function() {
		toggleSharing();
	});
	$( "#snapshot_button" ).click(function() {
		createSnapshot();
	});
	
	updateFleetView();
	setInterval(updateFleetView, 1000 * 60);
	setInterval(updateTimeSinceUpdate, 1000);
	
});