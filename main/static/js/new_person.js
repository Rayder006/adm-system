$(document).ready(function() {
    $('#CPF').inputmask();
    // $('#Telefone').inputmask();
    $('#Celular').inputmask();
    $("#CEP").inputmask("99999-999");
});

function cancelCreation(e){
    if(confirm("Tem certeza que deseja cancelar o cadastro?")==true){
        history.back();
    }
}