$('#nextBtn1').on('click', function (e) {
     $(".progress-bar").css('width', '25%');
})

$('#nextBtn2').on('click', function (e) {
     $(".progress-bar").css('width', '50%');
})

$('#nextBtn3').on('click', function (e) {
     $(".progress-bar").css('width', '75%');
})

$('#backBtn2').on('click', function (e) {
     $(".progress-bar").css('width', '0%');
})

$('#backBtn3').on('click', function (e) {
     $(".progress-bar").css('width', '25%');
})

// Activate Carousel
$("#myCarousel").carousel();

// Enable Carousel Indicators
$(".item").click(function(){
  $("#myCarousel").carousel(1);
});

// Enable Carousel Controls
$(".left").click(function(){
  $("#myCarousel").carousel("prev");
});

