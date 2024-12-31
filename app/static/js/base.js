$(document).ready(function() {
    $('.toast').toast('show');
    setActiveSidebarItem()
});

const addToast = (msg, title='Info', toast_class="bg-info") => {
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

const setActiveSidebarItem = () => {
    $('.nav-sidebar .nav-link').removeClass('active');
    let active_item = $(`a[href="${this.location.pathname}"]`);
    active_item.addClass('active')

    $('.nav-item').removeClass('menu-open');
    active_item.parent().parent().parent().addClass('menu-open')
}

