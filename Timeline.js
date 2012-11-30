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
  timeline.update(sha);
};

timeline.update = function(sha) {
  this.shaCounter = this.revisions.indexOf(sha);
  shortSha = sha.slice(0, this.shortShaLength);
  $('#shaDisplay').html(shortSha);
  timeline.updatePagerButtons();
};

timeline.updatePagerButtons = function () {
  var prevCommit = $('#prev-commit-btn');
  var nextCommit = $('#next-commit-btn');

  if (this.shaCounter == 0) {
    prevCommit.addClass("disabled");
  } else {
    prevCommit.removeClass("disabled");
  }

  if (this.shaCounter == (this.revisions.length - 1)) {
    nextCommit.addClass("disabled");
  } else {
    nextCommit.removeClass("disabled");
  }
};

$(".toggleable").bind('click', timeline.toggleBtn);
$("#shaForm").on('submit', function () {return(false)});
$("#goToSha").on('click', timeline.navigateToRevisionFromSearch);
timeline.update(timeline.revisions[0]);
