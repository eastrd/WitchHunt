function Make_field(id){
  return "<input type='text' id='" + id + "' />"
}

function Get_datetime_from_timestamp(unixTimeStamp) {
   var date = new Date(unixTimeStamp*1000);
   var year = date.getFullYear()
   var month = ('0' + (date.getMonth() + 1)).slice(-2)
   var day = ('0' + date.getDate()).slice(-2)
   return  year + '-' + month + '-' + day + ' ' + ('0' + date.getHours()).slice(-2) + ':' + ('0' + date.getMinutes()).slice(-2);
 }

// Attempt to read all incidents from the backend
$.ajax({
  url: '/api/incident/all',
  type: 'GET',
  success: function(response) {
      console.log("Success")
      let all_incident_data = JSON.parse(response)
      var table = $("<table>", { "cellpadding" : "10" })

      // Adds the header row
      $(table).append("<tr><th>Time</th><th>IP</th><th>Device</th><th>Url Suffix</th></tr>")
      $(".incident_list_div_class").append(table)
      var header_row = $("<tr/>")
      for (var i=0; i<all_incident_data.length; i++){
        // Fetch relevant information
        var timestamp = all_incident_data[i]["timestamp"]
        var atker_ip = all_incident_data[i]["atker_ip"]
        var atker_device = all_incident_data[i]["atker_device"]
        var url_suffix_visited = all_incident_data[i]["url_suffix_visited"]
        // var atk_triggered = all_incident_data[i]["atk_triggered"]

        // Convert timestamp to real datetime
        var datetime = Get_datetime_from_timestamp(timestamp)
        // Dynamically generate table and append inside list class
        var row = "<tr><td>" + datetime + "</td><td>" + atker_ip + "</td><td>" + atker_device + "</td><td>" + url_suffix_visited + "</td>"
        $(table).append(row)
      }
    console.log("Fetched all incidents")
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("Failed to load all incidents");
  }
});

// Search incident when the search button has been clicked
