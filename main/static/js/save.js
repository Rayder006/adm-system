window.onload = (e) => {
    let discount_type = "1"; 
    let currentType= "1";
    var change = new Event('change');
    let is_taxSelect1 =false;
    let is_taxSelect2 =false;
    const options = [];
    const paymentSelect = $("#payment_type").select2();
    const taxSelect = $("#tax").select2();
    // const clientSelect = $("#client").select2();
    // const sellerSelect = $("#seller").select2();
    // const originSelect = $("#sale_origin").select2();

        //Initializers
    document.getElementById("sale_type").value="1"
    
    


        //Event Handlers
    $("#final_price").on(
        "change", function (e){
            if($("#mixed").val()=="True"){
                $("#price2").val(Number($("#final_price").val())-Number($("#price1").val()));
            } else {
                $("#price2").val(0);
                $("#price1").val($("#final_price").val());
            }
        }
    )
    
    $("#price1").on(
        "change", function (e) {
            $("#price2").val(Number($("#final_price").val())-Number($("#price1").val()))
        }
    )

    $("#form").on(
        "submit", function (event){
            if(Number($("#price1")) + Number($("#price2"))!=Number($("#final_price"))){
                if(window.confirm("Preço diferente do preço final. Deseja Continuar?")==false) return false
            }
        }
    )

    $("#mixed").on(
        "change", function (e) {
            if(e.currentTarget.value=="True") {
                $("#paymentDiv2")[0].hidden = false
                $("#payment_type2").select2();
                $("#payment_type2")[0].required = true
                $("#price1").attr("readonly", false)
            } else {
                $("#paymentDiv2")[0].hidden = true
                $("#payment_type2")[0].required = false
                $("#payment_type2")[0].value = ""
                $("#tax2")[0].value = ""
                $("#price2")[0].value = "0"
                $("#installments2")[0].value = "1"
                $("#payment_type2").select2('destroy');
                $("#price1").attr("readonly", true)
                $("#price1").val($("#final_price").val())
                $("#price1").trigger("change");
            }
        }
    )

    $("#payment_type2").on(
        "change", function () {
            console.log()
            if($("#payment_type2").find(':selected').data('tax')=="True"){
                $(".taxDiv2").attr("hidden", false);
                $(".taxDiv2").attr("required", true)
                if(!is_taxSelect2) $("#tax2").select2();
                $("#tax2").select2('open');
                if($("#payment_type2").val()==1) $(".select2-search__field").val("Crédito")
                else $(".select2-search__field").val("Débito")
                $("#installments2")[0].val(1);
                is_taxSelect2 = true;
                $("#installments2")[0].required = true
            } 
            else {
                $(".taxDiv2").attr("hidden", true);
                $(".taxDiv2").attr("required", false)
                $("#tax2").val(null);
                $("#installments2").val(null);
                if(is_taxSelect2) $("#tax2").select2('destroy');
                is_taxSelect2 = false;
                $("#installments2")[0].required = false
            }
        }
    )

    $("#payment_type").on(
        "change", function () {
            console.log()
            if($("#payment_type").find(':selected').data('tax')=="True"){
                $(".taxDiv").attr("hidden", false);
                if(!is_taxSelect1) $("#tax").select2();
                $("#tax").select2('open');
                if($("#payment_type").val()==1) $(".select2-search__field").val("Crédito")
                else $(".select2-search__field").val("Débito")
                $("#installments").val(1);
                is_taxSelect1 = true;
                $("#installments")[0].required = true
            } 
            else {
                $(".taxDiv").attr("hidden", true);
                $("#tax").val(null);
                $("#installments").val(null);
                if(is_taxSelect1) $("#tax").select2('destroy');
                is_taxSelect1 = false;
                $("#installments")[0].required = false
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
        if($("#mixed").val()=="False") {
            $("#price1").val($("#final_price").val());
            $("#price1").trigger("change");
        }
        else $("#price2").val(Number($("#final_price"))-Number($("#price1").val()))
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
        if(currentType=="1") $("#sessions").attr("readonly", true) 
        else $("#sessions").attr("readonly", false) 
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
            $("#final_price").trigger("change")
        }
    }
}