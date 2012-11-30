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
  $("body").animate({scrollLeft: destinationOffset}, timeline.scrollSpeed);
  timeline.update(sha);
};
timeline.navigateToRevisionFromSearch = function () {
  var sha = $('#shaSearch').val();
  timeline.goToCommit(sha);
  timeline.update(sha);
};

timeline.update = function(sha) {
  timeline.shaCounter = timeline.revisions.indexOf(sha);
  shortSha = sha.slice(0, timeline.shortShaLength);
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

timeline.navigateToPreviousCommit = function () {
  var sha = timeline.revisions[(timeline.shaCounter - 1)];
  timeline.goToCommit(sha);
}

timeline.navigateToNextCommit = function () {
  var sha = timeline.revisions[(timeline.shaCounter + 1)];
  timeline.goToCommit(sha);
};

timeline.navigateToPreviousCommit = function () {
  var sha = timeline.revisions[(timeline.shaCounter - 1)];
  timeline.goToCommit(sha);
};

timeline.bindHashesToShaLinks = function () {
  $('.shaLink').each(function (i) { $(this).data("sha", timeline.revisions[i]) });
}

timeline.navigateToCommitFromLink = function () {
  timeline.goToCommit($(this).data("sha"));
}

$(".toggleable").on('click', timeline.toggleBtn);
$("#shaForm").on('submit', function () {return(false)});
$("#goToSha").on('click', timeline.navigateToRevisionFromSearch);
$('#next-commit-btn').on('click', timeline.navigateToNextCommit);
$('#prev-commit-btn').on('click', timeline.navigateToPreviousCommit);
timeline.bindHashesToShaLinks();
$('.shaLink').on('click', timeline.navigateToCommitFromLink);
timeline.update(timeline.revisions[0]);
