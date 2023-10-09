$(document).ready(function() {

    $("#installments2").on('change', function(){
        if($(this).val()>12) $(this).val(12);
        if($(this).val()<1) $(this).val(1);
    });

    $("#installments").on('change', function(){
        if($(this).val()>12) $(this).val(12);
        if($(this).val()<1) $(this).val(1);
    });

    $("#price1").on('change', function(){
        $("#price2").val(($("#final_price").val() - $(this).val()).toFixed(2));
    });

    $("#payment_type2").on('change', function(){
        $("#tax2").val(null);
        if($(this).find(":selected").data('tax')=="True"){
            $(".taxInput2").attr('required', true).closest('div').show();
            $("#tax2 option").each(function(){
                $(this).toggle($(this).data('type')==$("#payment_type2").val())
            })
        } else {
            $(".taxInput2").attr('required', false).closest('div').hide();
            $("#tax2").val(null);
            $("#installments2").val(1);
        }
    });

    $("#payment_type").on('change', function(){
        $("#tax").val(null);
        if($(this).find(":selected").data('tax')=="True"){
            $(".taxInput").attr('required', true).closest('div').show();
            $("#tax option").each(function(){
                $(this).toggle($(this).data('type')==$("#payment_type").val())
            })
        } else {
            $(".taxInput").attr('required', false).closest('div').hide();
            $("#tax").val(null);
            $("#installments").val(1);
        }
    });

    $("#mixed").on('change', function(){
        if($(this).val()!=1){
            $(".payment2").val(null).hide();
            $(".taxInput2").attr('required', false).closest('div').hide();
        } else {
            $(".payment2").val(null).show();
        }
        $("#price1").attr('readOnly', $(this).val()!=1);
        $("#sessions").trigger('change');
    });

    $("#price").on("change", function(){
        $("#discount").trigger('change');
    });

    $("#discount_type").on('change', function(){
        if($(this).val()=="2"){
            $("#discount").attr('max', 100);
        } else {
            $("#discount").attr('max', ($("#price").val() * $("#sessions").val()));
        }
        console.log("Max: " + $("#discount").attr('max'));
        $("#discount").trigger('change');
    });

    $("#discount").on('change', function(){
        if($(this).val() < 0 || !($(this).val())) $(this).val(0);
        if($(this).val() > Number($(this).attr('max'))){
            $(this).val($(this).attr('max'));
        }
        
        $("#sessions").trigger('change');
    });

    $("#sessions").on('change', function(){
        if($(this).val()<0 || !($(this).val())) $(this).val(0);
        if($("#discount_type").val()==1){
            $("#final_price").val((($("#price").val() * $(this).val()) - $("#discount").val()).toFixed(2));
        } else {
            let total = $("#price").val() * $(this).val();
            let discount = $("#discount").val();
            discount = (total * discount)/100;
            $("#final_price").val((total-discount).toFixed(2));
        }
        if($("#final_price").val()< 0) $("#final_price").val(0);
        $("#price1").val($("#final_price").val()).trigger('change');
    });

    $("#service").on('change', function(){
        $("#price").val(Number($(this).find(":selected").data('price').replace(',', '.')).toFixed(2));
        $("#sessions").val(Number($(this).find(":selected").data('sessions')));
        $("#discount_type").trigger('change');
    });

    $("#sale_type").on('change', function(){
        $("#sessions").attr('readOnly', ($(this).val()==1 || $(this).val()==4))
        $("#service_label").text(`${$(this).find(':selected').text()}*`)
        $("#service option").each(function(){
            if($(this).data('type')==$("#sale_type").val()) $(this).show();
            else $(this).hide();
        });
        $("#price").val(null);
        $("#service").val(null);
        $("#sessions").val(null).trigger('change');        
    });
});