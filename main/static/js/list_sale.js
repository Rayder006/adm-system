$(document).ready( function () {
    $('#table').DataTable({
        scroller:true,
        scrollY:400,
        responsive:true,
        select: {
            style: 'multi+shift'
        },
        colReorder: false,
        searchBuilder: {
            depthLimit: 2
        },
        dom: 'Bfrtip',
        columnDefs: [
            {
                targets: [1,2,3,7,8,9], // Índice da coluna de data (começando em 0)
                type: 'string', // Define o tipo de dados como "string"
            },
            {
                targets: [4,5], // Índice da coluna de data (começando em 0)
                type: 'number', // Define o tipo de dados como "string"
            },
            {
                targets:[6],
                type : "number",
                render: function(data, type) {
                    console.log(data)
                    if (type === 'display') {
                        const formCurrency = new Intl.NumberFormat('pt-BR', {
                            style: 'currency',
                            currency: 'BRL',
                            minimumFractionDigits: 2
                        })
                        return formCurrency.format(parseFloat(data.replace(',', '.')));
                    }
                    return data;
                }
            },
            {
                targets:[10],
                orderable:false
            },
            {
                targets:[0],
                type:'date',
                render: function(data, type){
                    let date = new Date(`${data}T00:00:00`);
                    if(type=="display"){
                        return `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth()+1).padStart(2, '0')}/${date.getFullYear()}`;
                    }
                    return data;
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
                title:"Vendas",
                key: {
                    key:'c',
                    altKey:true
                },
                exportOptions: {
                    columns: ':not(.export-hidden)' // Ignora as colunas com a classe "class="export-hidden""
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
});

function contract(e){
    console.log(e.getAttribute("data-url"));
    if(confirm("Tem certeza que deseja emitir este Contrato?\nApós a emissão, esta venda não poderá mais ser editada!")==true){
        window.open(e.getAttribute("data-url"), "_blank");
        window.location.reload();
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