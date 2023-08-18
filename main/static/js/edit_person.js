$(document).ready(function() {
    $('#CPF').inputmask();
    // $('#Telefone').inputmask();
    $('#Celular').inputmask();
    $("#CEP").inputmask("99999-999");
});

function cancelEdit(e){
    e.preventDefault();
    if(confirm("Tem certeza que deseja cancelar a edição?")==true){
        history.back();
    }
}