$(document).ready( function () {
    $('#table').DataTable({
        scroller:true,
        scrollY:400,
        select: {
            style: 'multi+shift'
        },
        colReorder: true,
        searchBuilder: {
            depthLimit: 2
        },
        dom: 'Bfrtip',
        buttons:[
            {
                extend: 'searchBuilder'
            },
            {
                extend: "copy",
                text: "Copiar",
                key: {
                    key:'c',
                    altKey:true
                }
            },
            {
                extend: "excelHtml5",
                text: "Excel",
                title:"Teste"
            },
            {
                extend: "print",
                text: "Imprimir",
            }
        ],
        search: {
            "smart" : false,
            "regex":true
        },
        stateSave: true,
        language: {
            "emptyTable":     "Não há dados disponíveis",
            "info":           "Mostrando _START_-_END_ de _TOTAL_ linhas",
            "infoEmpty":      " 0-0 de 0 linhas",
            "infoFiltered":   "",
            "infoPostFix":    "",
            "thousands":      ".",
            "lengthMenu":     "Mostrar _MENU_ linhas",
            "loadingRecords": "Carregando...",
            "processing":     "",
            "search":         "Procurar:",
            "zeroRecords":    "Nenhum registro correspondente encontrado",
            "paginate": {
                "first":      "Primeiro",
                "last":       "Ultimo",
                "next":       "Próx.",
                "previous":   "Ant."
            },
            "searchBuilder": {
                "add": '+',
                "button": 'Filtros',
                "clearAll": 'Limpar',
                "condition": 'Condição',
                "data": 'Coluna',
                "value": 'Valor',
                "logicAnd": 'And',
                "logicOr": 'Or',
                "title":"Filtros Avançados",
                
            },
            "select": {
                "rows": {
                    _: "%d linhas selecionadas",
                    1: "1 linha selecionada"
                }
            }
        }
    });
});



function deleteInvoice(e){
    console.log(e);
    if(confirm("Tem certeza que deseja deletar o Lançamento?") == true){
        document.getElementById("deleteForm-" + e.getAttribute("i_pk")).submit();
    }
    
}