$(document).ready( function () {
    let table = $('#table').DataTable({
        scrollX: true,
        scroller:true,
        responsive:true,
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
                },
                exportOptions: {
                    columns: ':not(.acoes)' // Ignora as colunas com a classe "acoes"
                }
            },
            {
                extend: "excelHtml5",
                text: "Excel",
                title:"Teste",
                exportOptions: {
                    columns: ':not(.acoes)' // Ignora as colunas com a classe "acoes"
                }
            },
            {
                extend: 'collection',
                text: 'Opções',
                buttons: [
                    {
                        text: 'Pagar',
                        action: function ( e, dt, node, config ) {
                            let pass = false; 
                            var dados = table.rows({ selected: true });
                            let payment_date = window.prompt("Insira a data de pagamento referente:\n\t(dd/mm/AA)\n\tDeixe em branco para hoje");
                            if(payment_date!=null){
                                dados = dados.data();
                                ids = []
                                dados.each(function(data) {
                                    if(data[7]=="Sim" || !pass){
                                        if(confirm("Uma ou mais dessas contas já está paga. Deseja alterar a data?")==false) return;
                                        else pass=true;
                                    }
                                    ids.push(data[9])
                                });
                                payInvoiceFunction(ids, payment_date);
                            }
                        }
                    }
                ]
            }
        ],
        search: {
            "smart" : false,
            "regex":true
        },
        "columns": [
            { "type": "string" }, //ID
            { "type": "string" }, //Tipo
            {                     //Valor
                "type" : "number",
                "render": function(data, type, row) {
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
            { "type": "string" },   //Fornecedor                  
            {                       //Lançamento
                "type":"date",
                "render": function(data,type,row){
                    if(type==="display"){
                        return data;
                    };
                    return new Date(data);
                }
            }, 
            {                   //Vencimento
                "type":"date",
                "render": function(data,type,row){
                    if(type==="display" || type ==="filter"){
                        return data;
                    }
                    let date = new Date(data);
                    return date;
                }
            },  
            {                  //Pagamento
                "type":"date",
                "render": function(data,type,row){
                    if(type==="display" || type ==="filter"){
                        return data;
                    }
                    let date = new Date(data);
                    return date;
                }
            },  
            { "type": "string" }, //A Pagar?
            { "orderable":false }, //Ações
            null
        ],
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

function payInvoiceFunction(ids, payment_date) {
    $.ajax({
        url: payInvoices, // Substitua pela URL correta
        type: 'POST',
        headers: {
            "X-CSRFToken": csrfToken // Inclui o token CSRF no cabeçalho
        },
        data: {
            ids: ids,
            payment_date: payment_date
        },
        dataType: "json", // Especifica o tipo de dados esperado na resposta
        success: function(data) {
            console.log(data); // Exibe a resposta da view
            // Atualize a tabela ou realize outras ações após marcar as contas como pagas
            window.location.reload();
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Exibe detalhes do erro
        }
    });
}




function deleteInvoice(e){
    if(confirm("Tem certeza que deseja deletar o Lançamento?") == true){
        document.getElementById("deleteForm-" + e.getAttribute("i_pk")).submit();
    }
    
}