$(window).on('load', function () {
    setTimeout(function () {
        $('.filters-fixed').addClass('active');
    }, 2000)
    setTimeout(function () {
        $('.filters-fixed').removeClass('active');
    }, 5500)
});

$(document).ready(function () {
    
    $('.brand-checkbox').on('click', event => {
        event.stopPropagation();
        const element = $(event.currentTarget).find('>input');
        filterPage($(element).attr('name'), $(element).val()) 
    })

    $('.category-checkbox').on('click', event => {
        event.stopPropagation();
        window.location.href = $(event.currentTarget).find('a').attr('href');
    })

    $('.in-stock-checkbox').on('click', event => {
        const element = $(event.currentTarget).find('input')
        filterPage($(element).attr('name'), $(element).prop("checked") ? 1 : 0)
    })

    $('#paginateByInput, #orderByInput').on('change', (event) => {
        filterPage($(event.currentTarget).attr("name"), $(event.currentTarget)?.val())
    })

    function filterPage(inputName, value) {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        if (value) {
            params.set(inputName, value)
        } else {
            params.delete(inputName)
        }
        window.location.search = params.toString()
    }
});