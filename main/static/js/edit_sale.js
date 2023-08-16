window.onload= (e) => {
    let discount_type;
    let currentType= document.getElementById("sale_type").value;
    var change = new Event('change');

    document.getElementById(currentType).hidden=false;

        //Event Handlers
    document.getElementById("plan").addEventListener(
        "change", function () {
            selectService(event)
        }
    )
    document.getElementById("service").addEventListener(
        "change", function () {
            selectService(event)
        }
    )
    document.getElementById("product").addEventListener(
        "change", function () {
            selectService(event)
        }
    )

    document.getElementById("sale_type").addEventListener(
        "change", function() {
            changeSaleType(event)
        }
    )

    document.getElementById("discount").addEventListener(
        "change", function() {
            priceCalc(e)
        }
    )

    document.getElementById("sessions").addEventListener(
        "change", function() {
            priceCalc(e)
        }
    )

    document.getElementById("discount_type").addEventListener(
        "change", function() {
            priceCalc(e)
        }
    )

    document.getElementById("price").addEventListener(
        "change", function() {
            priceCalc(e)
        }
    )

        //Funções
    function selectService(e){
        document.getElementById("price").setAttribute("value", document.getElementById(`${currentType}${e.target.value}`).getAttribute("data-price"))
        document.getElementById("sessions").setAttribute("value", document.getElementById(`${currentType}${e.target.value}`).getAttribute("data-sessions"))
        document.getElementById("price").dispatchEvent(change)
    }

    function changeSaleType(e){
        console.log("Teste")
        document.getElementById(currentType).hidden=true;
        document.getElementById(e.target.value).hidden=false
        currentType = e.target.value;
        if(currentType=="3") document.getElementById("sessions_label").innerHTML="Quantidade*"
        else document.getElementById("sessions_label").innerHTML="Qtd. de Sessões*"
    }

    function priceCalc(e){
        console.log("AA")
        if(currentType==1) price = document.getElementById("price").value
        else price = document.getElementById("price").value * document.getElementById("sessions").value;
        discount = document.getElementById("discount").value;
        discount_type = document.getElementById("discount_type");

        if(discount){
            if(discount_type.value == "percent"){
                final_price = Number(price-(discount*price)/100).toFixed(2)
            } else if(discount_type.value == "real"){
                final_price=price-discount;
            } 
            document.getElementById("final_price").value = final_price;
        }
    }
}

function cancelEditing(e){
    if(confirm("Tem certeza que deseja cancelar a edição?")==true){
        history.back();
    }
}