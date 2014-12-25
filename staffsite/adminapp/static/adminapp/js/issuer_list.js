(function ($) {
    $('.btn-delete').click(function () {

        if (!confirm("delete?")) {
            return;
        }

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
        $('#search_btn')[0].href = ('/adminapp/issuer_list/?search=' +
                                    this.value);
    });

})(jQuery);

