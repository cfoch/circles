function show_payment(n_seq, pk) {
  var payment;
  $.ajax({
    type: "post",
    url: "/games/get_payment/",
    data: {game: pk, n: n_seq} ,
    success: function (data) {
      var payment = data['payment'];
      $( ".price" ).html( 'Total: $' + payment );
      $( "input[name=amount]" ).val(payment);
    }
  });
}

function counter(pk) {
   var showme_n = 1;

  $( "#counter_down" ).click(function() {
    showme_n--;
    $('#showme_n').empty();
    if ((showme_n == 0) || (showme_n == 1)){
      if (showme_n == 0) { showme_n++ };
      $('#showme_n').append('SHOW ME ' + showme_n + ' SEQUENCE');
    }
    else {
      $('#showme_n').append('SHOW ME ' + showme_n + ' SEQUENCES');
    }
    show_payment(showme_n, pk);
    $('input[name=custom]').val('quantity=' + showme_n);
  });
  $( "#counter_up" ).click(function() {
    showme_n++;
    $('#showme_n').empty();
    $('#showme_n').append('SHOW ME ' + showme_n + ' SEQUENCES');
    show_payment(showme_n, pk);
    $('input[name=custom]').val('quantity=' + showme_n);
  });
}


