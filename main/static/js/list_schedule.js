window.onload = (e) => {
  const radios = document.querySelectorAll('input[name="viewRadio"]')
  const creationModal = $("#creationModal").modal();
  const dateModal = $("#dateModal").modal();
  const clientModal = $("#personSearchModal").modal();
  const Calendar = tui.Calendar;
  const container = document.getElementById('calendar');
  const events = JSON.parse(document.getElementById('event_list').textContent); 
  const services = JSON.parse(document.getElementById('service_list').textContent); 
  const employeeChecks = $('#checkbox-group input[type="checkbox"]');
  const events_map = new Map();
  const service_map = new Map();
  const eventList = [];
  const calendarList = [];
  const serviceSelect2 = $("#service").select2();
  const clientSelect2 = $("#client").select2();
  const clientSearchSelect2 = $("#clientSearch").select2({dropdownParent: $('#personSearchModal')});
  const meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho" , "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
  const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'))
  const calendar = new Calendar(container, {
    defaultView: 'week',
    week:{ startDayOfWeek: 0, dayNames: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'], narrowWeekend: false, workweek: false, showNowIndicator: true, showTimezoneCollapseButton: false, timezonesCollapsed: false, hourStart: 6, hourEnd: 22, eventView: ['time'], taskView: false, collapseDuplicateEvents: false, allDay:false},
    month:{ dayNames: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'], visibleWeeksCount: 0, workweek: false, narrowWeekend: false, startDayOfWeek: 0, isAlways6Weeks: true, visibleEventCount: 6,},
    useCreationPopup: false,
    useDetailPopup: false,
  });
  calendar.setTheme({
    month: {
      moreView: {
        border: '2px solid grey',
        boxShadow: '0 2px 6px 0 grey',
        backgroundColor: '#F0F0F0',
        width: 640,
        height: 320,
      },
    },
  });

  let lastEdit;
  let lastSelectedService;

    //Inicializa os Select2
  serviceSelect2.select2({dropdownParent: $('#creationModal')});
  clientSelect2.select2({dropdownParent: $('#creationModal')});

    //Inicializa a datatable de confirmação 
  let table = $('#confirmTable').DataTable({
    orderable:false,
    dom: 't',
    select: {
      style: 'multi+shift'
    },
  });
  if(table.rows().data().length > 0)confirmModal.show();

    //Cria as divisões de calendário por Funcionário
  employeeChecks.each( function(index) {
    calendarList.push({
      id:$(this).attr("id"),
      name:$(this).data("name"),
      isVisible:true
    })
    console.log(calendarList[index])
  });
  calendar.setCalendars(calendarList);


    //inicializa a mascara de celular
  $('#phone').inputmask();

    //Popula o map de serviços
  for (i=0;i<services.length;i++) {
    service_map.set(services[i].pk, services[i].name)
  }

    //Adiciona o nome do mês na página
  document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;

    //carrega os eventos do Banco de Dados
    for (const event of events) {
      events_map.set(event.id, event)
      var color;
      switch(event.title){
        case "Pilates":
          color="#fce8a5"
          break;
        case "Facial":
          color="#a5e1e9"
          break;
        case "Corporal":
          color="#d5edb9"
          break;
        case "Injetáveis":
          color="#ffc296"
          break;
        case "Cortesia":
          color="#c4bdf3"
          break;
        case "Avaliação":
          color="#f8cadc"
          break;
        default:
          color="#ff8ad2"
      }

      let title;

      if(event.title == event.category){
        if(event.sale_id){
          event.is_courtesy? title = `${event.client} - ${event.professional_name} - ${event.service_name}` : title = `${event.client} - ${event.professional_name} - ${event.service_name}`
        }
        else {
          title = `${event.client} - ${event.professional_name} - ${event.service_name}`
        }
      } else {
        title=event.title;
      }
  
      const eventObject = {
        id: event.id,
        calendarId: event.professional_id,
        title: title,
        start: `${event.date}T${event.start}`,
        end: `${event.date}T${event.end}`,
        backgroundColor:color
      };
      eventList.push(eventObject);
    }
    calendar.createEvents(eventList);


    //Event Handlers
  clientModal.on("hidden.bs.modal", function(){
    $("#hiddenMsg").hide();
    $("#clientTable tbody").empty();
    clientSearchSelect2.val(null).trigger('change');
  });

  $("#clientSearch").on('change', function(){
    $.ajax({
      url:$(this).find(":selected").data('url'),
      method:"GET",  
      dataType:"json",
      success: function(data){
        console.log(data)
        data.forEach(item => {
          if(!($("#"+item.professional_id).is(":checked"))){
            $("#hiddenMsg").show();
            return;
          }
          var tr = $("<tr>")
          var date_obj = new Date(item.date+'T00:00:00')
          var dateBtn = $("<a>").text(`${String(date_obj.getDate()).padStart(2, '0')}/${String(date_obj.getMonth()+1).padStart(2, '0')}/${date_obj.getFullYear()}`).addClass('date-btn').css('cursor', 'pointer');
          dateBtn.on('click', function(){
            console.log(date_obj)
            calendar.setDate(date_obj);
            clientModal.modal('hide');
          });

          var service = $("<td>").text(item.service)
          var professional = $("<td>").text(item.professional)
          var equipment = $("<td>").text(item.equipment)
          var date = $("<td>").append(dateBtn);
          var start = $("<td>").text(item.start)
          var end = $("<td>").text(item.end)

          tr.append(service, professional, equipment, date, start, end)
          $("#clientTable").append(tr);
        });
      },
    })
  });

  $("#personSearchBtn").on('click', function(){
    clientModal.modal('show');
  });

  $("#searchDate").on("click", function(){
    if($("#dateInput").val()!=null) calendar.setDate(new Date($("#dateInput").val()));
    dateModal.modal('hide')
  }); 

  $("#dateBtn").on("click", function(){
    dateModal.modal('show');
  });

  dateModal.on('hidden.bs.modal', function(){
      $("#dateInput").val(null)
  })
  
  employeeChecks.each(function(){
    $(this).on('change', function(){
      calendar.setCalendarVisibility(Number($(this).attr('id')), $(this).is(":checked"));
    })
  });

  $("#unconfirmButton").on(
    "click", function(e){
      var dados = table.rows({ selected: true }).data();
      var ids= []
      dados.each(function (data) {
        ids.push(data[0]);
      });
      
      $.ajax({
        url:"unconfirm/",
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

  $("#confirmButton").on(
    "click", function (e){
      var dados = table.rows({ selected: true }).data();
      var ids= []
      dados.each(function (data) {
        ids.push(data[0]);
      });

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

  clientSelect2.on(
    "change", (e) => {
      $.ajax({
        url:"service_filter/" + e.target.value,
        method:"GET",
        dataType:"json",
        success: function(data){
          $("#service").empty()
          $("#phone").val(data[0])
          data[1].forEach(item => {
            option = new Option(item.service, item.service_id, false, false);
            $(option).attr('data-sale-id', item.sale_id);
            $('#service').append(option);
          });

          $('#service').append(new Option("Avaliação", -1));
          $('#service').append(new Option("Cortesia", -2));

          $("#service").val(lastSelectedService).trigger('change');
        },
         error: function (data) {

          $("#service").empty()
          $('#service').append(new Option("Avaliação", -1));
          $('#service').append(new Option("Cortesia", -2));
         }
      })
      $("#_client").val(e.target.options[e.target.selectedIndex].textContent)
      // $("#phone").val(e.target.options[e.target.selectedIndex].getAttribute("data-phone"))
    }
   )

  document.getElementById("clientCheck").addEventListener(
    "change", (e) => {
      if(e.target.checked){
        document.getElementById("_client-div").hidden=false;
        $("#client-div").hide();
        $("#client-div").removeClass('d-flex');
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
        $("#client-div").show();
        $("#client-div").addClass('d-flex');
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
      calendar.changeView(e.target.value)
      document.getElementById("month").textContent=`${meses[calendar.getDate().getMonth()]}/${calendar.getDate().getFullYear()}`;
    })
  }


  document.getElementById("editButton").addEventListener(
    "click", (e) => {
      $("#editButton").attr('hidden', true);
      $("#confirmEditButton").attr('hidden', false);
      console.log(e)

      $("#date").attr("readOnly",false);
      $("#start").attr("readOnly",false);
      $("#end").attr("readOnly",false);
      $("#clientCheck").attr("disabled",false);
      if($("#clientCheck").is(':checked')){
        $("#client_div").removeClass('d-flex').hide();
        document.getElementById("_client-div").hidden=false;
      } else {
        document.getElementById("_client-div").hidden=true;
        $("#client-div").addClass('d-flex').show();
      }
      $("#_client").attr('disabled', false).attr('readonly', false);
      $("#client").attr("disabled", false);
      $("#service").attr("disabled", false);
      $("#professional").attr("disabled", false);
      $("#room").attr("readOnly", false);
      $("#equipment").attr("disabled", false);
      $("#obs").attr("readOnly", false);
      $("#phone").attr("readOnly", false);
    }
  )

  document.getElementById("confirmEditButton").addEventListener(
    "click", (e) => {
      document.getElementById("modalForm").setAttribute("action", `edit/${lastEdit}/`);
      document.getElementById("modalForm").submit();
    }
  )

  document.getElementById("deleteButton").addEventListener(
    "click", (e) => {
      if(confirm("Tem certeza que deseja deletar o agendamento?")==true){
        document.getElementById("modalForm").setAttribute("action", `delete/${lastEdit}/`);
        document.getElementById("modalForm").submit();
      }
    }
  )

  document.getElementById("submitCreation").addEventListener(
    "click", (e) => {
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
      calendar.clearGridSelections();
      openCreationModal(e, "create");
    },
    'clickEvent': (event) => {
        calendar.clearGridSelections();
        openCreationModal(event, "edit");
    },
    'beforeUpdateEvent': function(e) {
      calendar.clearGridSelections();
        if(confirm("Tem certeza que deseja alterar o agendamento?")==true){
          (e.changes.start) ? e.event.start = e.changes.start : {};
          (e.changes.end) ? e.event.end = e.changes.end : {};
          calendar.updateEvent(e.event.id, e.event.calendarId, e.event);

        }
    },
    'beforeDeleteSchedule': function(e) {
        calendar.clearGridSelections();
        calendar.deleteSchedule(e.schedule.id, e.schedule.calendarId);
    }
  });

  creationModal.on("hidden.bs.modal", function (event) {
      calendar.clearGridSelections();
      $("#client").val(null).trigger('change');
      $("#service").val(null).trigger('change');
      $("#ModalForm").trigger('reset');
    }); 

  //Funções
  function openCreationModal(e, isCreation){
    if(isCreation==="create"){
      $("#status").empty()
      $("#status").append($("<option>", {value: "1", text: "Novo"}))
      document.getElementById("modalForm").setAttribute("action", document.getElementById("modalForm").getAttribute("create-url"));

      document.getElementById("primaryFooter").hidden=false;
      document.getElementById("secondaryFooter").hidden=true;
      $("#obs").val(null);

      document.getElementById("date").readOnly = false;
      document.getElementById("start").readOnly = false;
      document.getElementById("end").readOnly = false;
      document.getElementById("obs").readOnly = false;
      document.getElementById("room").readOnly = false;
      document.getElementById("_client").readOnly = false;
      document.getElementById("_client-div").hidden = true;
      $("#client-div").addClass('d-flex').show();
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
      $("#editButton").attr('hidden', false);
      $("#clientCheck").attr('checked', !e.client_id)
      $("#confirmEditButton").attr("hidden", true);
      lastEdit = e.event.id;
      e = events_map.get(e.event.id);
      if(e.status!=1) $("#editButton").attr('hidden', true)
      console.log(e)
      document.getElementById("primaryFooter").hidden=true;
      document.getElementById("secondaryFooter").hidden=false;

      document.getElementById("equipment").value = (e.equipment_id ? e.equipment_id : null);
      if(e.status=="1"){
        document.getElementById("status").append(new Option("Novo", 1, true, true))
        document.getElementById("status").value = 1;
      } else if(e.status=="3"){
        document.getElementById("status").append(new Option("Cancelado", 3, true, true))
        document.getElementById("status").value = 3;
      } 
      else {
        document.getElementById("status").append(new Option("Confirmado", 2, true, true))
        document.getElementById("status").value = 2;
      }
      
      document.getElementById("professional").value= e.professional_id;
      clientSelect2.val(e.client_id).trigger('change')
      $("#client-div").removeClass('d-flex').hide();
      document.getElementById("_client-div").hidden= false;
      document.getElementById("_client").readOnly= true;
      document.getElementById("_client").value= e.client;
      if(e.service_id) {
        $("#service").val(e.service_id).trigger('change');
        lastSelectedService = e.sale_id
      } 
      else {
        if (e.is_courtesy){
          console.log("cortesia")
          $("#service").val(-2).trigger('change');
          lastSelectedService = -2;
        } else {
          $("#service").val(-1).trigger('change');
          lastSelectedService = -1;
        } 
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

      $("#clientCheck").prop('checked', e.client_id==null)
    }
    creationModal.modal('show')
  }
}