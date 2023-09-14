window.onload = (e) => {
  const radios = document.querySelectorAll('input[name="viewRadio"]')
  const creationModal = new bootstrap.Modal(document.getElementById('creationModal'), {backdrop:'static'})
  const Calendar = tui.Calendar;
  const container = document.getElementById('calendar');
  const events = JSON.parse(document.getElementById('event_list').textContent); 
  const services = JSON.parse(document.getElementById('service_list').textContent); 
  const events_map = new Map();
  const service_map = new Map();
  const eventList = [];
  const serviceSelect2 = $("#service").select2({dropdownParent: $('#creationModal')});
  const meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho" , "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
  const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'))
  const calendar = new Calendar(container, {
    defaultView: 'week',
    week:{
        startDayOfWeek: 0,
        dayNames: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
        narrowWeekend: false,
        workweek: false,
        showNowIndicator: true,
        showTimezoneCollapseButton: false,
        timezonesCollapsed: false,
        hourStart: 6,
        hourEnd: 22,
        eventView: ['time'],
        taskView: false,
        collapseDuplicateEvents: false,
        allDay:false
      },
    month:{
      dayNames: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
      visibleWeeksCount: 0,
      workweek: false,
      narrowWeekend: false,
      startDayOfWeek: 0,
      isAlways6Weeks: true,
      visibleEventCount: 6,
    },
    useCreationPopup: false,
    useDetailPopup: false,
  });
  var lastEdit;

    //Inicializa a datatable de confirmação 
  let table = $('#confirmTable').DataTable({
    orderable:false,
    dom: 't',
    select: {
      style: 'multi+shift'
    },
  });
  if(table.rows().data().length > 0)confirmModal.show();

    //carrega os eventos do Banco de Dados
  for (const event of events) {
    events_map.set(event.id, event)
    console.log(event);
    var color;
    switch(event.title){
      case "Pilates":
        color="#FFFF00"
        break;
      case "Facial":
        color="#0000FF"
        break;
      case "Corporal":
        color="#008000"
        break;
      case "Injetáveis":
        color="#FF0000"
        break;
      case "Cortesia":
        color="#FFA500"
        break;
      case "Avaliação":
        color="#800080"
        break;
      default:
        color="#FFC0CB"
    }

    const eventObject = {
      id: event.id,
      title: event.client,
      start: `${event.date}T${event.start}`,
      end: `${event.date}T${event.end}`,
      backgroundColor:color
    };
    eventList.push(eventObject);
  }
  calendar.createEvents(eventList);
  console.table(eventList);
    //inicializa a mascara de celular
  $('#phone').inputmask();

    //Popula o map de serviços
  for (i=0;i<services.length;i++) {
    console.log(services[i])
    service_map.set(services[i].pk, services[i].name)
  }

    //Adiciona o nome do mês na página
  document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;


    //Event Handlers
  $("#confirmButton").on(
    "click", function (e){
      var dados = table.rows({ selected: true }).data();
      var ids= []
      console.log(dados)
      dados.each(function (data) {
        ids.push(data[0]);
      });
      if(ids.length==0) {
        confirmModal.hide();
        return;
      }

      $.ajax({
        url:"confirm/",
        method:"POST",
        headers: {
          "X-CSRFToken": csrf_token // Inclui o token CSRF no cabeçalho
        },  
        data: {
          ids:ids
        },
        dataType:"json",
        success: function(data){
          window.location.reload();
        },
      })
    }
  )

  document.getElementById("client").addEventListener(
    "change", (e) => {
      console.log("carregando vendas do cliente: " + e.target.options[e.target.selectedIndex].textContent)
      $.ajax({
        url:"service_filter/" + e.target.value,
        method:"GET",
        dataType:"json",
        success: function(data){
          console.log(data)
          $("#service").empty()
          data.forEach(item => {
            option = new Option(item.service, item.service_id, false, false);
            $(option).attr('data-sale-id', item.sale_id);
            $('#service').append(option);
          });

          $('#service').append(new Option("Avaliação", -1));
          $('#service').append(new Option("Cortesia", -2));
        },
         error: function (data) {
          console.log("Erro" + data);

          $("#service").empty()
          $('#service').append(new Option("Avaliação", -1));
          $('#service').append(new Option("Cortesia", -2));
         }
      })
      console.log(e.target.options[e.target.selectedIndex])
      $("#_client").val(e.target.options[e.target.selectedIndex].textContent)
      $("#phone").val(e.target.options[e.target.selectedIndex].getAttribute("data-phone"))
    }
   )

  document.getElementById("clientCheck").addEventListener(
    "change", (e) => {
      if(e.target.checked){
        document.getElementById("_client-div").hidden=false;
        document.getElementById("client-div").hidden=true;
        document.getElementById("_client").required= true;
        document.getElementById("client").required= false;
        document.getElementById("client").value= null;
        document.getElementById("_client").value= null;
        document.getElementById("phone").readOnly = false;
        document.getElementById("phone").value= null;
        document.getElementById("client").dispatchEvent(new Event("change"));
      } else {
        document.getElementById("phone").readOnly=true;
        document.getElementById("_client-div").hidden=true;
        document.getElementById("client-div").hidden=false;
        document.getElementById("_client").required= false;
        document.getElementById("_client").value = null;
        document.getElementById("client").required= true;
        document.getElementById("client").value="";
        document.getElementById("client").dispatchEvent(new Event("change"));
      }
    }
  )


  document.getElementById("prev").addEventListener(
    "click", (e) => {
      calendar.prev()
      document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;
    }
  )
  document.getElementById("next").addEventListener(
    "click", (e) => {
      calendar.next()
      document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;
    }
  )
  document.getElementById("today").addEventListener(
    "click", (e) => {
      calendar.today()
      document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;
    }
  )

  for(let i=0;i<radios.length;i++){
    radios[i].addEventListener("change", (e) =>{
      console.log(e.target.value)
      console.log(document.getElementById("month"))
      calendar.changeView(e.target.value)
      document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;
    })
  }

  document.getElementById("deleteButton").addEventListener(
    "click", (e) => {
      if(confirm("Tem certeza que deseja deletar o agendamento?")==true){
        document.getElementById("modalForm").setAttribute("action", `${document.getElementById("modalForm").getAttribute("edit-url")}${lastEdit}/`);
        document.getElementById("modalForm").submit();
      }
    }
  )

  document.getElementById("submitCreation").addEventListener(
    "click", (e) => {
      console.log(document.getElementById("modalForm").getAttribute("action"))
      const requiredInputs = document.getElementById("modalForm").querySelectorAll("input[required], select[required]");

      // Verifique se todos os campos required estão preenchidos
      for (const input of requiredInputs) {
        if (!input.value.trim()) {
            alert("Por favor, preencha todos os campos obrigatórios: " + input.getAttribute("name"));
            e.preventDefault(); // Impede o envio do formulário
            return;
          }
      }

      const sale_input = document.createElement("input");
      sale_input.setAttribute("type", "hidden");
      sale_input.setAttribute("name", "sale");
      sale_input.setAttribute("value", $("#service").find(":selected").data("sale-id"));

      document.getElementById("modalForm").appendChild(sale_input);

      document.getElementById("modalForm").submit();
    });

  calendar.on({
    'selectDateTime': function teste(e) {  
      console.log(Date(e.start))  
      openCreationModal(e, "create");
    },
    'clickEvent': (event) => {
        openCreationModal(event, "edit");
    },
    'beforeUpdateEvent': function(e) {
        console.log('beforeUpdateEvent', e);
        if(confirm("Tem certeza que deseja alterar o agendamento?")==true){
          (e.changes.start) ? e.event.start = e.changes.start : {};
          (e.changes.end) ? e.event.end = e.changes.end : {};
          calendar.updateEvent(e.event.id, e.event.calendarId, e.event);

        }
    },
    'beforeDeleteSchedule': function(e) {
        console.log('beforeDeleteSchedule', e);
        calendar.deleteSchedule(e.schedule.id, e.schedule.calendarId);
    }
  });

  document.getElementById("creationModal").addEventListener(
    "hidden.bs.modal", function (event) {
      document.getElementById("modalForm").reset();
    }
  )

  //Funções
  function openCreationModal(e, isCreation){
    if(isCreation==="create"){
      $("#status").empty()
      $("#status").append($("<option>", {value: "1", text: "Novo"}))
      document.getElementById("modalForm").setAttribute("action", document.getElementById("modalForm").getAttribute("create-url"));

      document.getElementById("primaryFooter").hidden=false;
      document.getElementById("secondaryFooter").hidden=true;

      document.getElementById("date").readOnly = false;
      document.getElementById("start").readOnly = false;
      document.getElementById("end").readOnly = false;
      document.getElementById("obs").readOnly = false;
      document.getElementById("room").readOnly = false;
      document.getElementById("_client").readOnly = false;
      document.getElementById("_client-div").hidden = true;
      document.getElementById("client-div").hidden = false;
      document.getElementById("clientCheck").removeAttribute("disabled", '');
      document.getElementById("equipment").removeAttribute("disabled");
      document.getElementById("status").removeAttribute("disabled");
      document.getElementById("professional").removeAttribute("disabled");
      document.getElementById("client").removeAttribute("disabled");
      document.getElementById("service").removeAttribute("disabled");
      document.getElementById("phone").value="";

      let start = new Date(e.start)
      let end = new Date(e.end)
      let year = String(start.getFullYear());
      let month = start.getMonth()+1;
      let day = start.getDate();

      let start_time = `${start.getHours()}:${start.getMinutes()}`
      let end_time = `${end.getHours()}:${end.getMinutes()}`

      if(start.getHours()<10) start_time=`0${start_time}`;
      if(end.getHours()<10) end_time=`0${end_time}`;
      if(start.getMinutes()==0) start_time=`${start_time}0`;
      if(end.getMinutes()==0) end_time=`${end_time}0`;

      (month<10) ? month = `0${month}` : month = String(month);
      (day<10) ? day = `0${day}` : month = String(month);

      document.getElementById("date").setAttribute("value", year+'-'+month+'-'+day);
      document.getElementById("start").setAttribute("value", start_time)
      document.getElementById("end").setAttribute("value", end_time)

    } 
    else if (isCreation==="edit"){
      $("#status").empty()
      lastEdit = e.event.id;
      e = events_map.get(e.event.id);
      console.log(e)
      document.getElementById("primaryFooter").hidden=true;
      document.getElementById("secondaryFooter").hidden=false;

      document.getElementById("equipment").value = e.equipment_id;
      if(e.status=="1"){
        document.getElementById("status").append(new Option("Novo", 1, true, true))
        document.getElementById("status").value = 1;
      } else {
        document.getElementById("status").append(new Option("Confirmado", 2, true, true))
        document.getElementById("status").value = 2;
      }
      
      document.getElementById("professional").value= e.professional_id;
      document.getElementById("client-div").hidden= true;
      document.getElementById("_client-div").hidden= false;
      document.getElementById("_client").readOnly= true;
      document.getElementById("_client").value= e.client;
      document.getElementById("service").value= e.service_id;
      console.log(service_map.get(e.sale_id))
      if(service_map.get(e.sale_id)) {
        $('#service').append(new Option(service_map.get(e.sale_id), null, true, true));
      } else {
        console.log(e.is_courtesy);
        (e.is_courtesy) ? $('#service').append(new Option("Cortesia", -2, true, true)) : $('#service').append(new Option("Avaliação", -1, true, true)); 
      }
      document.getElementById("date").setAttribute("value", e.date);
      document.getElementById("start").setAttribute("value", e.start);
      document.getElementById("end").setAttribute("value", e.end);
      document.getElementById("room").setAttribute("value", e.room);
      document.getElementById("obs").setAttribute("value", e.obs);
      
      document.getElementById("date").readOnly = true;
      document.getElementById("start").readOnly = true;
      document.getElementById("end").readOnly = true;
      document.getElementById("obs").readOnly = true;
      document.getElementById("room").readOnly = true;
      document.getElementById("clientCheck").setAttribute("disabled", '');
      document.getElementById("equipment").setAttribute("disabled", '');
      document.getElementById("status").setAttribute("disabled", '');
      document.getElementById("professional").setAttribute("disabled", '');
      document.getElementById("client").setAttribute("disabled", '');
      document.getElementById("service").setAttribute("disabled", '');
      document.getElementById("phone").value=e.phone
      }
    creationModal.show()
  }
}