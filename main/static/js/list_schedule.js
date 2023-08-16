window.onload = (e) => {
  const radios = document.querySelectorAll('input[name="viewRadio"]')
  const creationModal = new bootstrap.Modal(document.getElementById('creationModal'), {backdrop:'static'})
  const Calendar = tui.Calendar;
  const container = document.getElementById('calendar');
  const events = JSON.parse(document.getElementById('data-el').textContent); 
  const events_map = new Map();
  const calendar = new Calendar(container, {
    defaultView: 'week',
    week:{
        startDayOfWeek: 0,
        dayNames: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
        narrowWeekend: false,
        workweek: true,
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
      workweek: true,
      narrowWeekend: true,
      startDayOfWeek: 0,
      isAlways6Weeks: true,
      visibleEventCount: 6,
    },
    useCreationPopup: false,
    useDetailPopup: false,
  });

  var lastEdit;

    //carrega os eventos do Banco de Dados
  for(let i=0;i<events.length;i++){ 
    let id;
    (events[i].professional_id) ? id = events[i].professional_id : id = i; 
    events_map.set(events[i].id, events[i]);
    calendar.createEvents([
      {
        id: events[i].id,
        calendarId: id,
        title: events[i].title,
        start: `${events[i].date}T${events[i].start}`,
        end: `${events[i].date}T${events[i].end}`
      },
    ]);
  }

    //Event Handlers
  document.getElementById("editButton").addEventListener(
    "click", (e) => {
      document.getElementById("modalForm").setAttribute("action", `${document.getElementById("modalForm").getAttribute("edit-url")}${lastEdit}`)
      document.getElementById("primaryFooter").hidden=false;
      document.getElementById("secondaryFooter").hidden=true;
      allowEditing();
    }
  )
  
  document.getElementById("prev").addEventListener(
    "click", (e) => {
      calendar.prev()
    }
  )
  document.getElementById("next").addEventListener(
    "click", (e) => {
      calendar.next()
    }
  )
  document.getElementById("today").addEventListener(
    "click", (e) => {
      calendar.today()
    }
  )

  for(let i=0;i<radios.length;i++){
    radios[i].addEventListener("change", (e) =>{
      console.log(e.target.value)
      console.log(typeof(e.target.value))
      if(e.target.value == "month"){
        
      }
      calendar.changeView(e.target.value)
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
      document.getElementById("modalForm").submit();
    }
  );

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
    console.log('clickEvent', e);
    if(isCreation==="create"){
      document.getElementById("modalForm").setAttribute("action", document.getElementById("modalForm").getAttribute("create-url"));

      document.getElementById("primaryFooter").hidden=false;
      document.getElementById("secondaryFooter").hidden=true;

      document.getElementById("date").readOnly = false;
      document.getElementById("start").readOnly = false;
      document.getElementById("end").readOnly = false;
      document.getElementById("obs").readOnly = false;
      document.getElementById("sessions").readOnly = false;
      document.getElementById("room").readOnly = false;
      document.getElementById("equipment").removeAttribute("disabled");
      document.getElementById("status").removeAttribute("disabled");
      document.getElementById("professional").removeAttribute("disabled");
      document.getElementById("client").removeAttribute("disabled");
      document.getElementById("service").removeAttribute("disabled");

      let start = new Date(e.start)
      let end = new Date(e.end)
      let year = String(start.getYear()+1900);
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
      lastEdit = e.event.id;
      e = events_map.get(e.event.id);
      document.getElementById("primaryFooter").hidden=true;
      document.getElementById("secondaryFooter").hidden=false;

      document.getElementById("equipment").value = e.equipment_id;
      document.getElementById("status").value= e.status_id;
      document.getElementById("professional").value= e.professional_id;
      document.getElementById("client").value= e.client_id;
      document.getElementById("service").value= e.service_id;
      document.getElementById("date").setAttribute("value", e.date);
      document.getElementById("start").setAttribute("value", e.start);
      document.getElementById("end").setAttribute("value", e.end);
      document.getElementById("sessions").setAttribute("value", e.sessions);
      document.getElementById("room").setAttribute("value", e.room);
      document.getElementById("obs").setAttribute("value", e.obs);
      
      document.getElementById("date").readOnly = true;
      document.getElementById("start").readOnly = true;
      document.getElementById("end").readOnly = true;
      document.getElementById("obs").readOnly = true;
      document.getElementById("sessions").readOnly = true;
      document.getElementById("room").readOnly = true;
      document.getElementById("equipment").setAttribute("disabled", '');
      document.getElementById("status").setAttribute("disabled", '');
      document.getElementById("professional").setAttribute("disabled", '');
      document.getElementById("client").setAttribute("disabled", '');
      document.getElementById("service").setAttribute("disabled", '');
      }
    creationModal.show()
  }

  function allowEditing(){
    document.getElementById("date").readOnly = false;
    document.getElementById("start").readOnly = false;
    document.getElementById("end").readOnly = false;
    document.getElementById("obs").readOnly = false;
    document.getElementById("sessions").readOnly = false;
    document.getElementById("room").readOnly = false;
    document.getElementById("equipment").removeAttribute("disabled");
    document.getElementById("status").removeAttribute("disabled");
    document.getElementById("professional").removeAttribute("disabled");
    document.getElementById("client").removeAttribute("disabled");
    document.getElementById("service").removeAttribute("disabled");
  }
}