$(document).ready(() => {

    function blinkColor(element) {
        element.addClass("text-danger", 500);
        setTimeout(() => {
            element.removeClass("text-danger", 500);
        }, 500);
    }

    $(".btn-add").on("click", async (event) => {
        try {
            const productId = $(event.currentTarget).data('product_id')

            const response = await fetch(addToCartURI, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: productId
                }),
                headers: { "X-CSRFToken": csrftoken, 'Content-Type': 'application/json' }
            })

            const data = await response.json()

            $("#cart-total-price").html(data?.total_price)
            $("#cart-quantity").html(data?.quantity)
            blinkColor($(".open-cart"));
            if ($(`.cart-nav-item[data-product_id="${data?.item?.product?.id}"]`)) {
                $(`.cart-nav-item[data-product_id="${data?.item?.product?.id}"]`).remove()
                $("#cart-products").append(productComponent(data?.item))
            } else {
                $("#cart-products").append(productComponent(data?.item))
            }
        } catch (error) { }
    })

    $(".btn-add-many").on("click", async (event) => {
        try {
            const productId = $(event.currentTarget).data('product_id')

            const response = await fetch(addToCartURI, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: productId,
                    product_quantity: parseInt($("#product-quantity").val())
                }),
                headers: { "X-CSRFToken": csrftoken, 'Content-Type': 'application/json' }
            })

            const data = await response.json()

            $("#cart-total-price").html(data?.total_price)
            $("#cart-quantity").html(data?.quantity)
            blinkColor($(".open-cart"));
            if ($(`.cart-nav-item[data-product_id="${data?.item?.product?.id}"]`)) {
                $(`.cart-nav-item[data-product_id="${data?.item?.product?.id}"]`).remove()
                $("#cart-products").append(productComponent(data?.item))
            } else {
                $("#cart-products").append(productComponent(data?.item))
            }
        } catch (error) { }
    })

    $(".icon-delete").on("click", async (event) => {
        try {
            const productId = $(event.currentTarget).closest(".cart-checkout-item").data('product_id')
            const response = await fetch(removeFromCartURI, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: productId
                }),
                headers: { "X-CSRFToken": csrftoken, 'Content-Type': 'application/json' }
            })

            if (response.ok) {
                location.reload()
            } else {
                throw new Error()
            }
        } catch (error) { }
    })

    $(".form-quantity").on("click", async (event) => {
        $(event.currentTarget).attr("disabled", "disabled")

        const productId = $(event.currentTarget).closest(".cart-checkout-item").data('product_id')

        try {
            const response = await fetch(updateCartURI, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: productId,
                    product_quantity: $(event.currentTarget).val()
                }),
                headers: { "X-CSRFToken": csrftoken, 'Content-Type': 'application/json' }
            })

            const data = await response.json()

            $("#cart-total-price").html(data?.total_price)
            $(".checkout-total-price").html(data?.total_price)
            $("#checkout-discount-price").html(data?.total_discount)
            $("#checkout-regular-price").html(data?.total_regular_price)
            $("#cart-quantity").html(data?.quantity)
            blinkColor($(".open-cart"));
            if (data.item === null) {
                $(`.cart-nav-item[data-product_id="${data?.item?.product?.id}"]`).remove()
            }
            else {
                $(`.cart-nav-item[data-product_id="${data?.item?.product?.id}"]`).remove()
                $("#cart-products").append(productComponent(data?.item))
            }
        } catch (error) {
        } finally {
            $(event.currentTarget).removeAttr("disabled")
        }
    })


    function productComponent(item) {
        let priceComponent;
        if (item?.product?.discount) {
            priceComponent = `<span class="final">&#8380; <span class="discount-price">${item?.product?.discount_price}</span></span>
                            <span class="discount">&#8380; <span class="regular-price">${item?.product?.regular_price}</span></span>`
        } else {
            priceComponent = `<span class="final">&#8380; <span class="discount-price">${item?.product?.regular_price}</span></span>`
        }

        return `<div class="cart-block cart-block-item clearfix cart-nav-item" data-product_id="${item?.product?.id}">
            <div class="image">
            <a href="${productDetailURI.replace("product_slug", item?.product?.slug)}">
                <img src="${item?.product?.get_image_feature}" alt="${item?.product?.name}" />
            </a>
            </div>
            <div class="title">
                <div><a href="${productDetailURI.replace("product_slug", item?.product?.slug)}">${item?.product?.name}</a></div>
            </div>
            <div class="quantity">${item?.quantity}</div>
            <div class="price">
            ${priceComponent}
            </div>
        </div>`
    }

    $("#btn-whatsapp-order").on("click", async (event) => {
        const phone = $(event.currentTarget).data('phone')
        try {
            const response = await fetch(getCartDetailURI, {
                method: 'GET',
                headers: { "X-CSRFToken": csrftoken, 'Content-Type': 'application/json' }
            })

            const data = await response.json()

            let text = "Sifariş:%0a"

            Object.values(data).forEach(item => {
                text += `${item?.product?.name} - ${item?.quantity}%0a`
            })

            window.open(`https://wa.me/${phone}?text=${text}`, '_blank').focus();
        } catch (error) {

        }
    })
});
