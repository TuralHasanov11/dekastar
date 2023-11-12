$(document).ready(function () {
    $('.category-input-label').on('click', event => {
        window.location.href = $(event.currentTarget).closest('.category-checkbox').find('.category-change-link').attr('href');
    })

    $('#inStock').on('click', event => {
        window.location.href = $(event.currentTarget).closest('.in-stock-checkbox').find('.in-stock-change-link').attr('href');
    })

    $('.brand-input-label').on('click', event => {
        window.location.href = $(event.currentTarget).closest('.brand-checkbox').find('.brand-change-link').attr('href');
    })
});
