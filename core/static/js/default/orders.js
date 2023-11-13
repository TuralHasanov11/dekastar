$(document).ready(() => {

    console.log(addToCartURI, removeFromCartURI)

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
            console.log(`.cart-block-item[data-product_id="${data?.item?.product?.id}"]`)
            if($(`.cart-block-item[data-product_id="${data?.item?.product?.id}"]`)){
                $(`.cart-block-item[data-product_id="${data?.item?.product?.id}"]`).remove()
                $("#cart-products").append(productComponent(data?.item))
            }else{
                $("#cart-products").append(productComponent(data?.item))
            }
        } catch (error) { }
    })


    function productComponent(item){
        let priceComponent;
        if(item?.product?.discount){
            priceComponent = `<span class="final">&#8380; <span class="discount-price">${item?.product?.discount_price}</span></span>
                            <span class="discount">&#8380; <span class="regular-price">${item?.product?.regular_price}</span></span>`
        }else{
            priceComponent = `<span class="final">&#8380; <span class="discount-price">${item?.product?.regular_price}</span></span>`
        }

        return `<div class="cart-block cart-block-item clearfix" data-product_id="${item?.product?.id}">
            <div class="image">
            <a href="${productDetailURI.replace("product_slug", item?.product?.slug)}">
                <img src="${item?.product?.get_image_feature}" alt="${item?.product?.name}" />
            </a>
            </div>
            <div class="title">
                <div><a href="${productDetailURI.replace("product_slug", item?.product?.slug)}">${item?.product?.name}</a></div>
            </div>
            <div class="quantity">
                <input type="number" value="${item?.quantity}" class="form-control form-quantity" />
            </div>
            <div class="price">
            ${priceComponent}
            </div>
            <span class="icon icon-cross icon-delete"></span>
        </div>`
    }
});
