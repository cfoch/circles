//flow
function flow (is_paid_game) {
  var sequence = new Array(7);
  $( ".selector" ).draggable({
  revert: true,
  cursor: 'move',
  drag: function () { 
  }
  });
  $( ".circle" ).droppable({
  drop: function (event, ui) {
    var pos = $(this).attr('class').split(' ')[1];
    var selector = $(ui.draggable);
    var selector_color = selector.css("background-color");
    var circle_color = $(this).css("background-color");
    var exists_color = jQuery.inArray(selector_color, sequence);

    if (exists_color > -1) { //existe
      var pos_existing_color = sequence.indexOf(selector_color);
      var circle_with_current_color = $( "." + pos_existing_color);
      //removing existing color
      delete sequence[pos_existing_color];
      //sequence.remove(pos_existing_color);
      circle_with_current_color.css("background-color", "rgba(0, 0, 0, 0)");
    }
    $(this).css("background-color", selector_color);
    sequence[pos] = selector_color;
  }
  });
}
