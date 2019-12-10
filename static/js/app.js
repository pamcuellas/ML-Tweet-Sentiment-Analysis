$(document).ready(function(){

  // Start spinner effect on button when clicked
  $("#btn_pred").click( function (index) {
    $("#span_pred").addClass('spinner-border spinner-border-sm');
  });

  // Start spinner effect on button when clicked
  $("#btn_grab").click( function (index) {
    $("#span_grab").addClass('spinner-border spinner-border-sm');
  });    

  // Tooltip to present info about tweet.
  $('[data-toggle="tooltip"]').tooltip();   

  // Clean up text boxes
  $("#clean-up").click( function () {
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    $("#result img").attr("src", "../static/images/twitter.png");
  });      
});
