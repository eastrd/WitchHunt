// Attempt to read all pots from the backend
$.ajax({
  url: '/api/pot/all',
  type: 'GET',
  success: function(response) {
      console.log("Success")
      let all_pot_data = JSON.parse(response)
      var table = $("<table>", { "cellpadding" : "10" })

      // Adds the header row
      $(table).append("<tr><th>Name</th><th>Url Suffix</th><th>Suffix Query</th><th>Notification Email</th><th>Template</th><th>Payload Name</th><th>Delete</th></tr>")//<th>Valid Until</th></tr>")
      $(".pot_list_div_class").append(table)
      var header_row = $("<tr/>")
      for (var i=0; i<all_pot_data.length; i++){
        // Fetch relevant information
        var name = all_pot_data[i]["project_name"]
        var url_suffix = all_pot_data[i]["url_suffix"]
        var suffix_query = all_pot_data[i]["suffix_query"]
        var notif_method = all_pot_data[i]["notif_method"]
        var template = all_pot_data[i]["template"]
        var js_code_name = all_pot_data[i]["js_code_name"]

        // Dynamically generate table and append inside pot_list_div_class
        var row = "<tr><td>" + name + "</td><td>" + url_suffix + "</td><td>" + suffix_query + "</td><td>" + notif_method + "</td><td>" + template + "</td><td>" + js_code_name + "</td>"
        // Adds delete button
        row += "<td><input class='pot_btn_del_class' type='button' value=' - ' id='del_btn_id_" + suffix_query + "' /></td></tr>"
        $(table).append(row)
      }
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("Failed to load all pots");
  }
});

// Delete pot and refresh the list
$(document).on("click", ".pot_btn_del_class", function(){
  // Get pot url suffix and delete it
  var suffix_query = $(this).attr("id").replace("del_btn_id_", "")
  let data = {
    suffix_query : suffix_query
  }
  // Send ajax to backend
  $.ajax({
    url: '/api/pot/del',
    type: 'POST',
    data: data,
    success: function(response) {
        // Refresh the page
        location.reload()
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log("Failed to load all pots");
    }
  });
})


// Search pots when the search button has been clicked


// Add new pot and refresh the list
