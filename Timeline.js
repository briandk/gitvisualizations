// Handling type-ahead functionality
$('#shaSearch').typeahead( {source: revisions} );

var timeline = {};
timeline.revisions = revisions;
timeline.scrollSpeed = 400;
timeline.shaCounter = 0;
timeline.currentSha = ""
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
  timeline.currentSha = sha;
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

timeline.navigateToCommitFromPager = function() {
  if (!$(this).hasClass("disabled")) {
    var counterIncrement = parseFloat($(this).attr('data-counter-increment'));
    var sha = timeline.revisions[timeline.shaCounter + counterIncrement];
    timeline.goToCommit(sha);
  }
}

timeline.bindHashesToShaLinks = function () {
  $('.shaLink')
    .each(function (i) { $(this).data("sha", timeline.revisions[i]) })
    .on('click', function () { timeline.goToCommit($(this).data("sha")) });
}

timeline.zoom = function () {
  // To zoom
    // get the scale factor
    // get the left-offset of the currently displayed commit
    // set the transform-origin of the table to be the left offset
    // transform the table
    // change the metadata font size

  var scaleFactor = parseFloat($(this).attr("data-zoom"));
  var scaleFactorAsString = "scale(" + scaleFactor + ")";
  var fontScale = (100/scaleFactor);

  var tableTransforms = {"-webkit-transform":   scaleFactorAsString,
                         "-ms-transform":       scaleFactorAsString,
                         "-moz-transform":      scaleFactorAsString,
                         "-o-transform-origin": scaleFactorAsString};

  var metaDataTransforms = {"font-size": (fontScale + '%')};

  $('table').css(tableTransforms);
  $('.snapshotMetadata').css(metaDataTransforms);
}

$(".toggleable").on('click', timeline.toggleBtn);
$("#shaForm").on('submit', function () {return(false)});
$("#goToSha").on('click', timeline.navigateToRevisionFromSearch);
$('.pager-btn').on('click', timeline.navigateToCommitFromPager);
timeline.bindHashesToShaLinks();
timeline.update(timeline.revisions[0]);
