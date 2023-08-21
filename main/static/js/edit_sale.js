window.onload = (e) => {
    let discount_type = "1"; 
    let currentType= document.getElementById("sale_type").value;
    var change = new Event('change');
    let is_taxSelect =false;
    const options = [];
    const paymentSelect = $("#payment_type").select2();
    const taxSelect = $("#tax").select2();
    // const clientSelect = $("#client").select2();
    // const sellerSelect = $("#seller").select2();
    // const originSelect = $("#sale_origin").select2();

    

        //Initializers
    document.getElementById(currentType).hidden=false;

        //Event Handlers
    $("#payment_type").on(
        "change", function () {
            console.log()
            if($("#payment_type").find(':selected').data('tax')=="True"){
                $("#taxDiv").attr("hidden", false);
                if(!is_taxSelect) $("#tax").select2();
                $("#tax").select2('open');
                if($("#payment_type").val()==1) $(".select2-search__field").val("Crédito")
                else $(".select2-search__field").val("Débito")
                is_taxSelect = true;
            } 
            else {
                $("#taxDiv").attr("hidden", true);
                $("#tax").val(null);
                if(is_taxSelect) $("#tax").select2('destroy');
                is_taxSelect = false;
            }
        }
    )

    $("#tax").change(function () {
            if($(this).find(':selected').data('id')!=$("#payment_type")[0].value && $(this).val()){
                console.log($(this).find(':selected'))
                console.log($("#payment_type")[0].value)
                alert("Esta taxa não pertence à forma de pagamento selecionada")
                $("#tax").val(null).trigger('change');
            }
        }
    )
    


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
        document.getElementById("price").value= document.getElementById(`${currentType}${e.target.value}`).getAttribute("data-price")
        document.getElementById("sessions").value= document.getElementById(`${currentType}${e.target.value}`).getAttribute("data-sessions")
        if(e.target.id=="plan") document.getElementById("sessions").readOnly=true 
        else document.getElementById("sessions").readOnly=false;
        priceCalc();
    }

    function changeSaleType(e){
        document.getElementById(currentType).hidden=true;
        document.getElementById(currentType).querySelector("select").required=false;
        document.getElementById(currentType).querySelector("select").value="";
        document.getElementById(e.target.value).hidden=false;
        document.getElementById(e.target.value).querySelector("select").required=true;
        currentType = e.target.value;
        
        if(currentType=="3") document.getElementById("sessions_label").innerHTML="Quantidade*"
        else document.getElementById("sessions_label").innerHTML="Qtd. de Sessões*"

        document.getElementById(e.target.value).querySelector("select").dispatchEvent(change);

        document.getElementById(currentType).querySelector("select").value=""
    }

    function priceCalc(e){
        if(currentType==1) price = document.getElementById("price").value
        else price = document.getElementById("price").value * document.getElementById("sessions").value;
        discount = document.getElementById("discount").value;
        discount_type = document.getElementById("discount_type");

        if(discount){
            if(discount_type.value == "percent"){
                final_price = Number(price-(discount*price)/100).toFixed(2)
            } else if(discount_type.value == "real"){
                final_price=Number(price-discount).toFixed(2);
            } 
            document.getElementById("final_price").value = final_price;
        }
    }

    function cancelEditing(e){
        if(confirm("Tem certeza que deseja cancelar a edição?")==true){
            history.back();
        }
    }
}