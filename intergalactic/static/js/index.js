function toggle_comments(el){
    $this = $(el);
    var form = $this.parent().find('form').filter( ':first' );
    if (form.is(':visible')){
        form.addClass('hide');
    }
    else{
        form.removeClass('hide');
    }
}

function toggleNotifi(){
    var box = $('#box');
    if (box.is(':visible')){
        box.css({opacity:'0'});
        setTimeout(()=>{box.toggle()}, 700);
    }
    else{
        box.toggle();
        box.css({opacity:'1'});
    }
}