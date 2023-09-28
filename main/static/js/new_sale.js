$(document).ready(function() {
    const serviceSelect = $("#service").select2();
    const clientSelect = $("#client").select2();
    const taxes = JSON.parse(document.getElementById('tax_list').textContent); 
    for(const tax of taxes){
        console.log(tax)
    }
    $("#sale_type").on(
        "change", function(e) {
            console.log(e);
            selectType(e);
        }
    )

    $("#discount").on(
        "change", function(e){
            calculatePrice()
        }
    )

    $("#service").on(
        "change", function(e) {
            console.log(e);
            changePrice(e);
        }
    )

    $("#sessions").on(
        "change", function(e){
            calculatePrice();
        }
    )

    $("#mixed").on(
        "change", function(e) {
            $(".payment2").attr("hidden", e.target.value=="0");
            $(".paymentInput2").attr("required", e.target.value=="1");
            $("#price1").attr("readonly", e.target.value=="0");
            $("#price1").val($("#final_price").val())
        }
    )

    $("#payment_type").on(
        "change", function(e){
            $(".taxDiv").attr("hidden", $(this).find(":selected").data("tax")=="False")
            $(".taxInput").attr("required", !($(this).find(":selected").data("tax")=="False"))
            $("#tax").empty();
            $("#tax").append(new Option("Selecione", null, true, true));
            for(const tax of taxes){
                if(tax.payment_type_id==$(this).val()) $("#tax").append(new Option(tax.name, tax.id, false, false))
            }
        }
    )

    $("#payment_type2").on(
        "change", function(e){
            $(".taxDiv2").attr("hidden", $(this).find(":selected").data("tax")=="False")
            $(".taxInput2").attr("required", !($(this).find(":selected").data("tax")=="False"))
            $("#tax2").empty();
            $("#tax2").append(new Option("Selecione", null, true, true));
            
            for(const tax of taxes){
                if(tax.payment_type_id==Number($(this).val())) $("#tax2").append(new Option(tax.name, tax.id, false, false))
            }
        }
    )

    $("#installments1").on(
        "change", function(e){
            if($(this).val()>12) $(this).val(12);
            if($(this).val()<1) $(this).val(1);
        }
    )

    $("#installments2").on(
        "change", function(e){
            if($(this).val()>12) $(this).val(12);
            if($(this).val()<1) $(this).val(1);
        }
    )

    $("#price1").on(
        "change", function(e){
            price1 = Number($("#price1").val());
            final_price = Number($("#final_price").val());

            if(price1>final_price){
                $("#price1").val(final_price);
                $("#price2").val(0);
            } else {
                $("#price2").val((final_price-price1).toFixed(2));
            }
        }
    )

        // Funções
    function selectType(event){
        $("#service_label").text($("#sale_type").find(":selected").text() + '*');
        $("#service").empty()    
        $.ajax({
            url:"saleServiceAjax/"+event.target.value,
            method:"GET", 
            dataType:"json",
            success: function(data){
                $("#service").append(new Option("Selecione", null, true, true));
              console.log(data)
              for(var i=0; i<data.length;i++){
                option = new Option(data[i].name, data[i].id, false, false);
                $(option).data("price", data[i].price);
                $(option).data("sessions", data[i].sessions);

                $("#service").append(option);
              }
            },
        });
        
        if(event.target.value == "1"){
            $("#sessions").attr("readonly", true);
        } else {
            $("#sessions").attr("readonly", false);
        }
        console.log("AAAAA")
        return $("#service").trigger("change");  
    }

    function changePrice(event){
        $("#price").val($(event.target).find(":selected").data("price"))
        $("#sessions").val($(event.target).find(":selected").data("sessions"))

        calculatePrice();
    }

    function calculatePrice(){
        var price = Math.round(Number($("#price").val()) * 100);
        var sessions = Number($("#sessions").val());
        price = price*sessions;

        
        if($("#discount_type").val()=='1'){
            var discount = Math.round(Number($("#discount").val()) * 100); // multiplica por 100 pra ficar em centavos
            $("#final_price").val(((price - discount)/100).toFixed(2));
            $("#price1").val(((price - discount)/100).toFixed(2));
        } else {
            var discount = Number($("#discount").val()) / 100;  // divide por 100 pra ficar em porcentagem
            $("#final_price").val(((price-(price*discount))/100).toFixed(2));
            $("#price1").val(((price-(price*discount))/100).toFixed(2));
        }
    }
});