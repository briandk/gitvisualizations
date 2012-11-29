// Handling type-ahead functionality
$('#shaSearch').typeahead( {source: revisions} );


var timeline = {
  toggleBtn: function (evt) {
    //console.log(this.id);

    $(this).toggleClass("active");
    /*
    if ( $(this).hasClass("active") ) {
      $(this).removeClass("active");
    } else {
      $(this).addClass("active");
    }
    */
  }

};

$(".toggleable").bind('click', timeline.toggleBtn);
