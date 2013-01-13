// Handling type-ahead functionality
$('#shaSearch').typeahead( {source: revisions} );

var timeline = {};
timeline.revisions = revisions;
timeline.scrollSpeed = 300;
timeline.shaCounter = 0;
timeline.currentSha = "";
timeline.zoomLevel = 1;
timeline.shortShaLength = 8;
timeline.toggleBtn = function () { $(this).toggleClass("active") };
timeline.goToCommit = function(sha) {
  var destinationOffset = $('#' + sha).offset().left;
  if (parseInt($('body').scrollLeft()) != parseInt(destinationOffset)) {
    $("body").animate({scrollLeft: destinationOffset}, timeline.scrollSpeed);
  }
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
  var prevCommit = $('.page-backward');
  var nextCommit = $('.page-forward');

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

timeline.navigateToCommitFromPager = function () {
  if (!$(this).hasClass("disabled")) {
    var counterIncrement = parseFloat($(this).attr('data-counter-increment'));
    var sha = timeline.revisions[timeline.shaCounter + counterIncrement];
    timeline.goToCommit(sha);
  }
};


timeline.bindHashesToShaLinks = function () {
  $('.shaLink').each(function (i) { $(this).data("sha", timeline.revisions[i]) });
  $('#first-commit-btn').data("sha", timeline.revisions[0]);
  $('#last-commit-btn').data("sha", timeline.revisions[timeline.revisions.length - 1]);
  $('.shaLink, #first-commit-btn, #last-commit-btn').on('click', function () { timeline.goToCommit($(this).data("sha")) });
};

timeline.zoom = function () {
  var scaleFactor = 1 / parseFloat($(this).attr("data-zoom"));
  var destinationOffset = scaleFactor * $('#' + timeline.currentSha).offset().left;
  var fontScale = (100/scaleFactor);
  var leftOffset = $('#' + timeline.currentSha).offset().left;
  var scale = timeline.getTransform("", "scale(" + scaleFactor + ")");

  $('table').css(scale);
  $("body").animate({scrollLeft: destinationOffset}, 500);
  setTimeout(function () { $('.snapshotMetadata').css("font-size", fontScale + '%') }, 501);
  setTimeout(function () {timeline.goToCommit(timeline.currentSha)}, 645);
  $('.zoomLevel').removeClass("disabled");
  $(this).addClass("disabled");
};

timeline.getTransform = function(property, value) {
  var propertiesMap = {};
  propertiesMap["-webkit-transform" + property] = value;
  propertiesMap["-ms-transform" + property] = value;
  propertiesMap["-moz-transform" + property] = value;
  propertiesMap["-o-transform" + property] = value;

  return propertiesMap;
};


$(".toggleable").on('click', timeline.toggleBtn);
$("#shaForm").on('submit', function () {return(false)});
$("#goToSha").on('click', timeline.navigateToRevisionFromSearch);
$('#next-commit-btn').on('click', timeline.navigateToCommitFromPager);
$('#prev-commit-btn').on('click', timeline.navigateToCommitFromPager);
$('.zoomLevel').on('click', timeline.zoom);
timeline.bindHashesToShaLinks();
timeline.update(timeline.revisions[0]);
