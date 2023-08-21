$(document).ready(function() {
    $('#CPF').inputmask();
    // $('#Telefone').inputmask();
    $('#cellphone').inputmask();
    $("#cep").inputmask("99999-999");
});

function cancelEdit(e){
    e.preventDefault();
    if(confirm("Tem certeza que deseja cancelar a edição?")==true){
        history.back();
    }
}