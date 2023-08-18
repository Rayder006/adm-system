$(document).ready(function() {
    $('#CPF').inputmask();
    $('#Telefone').inputmask();
    $('#Celular').inputmask();
});

function cancelCreation(e){
    if(confirm("Tem certeza que deseja cancelar o cadastro?")==true){
        history.back();
    }
}