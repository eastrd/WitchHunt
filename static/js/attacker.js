function MakeField(id){
  return "<input type='text' id='" + id + "' />"
}

// Attempt to read all attackers from the backend
$.ajax({
  url: '/api/attacker/all',
  type: 'GET',
  success: function(response) {
      console.log("Success")
      let all_attacker_data = JSON.parse(response)
      var table = $("<table>", { "cellpadding" : "10" })

      // Adds the header row
      $(table).append("<tr><th>IP</th><th>Device</th><th>Lat</th><th>Lon</th><th>Country</th><th>City</th><th>ISP</th><th>AS</th><th>other_info</th></tr>")
      $(".attacker_list_div_class").append(table)
      var header_row = $("<tr/>")
      for (var i=0; i<all_attacker_data.length; i++){
        // Fetch relevant information
        var ip = all_attacker_data[i]["ip"]
        var device = all_attacker_data[i]["device"]
        var lat = all_attacker_data[i]["lat"]
        var lon = all_attacker_data[i]["lon"]
        var country = all_attacker_data[i]["country"]
        var city = all_attacker_data[i]["city"]
        var isp = all_attacker_data[i]["isp"]
        var as = all_attacker_data[i]["as"]
        var other_info = all_attacker_data[i]["other_info"]

        // Dynamically generate table and append inside list class
        var row = "<tr><td>" + ip + "</td><td>" + device + "</td><td>" + lat + "</td><td>" + lon + "</td><td>" + country + "</td><td>" + city + "</td><td>" + isp + "</td><td>" + as + "</td><td>" + other_info + "</td>"
        // Adds delete button
        //row += "<td><input class='attacker_btn_del_class' type='button' value=' - ' id='del_btn_id_" + ip + "' /></td></tr>"
        // Append an empty row with text fields at the end in case user wants to add new attacker
        $(table).append(row)
      }
    console.log("Fetched all attackers")
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("Failed to load all attackers");
  }
});

// Search attacker when the search button has been clicked
