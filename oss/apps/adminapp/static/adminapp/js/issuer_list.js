(function ($) {
$('.btn-delete').click(function () {
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
})(jQuery);