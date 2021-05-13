window.onload = () => {
  $('form.comment-form').on('click', 'button[type="submit"]', (ev) => {
    // var form = $('form.comment-form')
    // var input = $('input.comment-input')
    // var commentsWrapper = $('.comments-wrapper')
    // var commentCount = document.querySelector('.comments-count')
    var form = $(ev.target.parentNode.parentNode)
    var input = $(form).find('input.comment-input')
    // var commentsWrapper = $('.comments-wrapper')
    var commentCount = document.querySelector('.comments-count')
    $.post(form.attr('action'), form.serialize(), data => {
      switch (data.form_is_valid) {
        case 'AnonymousUser':
          if (!form.parent().children('.AnonymousUser').length) {
            form.parent().append('<p class="AnonymousUser" style="margin-top:10px; color: red">Вы должны войти в аккаунт</p>')
          }
          input.val('')
          form.addClass('hide')
          break
        case true:
          $('.comments-div').html(data.form_html);
          commentCount.innerText = Number(commentCount.innerText) + 1
          input.val('')
          input.css({border: '1px solid black'})
          break
        case false:
          input.css({border: '1px solid red'})
          break
      }
    });
    event.preventDefault();
  });
  $('i.like-button').on('click', () => {
    var target = $('i.like-button')
    var dislikeCount = document.querySelector('.dislikes')
    var dislike = $('i.dislike-button')
    var wrapper = $('.like-wrapper')
    var likeCount = document.querySelector('.likes')

    $.ajax({
      url: '/like/' + target.data('publ') + '/' + target.data('user') + '/like',
      success: (data) => {
        if (data.form_is_valid) {
          if (data.plus) {
            target.addClass('fas')
            target.removeClass('far')
            likeCount.innerText = Number(likeCount.innerText) + 1
          } else {
            target.addClass('far')
            target.removeClass('fas')
            likeCount.innerText = Number(likeCount.innerText) - 1
          }

          if (data.minus) {
            dislike.addClass('far')
            dislike.removeClass('fas')
            dislikeCount.innerText = Number(dislikeCount.innerText) - 1
          }

        } else {
          if (!wrapper.parent().children('.AnonymousUserLike').length) {
            wrapper.parent().append('<p class="AnonymousUserLike" style="margin-top:10px; color: red">Чтобы лайкать, Вы должны войти в аккаунт</p>')
          }
        }
      },
    });
    event.preventDefault();
  });
  $('i.dislike-button').on('click', () => {
    var like = $('i.like-button')
    var dislikeCount = document.querySelector('.dislikes')
    var dislike = $('i.dislike-button')
    var wrapper = $('.like-wrapper')
    var likeCount = document.querySelector('.likes')

    $.ajax({
      url: '/like/' + dislike.data('publ') + '/' + dislike.data('user') + '/dislike',
      success: (data) => {
        if (data.form_is_valid) {
          if (data.plus) {
            dislike.addClass('fas')
            dislike.removeClass('far')
            dislikeCount.innerText = Number(dislikeCount.innerText) + 1
          } else {
            dislike.addClass('far')
            dislike.removeClass('fas')
            dislikeCount.innerText = Number(dislikeCount.innerText) - 1
          }

          if (data.minus) {
            like.addClass('far')
            like.removeClass('fas')
            likeCount.innerText = Number(likeCount.innerText) - 1
          }

        } else {
          if (!wrapper.parent().children('.AnonymousUserDis').length) {
            wrapper.parent().append('<p class="AnonymousUserDis" style="margin-top:10px; color: red">Чтобы дизлайкать, Вы должны войти в аккаунт</p>')
          }
        }
      },
    });
    event.preventDefault();
  });
  $('.notifi-item').on('click', 'i.fa-trash-alt', () => {
    var button = $(event.currentTarget).find('i')
    var count = document.querySelector('.notifications-count1')
    var count2 = document.querySelector('.notifications-count2')

    $.ajax({
      url: '/notification_read/' + button.data('id') + '/' + button.attr('name'),
      success: (data) => {
        button.parent().remove()
        count.innerText = Number(count.innerText) - 1
        count2.innerText = Number(count2.innerText) - 1
      },
    });
    event.preventDefault();
  });

  $('#pub_rating').on('click', 'i.icon-star', (event) => {
    const pub_id = event.target.parentElement.dataset.pubid
    const user_pub_rating = +event.target.dataset.rating
    const wrapper = $('#pub_rating')
    const user_pub_rating_el = $('#user_pub_rating')
    const average_pub_rating_el = $('#average_pub_rating')

    $.post('/user_pub_rating/', {
      user_pub_rating: user_pub_rating,
      pub_id: pub_id
    }, function (data) {
      if (data.form_is_valid && data.form_is_valid !== 'AnonymousUser') {
        user_pub_rating_el.text(data.user_pub_rating);
        average_pub_rating_el.text(data.average_pub_rating);
      } else if (data.form_is_valid === 'AnonymousUser') {
        if (!wrapper.parent().children('.AnonymousUserDis').length) {
          wrapper.parent().append('<p class="AnonymousUserDis" style="margin-top:10px; color: red">Чтобы ставить рейтинг, Вы должны войти в аккаунт</p>')
        }
      } else {
        if (!wrapper.parent().children('.AnonymousUserDis').length) {
          wrapper.parent().append('<p class="AnonymousUserDis" style="margin-top:10px; color: red">Непредвиденная ошибка!</p>')
        }
      }
    });
    event.preventDefault();
  });
};