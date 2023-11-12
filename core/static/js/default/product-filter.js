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
        filterPage({[$(element).attr('name')]: $(element).val()})
    })

    $('.category-checkbox').on('click', event => {
        event.stopPropagation();
        window.location.href = $(event.currentTarget).find('a').attr('href');
    })

    $('.in-stock-checkbox').on('click', event => {
        const element = $(event.currentTarget).find('input')
        filterPage({[$(element).attr('name')]: $(element).prop("checked") ? 1 : 0})
    })

    $('#paginateByInput, #orderByInput').on('change', (event) => {
        filterPage({[$(event.currentTarget).attr("name")]: $(event.currentTarget)?.val()})
    })

    $("#priceRangeSubmitBtn").on('click', (event) => {
        event.preventDefault()
        console.log(minPrice, maxPrice)
        filterPage({ "min_price": minPrice, "max_price": maxPrice })
    })

    function filterPage(query) {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        Object.keys(query).forEach(key => {
            if (query[key]) {
                params.set(key, query[key])
            } else {
                params.delete(key)
            }
        })
        window.location.search = params.toString()
    }
});
