function MakeField(id){
  return "<input type='text' id='" + id + "' />"
}

// Attempt to read all payloads from the backend
$.ajax({
  url: '/api/payload/all',
  type: 'GET',
  success: function(response) {
      console.log("Success")
      let all_payload_data = JSON.parse(response)
      var table = $("<table>", { "cellpadding" : "10" })

      // Adds the header row
      $(table).append("<tr><th>ID</th><th>*Name</th><th>Description</th><th>*Payload Code</th><th>*</th></tr>")
      $(".payload_list_div_class").append(table)
      var header_row = $("<tr/>")
      for (var i=0; i<all_payload_data.length; i++){
        // Fetch relevant information
        var id = all_payload_data[i]["id"]
        var name = all_payload_data[i]["name"]
        var description = all_payload_data[i]["desc"]
        var js_code = all_payload_data[i]["js_code"]

        // Dynamically generate table and append inside list class
        var row = "<tr><td>" + id + "</td><td>" + name + "</td><td>" + description + "</td><td>" + js_code + "</td>"
        // Adds delete button
        row += "<td><input class='payload_btn_del_class' type='button' value=' - ' id='del_btn_id_" + name + "' /></td></tr>"
        // Append an empty row with text fields at the end in case user wants to add new payload
        $(table).append(row)
      }
      // Add a dropdown for selecting payloads
      var input_row = "<tr><td></td><td>"
      + MakeField("new_name")
      + "</td><td>"
      + MakeField("new_desc")
      +"</td><td>"
      + MakeField("new_js_code")
      + "</td>"
      input_row += "<td><input type='button' value=' + ' id='add_btn' /></td></tr>"
      $(table).append(input_row)
    console.log("Fetched all payloads")
  },
  error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("Failed to load all payloads");
  }
});

// Delete payload and refresh the list
$(document).on("click", ".payload_btn_del_class", function(){
  // Get payload url suffix and delete it
  var name = $(this).attr("id").replace("del_btn_id_", "")
  let data = {
    name : name
  }
  // Send ajax to backend
  $.ajax({
    url: '/api/payload/del',
    type: 'POST',
    data: data,
    success: function(response) {
        console.log("Delete payload success")
        // Refresh the page
        location.reload()
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log("Failed to del payload");
    }
  })
})


// Search payload when the search button has been clicked


// Add new payload and refresh the list
$(document).on("click", "#add_btn", function(){
  var new_name = $("#new_name").val()
  var new_desc = $("#new_desc").val()
  var new_js_code = $("#new_js_code").val()

  let data = {
    name  : new_name,
    desc  : new_desc,
    js_code  : new_js_code
  }
  // Send ajax to backend
  $.ajax({
    url: '/api/payload/add',
    type: 'POST',
    data: data,
    success: function(response) {
        console.log("Add payload success")
        // Refresh the page
        location.reload()
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log("Failed to add payload");
    }
  })
})
