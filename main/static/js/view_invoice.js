function deleteInvoice(e){
    if(confirm("Tem certeza que deseja apagar o registro de Lançamento?")==true){
        document.getElementById("deleteForm").submit();
    }
}