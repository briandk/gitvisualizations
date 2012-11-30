// Handling type-ahead functionality
$('#shaSearch').typeahead( {source: revisions} );

var timeline = {};
timeline.toggleBtn = function () { $(this).toggleClass("active") };
timeline.goToCommit = function(commitHash) {
  destinationOffset = $('#' + commitHash).offset().left
  $(window).scrollLeft(destinationOffset)
}

$(".toggleable").bind('click', timeline.toggleBtn);
