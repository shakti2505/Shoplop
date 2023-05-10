$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// $('.plus-cart').click(function(){
//     let id = $(this).attr("pid").toString();
//     let eml = this.parentNode.children[2]
//     console.log(id)
//     $.ajax({
//         type:"GET",
//         url : "/pluscart",
//         data:{
//             prod_id:id
//         },
//         success: function(data){
//             eml.innerText = data.quantity
//             document.getElementById('amount').innerText= data.amount
//             document.getElementById('totalamount').innerText= data.totalamount

//         }
//     })
// })



// $('.minus-cart').click(function(){
//     let id = $(this).attr("pid").toString();
//     let eml = this.parentNode.children[2]
//     console.log(id)
//     $.ajax({
//         type:"GET",
//         url : "/minuscart",
//         data:{
//             prod_id:id
//         },
//         success: function(data){
//             eml.innerText = data.quantity
//             document.getElementById('amount').innerText= data.amount
//             document.getElementById('totalamount').innerText= data.totalamount

//         }
//     })
// })


$('.minus-cart').click(function(){
    let id = $(this).attr("pid").toString();
    let eml = this.parentNode.children[2]
    console.log(id)
    console.log('minus cart')
    $.ajax({
        type:"GET",
        url : "/update_cart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText= data.amount
            document.getElementById('totalamount').innerText= data.totalamount

        }
    })
})

$('.plus-cart').click(function(){
    let id = $(this).attr("pid").toString();
    let eml = this.parentNode.children[2]
    console.log(id)
    console.log('plus cart')
    $.ajax({
        type:"GET",
        url : "/update_cart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById('amount').innerText= data.amount
            document.getElementById('totalamount').innerText= data.totalamount

        }
    })
})


$('.remove-cart').click(function(){
    let id = $(this).attr("pid").toString();
    let eml = this
    $.ajax({
        type:"GET",
        url : "/removecart",
        data:{
            prod_id:id
        },
        success: function(data){
            console.log("delete")   
            document.getElementById('amount').innerText= data.amount
            document.getElementById('totalamount').innerText= data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()

        }
    })
})