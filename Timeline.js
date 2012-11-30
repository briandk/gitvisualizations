// Handling type-ahead functionality
$('#shaSearch').typeahead( {source: revisions} );

var timeline = {};
timeline.counter = 0;
timeline.revisions = revisions;
timeline.toggleBtn = function () { $(this).toggleClass("active") };
timeline.goToCommit = function(sha) {
  var destinationOffset = $('#' + sha).offset().left
  $(window).scrollLeft(destinationOffset)
};
timeline.navigateToRevisionFromSearch = function () {
  var sha = $('#shaSearch').val()
  timeline.goToCommit(sha)
}

$(".toggleable").bind('click', timeline.toggleBtn);
$("#goToSha").bind('click', timeline.navigateToRevisionFromSearch)
