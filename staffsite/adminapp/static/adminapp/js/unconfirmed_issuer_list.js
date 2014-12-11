(function ($) {
$('.btn-issuer-reject').click(function () {
  var button = this;
  console.log($(button).data('href'))
  $.ajax({
    'url': $(button).data('href'),
    'type': 'POST'
  }).done(function () {
    $(button).parents('.issuer').remove();
  }).fail(function (e) {
    console.log(e);
  });
});

$('.btn-issuer-accept').click(function () {
  var button = this;
  $.ajax({
    'url': $(button).data('href'),
    'type': 'POST'
  }).done(function () {
    $(button).parents('.issuer').remove();
  }).fail(function (e) {
    console.log(e);
  });
});

$('#search_box').keyup(function () {
var search = this;
$('#search_btn')[0].href = '/adminapp/unconfirmed_issuer_list/?search=' + this.value;
});

})(jQuery);

