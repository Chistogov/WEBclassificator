$('#modal').on('shown.bs.modal', function () {
  $('#input').trigger('focus')
});

$('#tabForm a').on('click', function (e) {
    console.log('ready');
  e.preventDefault();
  $(this).tab('show')
});

// $('.dropdown-toggle').dropdown();

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
    $('.collapse').on('show.bs.collapse', function (e) {
        $('.collapse').collapse("hide")
    })
    $('.checktag').click(function() {
        var checks = document.getElementsByClassName("checkitem");
        document.getElementById("params").innerText="";
        for (var i = 0; i < checks.length; i++) {
            if(checks[i].checked)
            {
                document.getElementById("params").innerHTML += '<li>'+checks[i].dataset.name;
            }
        }
    });
    $('.checktag_d').click(function() {
        var checks = document.getElementsByClassName("checkitem_d");
        document.getElementById("params_d").innerText="";
        for (var i = 0; i < checks.length; i++) {
            if(checks[i].checked)
            {
                document.getElementById("params_d").innerHTML += '<li>'+checks[i].dataset.name;
            }
        }
    });
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