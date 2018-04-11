

$('#modal').on('shown.bs.modal', function () {
  $('#input').trigger('focus')
})

$('#tabForm a').on('click', function (e) {
    console.log('ready');
  e.preventDefault()
  $(this).tab('show')
})

$(document).ready(function() {
    console.log('ready');
    if (document.getElementById("timer")){
        sec = 0;
        setInterval(function(){
        sec++;
        document.getElementById("timer").innerText = sec;
        }, 1000);
    }
    $('.collapse').collapse()
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



