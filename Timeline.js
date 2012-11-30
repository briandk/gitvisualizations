// Handling type-ahead functionality
$('#shaSearch').typeahead( {source: revisions} );

var timeline = {};
timeline.revisions = revisions;
timeline.scrollSpeed = 400;
timeline.shaCounter = 0;
timeline.shortShaLength = 8
timeline.toggleBtn = function () { $(this).toggleClass("active") };
timeline.goToCommit = function(sha) {
  var destinationOffset = $('#' + sha).offset().left;
  $("body").animate({scrollLeft: destinationOffset}, this.scrollSpeed);
  this.updateDisplay
};
timeline.navigateToRevisionFromSearch = function () {
  var sha = $('#shaSearch').val();
  timeline.goToCommit(sha);
  timeline.updateDisplay(sha);
}
timeline.updateDisplay = function(sha) {
  this.shaCounter = this.revisions.indexOf(sha);
  shortSha = sha.slice(0, this.shortShaLength);
  $('#shaDisplay').html(shortSha);
}

$(".toggleable").bind('click', timeline.toggleBtn);
$("#shaForm").on('submit', function () {return(false)});
$("#goToSha").on('click', timeline.navigateToRevisionFromSearch);
timeline.updateDisplay(timeline.revisions[0]);
