$('.collapse').collapse()

$('#modal').on('shown.bs.modal', function () {
  $('#input').trigger('focus')
})

$('#tabForm a').on('click', function (e) {
  e.preventDefault()
  $(this).tab('show')
})

