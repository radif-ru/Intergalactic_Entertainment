window.onload = ()=> {
    $('form.comment-form').on('click', 'button[type="submit"]', ()=>{
        var form = $('form.comment-form')
        var input = $('input.comment-input')
        var commentsWrapper = $('.comments-wrapper')
        $.post(form.attr('action'), form.serialize(), data => {
            switch (data.form_is_valid){
                case true:
                    $('.comments-div').html(data.form_html);
                    input.val('')
                    input.css({border: "1px solid black"})
                    break
                case false:
                    input.css({border: "1px solid red"})
                    break
                case 'AnonymousUser':
                    commentsWrapper.append('<p style="margin-top:10px;">Вы должны войти в аккаунт</p>')
                    input.val('')
                    break
            }
        });
        event.preventDefault();
    });
    $('i.like-button').on('click', ()=>{
        var target = $('i.like-button')
        var wrapper = $('.like-wrapper')
        var likeCount = document.querySelector('.likes')

        $.ajax({
            url:'/like/' + target.data('publ') + '/' + target.data('user'),
            success: (data) => {
                if (data.form_is_valid){
                    if (data.plus){
                        target.addClass('fas')
                        target.removeClass('far')
                        likeCount.innerText = Number(likeCount.innerText) + 1 
                    }
                    else{
                        target.addClass('far')
                        target.removeClass('fas')
                        likeCount.innerText = Number(likeCount.innerText) - 1 
                    }

                }
                else{
                    wrapper.append('<p style="margin-top:10px;">Вы должны войти в аккаунт</p>')
                }
            },
        });
        event.preventDefault();
    });
};