$(document).ready(function() {
    const supplierSelect = $("#supplier").select2();

    $('#cost').inputmask("numeric", {
      radixPoint: ",",
      groupSeparator: ",",
      digits: 2,
      autoGroup: true,
      prefix: 'R$ ',
      placeholder: "0"
    });

    if($("#Recorrencia").val()=="True"){
        document.getElementById("qtd_div").style.visibility = "visible";
        document.getElementById("rec_div").style.visibility = "visible";

        document.getElementById("Prazo").setAttribute("required", true);
        document.getElementById("Qtd").setAttribute("required", true);
    }
});

window.onload = (event) => {
    
}

function cancelCreation(e){  
    if(confirm("Tem certeza que deseja cancelar a edição?")==true) history.back();
}

function changeView(e){
    console.log(e.target.getAttribute("value") == "True")
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
