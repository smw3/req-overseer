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
	var distance =  now - timeSinceLastUpdate;
	
	var timeSinceText = "";
	var days = Math.floor(distance / (1000 * 60 * 60 * 24));
	if (days > 0)
		timeSinceText = timeSinceText + days + " days ";
	
	var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
	if (hours > 0)
		timeSinceText = timeSinceText + days + " hours ";
	
	var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	if (minutes > 0)
		timeSinceText = timeSinceText + days + " minutes ";
	
	var seconds = Math.floor((distance % (1000 * 60)) / 1000);
	if (distance < 1000*60*10) 
		timeSinceText = timeSinceText + seconds + " seconds ";
	
	timeSinceText = timeSinceText + "ago";
	
	$("#last_refresh_time").html("<strong>Last updated: " + formatDate(new Date(timeSinceLastUpdate)) + " (" + timeSinceText + ")</strong>")
}
