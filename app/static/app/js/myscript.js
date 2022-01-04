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

//ajax for adding and removing the product
//increasing the quantity
$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2] //this is for showing if increased quantity
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity //this is for showing if increased quantity
            document.getElementById("amt").innerText = data.amt
            document.getElementById("total_amt").innerText = data.total_amt
            //console.log(data)
        }
    })
})

//decreasing the quantity
$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2] //this is for showing if increased quantity
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity //this is for showing if increased quantity
            document.getElementById("amt").innerText = data.amt
            document.getElementById("total_amt").innerText = data.total_amt
            //console.log(data)
        }
    })
})

//removing the item
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this //this is for showing if increased quantity
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success: function(data){
            //eml.innerText = data.quantity //this is for showing if increased quantity
            document.getElementById("amt").innerText = data.amt
            document.getElementById("total_amt").innerText = data.total_amt
            //console.log(data)
            //eml.parentNode.parentNode.parentNode.parentNode.remove()  //for removing the item in the cart
        }
    })
})
