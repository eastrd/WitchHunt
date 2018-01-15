$(function(){
  $("#contentDrop").change(function(){
    var selected = $(this).find(":selected").val();
    if (selected=="custom"){
      $("#contentDrop").after(
        '<div class="ui input" id="customContent">'
        +
        '<input type="text" id="contentURL" placeholder="http://real-site.com/abc/page.aspx">'
        +
        '</div>'
      );
    }
    else{
      $("#customContent").remove();
    }
  });

  $("#submit").click(function(){
    var notes = $("#notes").val();
    var url = $("#url").val();
    var content = $("#contentDrop").find(":selected").val();
    if (content == "custom"){
      content = $("#contentURL").val();
    }
    var time = $("#time").val();
    var email = $("#email").val();

    var postData = {};
    postData["notes"] = notes;
    postData["url"] = url;
    postData["content"] = content;
    postData["time"] = time;
    postData["email"] = email;
    postData["time"] = time;

    $.ajax({
      type:   "POST",
      url:    "/tavern",
      data:   postData,
      success: function(response, xml){
        alert("Setting Up...");
        if (response == "1"){
          alert("Success");
        }
        else{
          if (response == "0"){
            alert("Endpoint already exists");
          }
          else{
            alert("Internal Error");
          }
        }
      },
      fail: function(status){
        alert(status);
      }
    });

  });

});
