// $(document).ready(function(){
//     console.log("teste")
//     IMask(document.getElementById("Telefone"), { mask : '0000-0000' });
//     IMask(document.getElementById("Celular"), { mask : '(00) 90000-0000' });
// });



function cancelEdit(e){
    e.preventDefault();
    if(confirm("Tem certeza que deseja cancelar a edição?")==true){
        history.back();
    }
}