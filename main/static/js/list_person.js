$(document).ready( function () {
    $('#table').DataTable({
        scroller:true,
        scrollY:400,
        scrollX:true,
        scrollx:true,
        select: true,
        colReorder: true,
        searchBuilder: {
            depthLimit: 2
        },
        dom: 'Bfrtip',
        buttons:[
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
            }
        ],
        columnDefs:[
            {"targets":4, orderable:false}
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



function deletePerson(e){
    if(confirm(`Tem certeza que deseja deletar o cadastro de ${e.getAttribute("p_name")}?`) == true){
        console.log(document.getElementById("deleteForm-" + e.getAttribute("p_pk")))
        console.log("deleteForm-" + e.getAttribute("p_pk"));
        document.getElementById("deleteForm-" + e.getAttribute("p_pk")).submit();
    }
}