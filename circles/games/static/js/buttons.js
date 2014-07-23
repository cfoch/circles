function buttons() {
  //botones
  $( ".showme_off" ).click(function() {
    $( ".play_on" ).hide();
    $( ".showme_on" ).show();
    $( ".showme_off" ).hide();
    $( ".play_off" ).show();
    $( ".selectors-wrapper").hide();
    $( ".price").show();
  });
  $( ".play_off" ).click(function() {
    $( ".play_off" ).hide();
    $( ".showme_off" ).show();
    $( ".showme_on" ).hide();
    $( ".play_on" ).show();
    $( ".selectors-wrapper").show();
    $( ".price").hide();
  });
  $(".go").click(function() {
    //event.preventDefault();
    $('.paypal').submit();
  });
}
