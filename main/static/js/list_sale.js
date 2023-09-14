$(document).ready( function () {
    $('#table').DataTable({
        scroller:true,
        scrollY:400,
        scrollX:true,
        scrollx:true,
        responsive:true,
        select: {
            style: 'multi+shift'
        },
        colReorder: true,
        searchBuilder: {
            depthLimit: 2
        },
        dom: 'Bfrtip',
        columnDefs: [
            {
                targets: [1,2,3,5,6,7], // Índice da coluna de data (começando em 0)
                type: 'string', // Define o tipo de dados como "datetime"
            },
            {
                targets:[8],
                orderable:false
            },
            {
                targets:[0],
                type:'date',
                render: function(data, type){
                    let partes = data.split('-');
                    let fusoHorarioLocal = new Date().getTimezoneOffset() / 60;

                    let date = new Date(Date.UTC(parseInt(partes[0]), parseInt(partes[1]) - 1, parseInt(partes[2]), fusoHorarioLocal));
                    if(type=="display"){
                        console.log("String: " + data + "\nObjeto Date: " + date);
                        const day = String(date.getDate()).padStart(2, '0');
                        const month = String(date.getMonth() + 1).padStart(2, '0'); // Mês é base 0
                        const year = date.getFullYear();
                        return `${day}/${month}/${year}`;
                    }
                    return date.getTime();
                }
            }
        ],
        buttons:[
            {
                extend: 'searchBuilder'
            },
            {
                extend: "excelHtml5",
                text: "Excel",
                title:"Teste",
                key: {
                    key:'c',
                    altKey:true
                }
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

    // $(".cancelButton").on(
    //     "click", function (e) {
    //         console.log(e);
    //         cancelSale()
    //     }
    // )
});

function contract(e){
    console.log(e.getAttribute("data-url"));
    if(confirm("Tem certeza que deseja emitir este Contrato?\nApós a emissão, esta venda não poderá mais ser editada!")==true){
        window.open(e.getAttribute("data-url"), "_blank");
        return window.location.reload();
    }
}

function deleteSale(e){
    console.log(e);
    if(confirm("Tem certeza que deseja deletar o registro da venda?\nISSO NÃO PODE SER REVERTIDO!") == true){
        document.getElementById("deleteForm-" + e.getAttribute("s_pk")).submit();
    }
    
}

function cancelSale(e){
    console.log(e)
    if(confirm("Tem certeza que deseja cancelar a Venda?")==true){
        $.ajax({
            url: e.getAttribute("data-url"), // Substitua pela URL correta
            type: 'POST',
            headers: {
                "X-CSRFToken": e.getAttribute("data-csrf") // Inclui o token CSRF no cabeçalho
            },
            dataType: "json", // Especifica o tipo de dados esperado na resposta
            success: function(data) {
                console.log(data); // Exibe a resposta da view
                window.location.reload();
                // Atualize a tabela ou realize outras ações após marcar as contas como pagas
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText); // Exibe detalhes do erro
            }
        });
    }
}

function renderData(data, type, row){
    console.log("data:", data)
    console.log("type:", type)
    console.log("row:", row)
}