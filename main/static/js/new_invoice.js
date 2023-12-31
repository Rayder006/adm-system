$(document).ready(function() {
    const saleTypeSelect = $("#TipoConta").select2();
    const supplierSelect = $("#supplier").select2();
    
    $('#cost').inputmask("numeric", {
      radixPoint: ",",
      groupSeparator: ",",
      digits: 2,
      autoGroup: true,
      prefix: 'R$ ',
      placeholder: "0"
    });
});

function changeView(e){
    console.log(e);
    if(e.target.value=="True"){
        document.getElementById("qtd_div").style.visibility = "visible";
        document.getElementById("rec_div").style.visibility = "visible";

        document.getElementById("Prazo").setAttribute("required", true);
        document.getElementById("Qtd").setAttribute("required", true);
    }else{
        document.getElementById("qtd_div").style.visibility = "hidden";
        document.getElementById("rec_div").style.visibility = "hidden";

        document.getElementById("Prazo").removeAttribute("required");
        document.getElementById("Qtd").removeAttribute("required");
    }
}

function cancelCreation(e){
    if(confirm("Tem certeza que deseja cancelar o cadastro?")==true){
        history.back();
    }
}