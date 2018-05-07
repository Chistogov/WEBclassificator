$('#modal').on('shown.bs.modal', function () {
  $('#input').trigger('focus')
});

$('#tabForm a').on('click', function (e) {
    console.log('ready');
  e.preventDefault();
  $(this).tab('show')
});

$('.dropdown-toggle').dropdown();

$(document).ready(function() {
    console.log('ready');
    if (document.getElementsByClassName("timer")[0]){
        sec = 0;
        setInterval(function(){
        sec++;
        var timers = document.getElementsByClassName("timer");
        for (var i = 0; i < timers.length; i++) {
          timers[i].innerText=sec;
          timers[i].setAttribute("value", sec);
        }
        }, 1000);
    }
    $('.collapse').collapse();
    $('.dropdown-toggle').dropdown();
    $('[data-toggle="tooltip"]').tooltip()
    $('.datepicker').datepicker({
    format: 'mm/dd/yyyy',
    startDate: '-3d'
    });
});

$('#timer').on('click', function(e)
{
    // e.preventDefault()
    // console.log('ready');
    // sec = 0;
    // setInterval(function(){
    // sec++;
    // document.getElementById("timer").innerText = sec;
    // }, 1000);
});



