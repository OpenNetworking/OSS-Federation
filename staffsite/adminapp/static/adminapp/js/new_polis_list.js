(function ($) {
$('.btn-confirm').click(function () {
  var button = this;
  $.ajax({
    'url': $(button).data('href'),
    'type': 'POST'
  }).done(function () {
    $(button).parents('.polis_owner').remove();
  }).fail(function (e) {
    console.log(e);
  });
});
})(jQuery);