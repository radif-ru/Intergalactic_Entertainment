function toggle_comments(el){
    $this = $(el)
    var form = $this.parent().find('form')
    if (form.is(':visible')){
        form.addClass('hide')
    }
    else{
        form.removeClass('hide')
    }
}

function toggleNotifi(){
    var box = $('#box')
    if (box.css('opacity') == 1){
    box.css({height: '0px',opacity:'0'})
    }
    else{
    box.css({height: '510px',opacity:'1'})
    }
}