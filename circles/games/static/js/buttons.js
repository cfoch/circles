function buttons(is_paid_game) {
  $( ".showme_off" ).click(function() {
    $( ".play_on" ).hide();
    $( ".showme_on" ).show();
    $( ".showme_off" ).hide();
    $( ".play_off" ).show();
    $( ".selectors-wrapper" ).hide();
    $( ".price" ).show();
    if (is_paid_game) {
      $( ".click2show" ).show();
      $( ".payment_advise" ).show();
      $( ".paypal_form" ).hide();
    }
  });
  $( ".play_off" ).click(function() {
    $( ".play_off" ).hide();
    $( ".showme_off" ).show();
    $( ".showme_on" ).hide();
    $( ".play_on" ).show();
    $( ".selectors-wrapper" ).show();
    $( ".price" ).hide();
    if (is_paid_game) {
      $( ".click2show" ).hide();
      $( ".payment_advise" ).hide();
      $( ".paypal_form" ).show();
    }
  });
  $(".go").click(function() {
    //event.preventDefault();
    $('.paypal').submit();
  });
}
