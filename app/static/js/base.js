$(document).ready(function() {
    $('.toast').toast('show');
});

function addToast(msg, title='Info', toast_class="bg-info"){
    let toast = $(document).Toasts('create', {
        'title': title,
        'body': msg,
        'position': 'bottomRight',
        'class': `${toast_class} alert-toast`,
        'fixed': true,
        'autohide': true,
        'delay': 3000
        });
}
