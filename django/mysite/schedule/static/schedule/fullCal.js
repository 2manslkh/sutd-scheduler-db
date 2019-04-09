$(document).ready(function(){

        $('.selectpicker').selectpicker();

        $('#calendar').fullCalendar({
            //hiddenDays:[0,6], same as below

            weekends: false,
            header : {
                left: "month,agendaWeek,agendaDay", //space leaves a gap between buttons
                center: "title",
                right:"today, prev,next"
            },
            aspectRatio:1.5,
            defaultView: 'agendaWeek',
            // themeSystem: 'bootstrap4',
            allDaySlot: false,
            height: 'auto',
            timezone: 'Asia/Singapore',
            /* Min and Max time on calendar */
            minTime: "08:00:00",
            maxTime: "20:00:00",
            events:[
                {
                    title: "Elements of Software Construction",
                    start: "2019-02-25 10:00", //YYYY-MM-DD
                    end: "2019-02-25 11:30",
                    description: "Prof",
                    location: "LT"
                },
                {
                    title: "Probs and Stats",
                    start: "2019-04-01 08:00",
                    end: "2019-04-01 09:40",
                    description: "Prof",
                    location: "CC13"
                }
            ],
            color: 'yellow',
            textColor: 'black',

            eventRender: function(objEvent, element, view) {
                if (view.name === "agendaWeek" || view.name === "agendaDay"){
                 element.find(".fc-content").append(objEvent.location + "</br>" + objEvent.description);
                 //element.find(".fc-title").empty().append('<div class="fc-title"><b>Probs and Stats<b></div>')
                }},

            eventAfterAllRender: function (view, element) {
                //The title isn't rendered until after this callback, so we need to use a timeout.
                if(view.type === "agendaWeek"){
                    window.setTimeout(function(){
                        $("#calendar").find('.fc-toolbar').append(
                            "<div id='schedule-filter'>"+
                            "<select class='selectpicker' multiple data-actions-box='true' title='Filter'>"+
                            "<option>Course 1</option>"+
                            "<option>Course 2</option>"+
                        $("#calendar").find('.fc-toolbar').append(
                            "<button class='button-submit'>&#8629;</button>"+
                       $("#calendar").find('.fc-toolbar').append(
                            '<button id="export-button">'+
                            '<i class="far fa-share-square"></i>'+
                            '</button>'
                        )));
                    },0);
                }
            },


            selectable:false,
            select: function(start, end, jsEvent, view){
                var obj = {};
                obj.title = prompt("Enter a title:", "Event");
                obj.start = moment(start).format("YYYY-MM-DD hh:mm");
                obj.end = moment(end).format("YYYY-MM-DD hh:mm");
                allDay = false;
            },
        });
    });
