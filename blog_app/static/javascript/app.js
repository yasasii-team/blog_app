$(function(){
    $('.delete_button').on('click', function(){
        var id = $(this).attr("id");
        var csrf_token = $('meta[name="csrf_token"]').attr('content');
        var send_data  = {
            'id': id,
        };

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })

        if (confirm('本当に投稿を削除しますか？')) {
            $.ajax({
                url: '/delete',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify(send_data),
                contentType: 'application/json'
            })
            .done((data) => {
                $('#deleted_post_' + data.id).fadeOut();
            });
        }
    });
});