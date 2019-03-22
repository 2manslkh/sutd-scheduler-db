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
                    start: "2019-02-27 08:00",
                    end: "2019-02-27 09:00",
                    description: "Prof",
                    location: "CC13",
                    allDay:false
                }
            ],
             eventRender: function(objEvent, element, view) {
                if (view.name === "agendaWeek" || view.name === "agendaDay"){
                 element.find(".fc-content").append(objEvent.location + "</br>" + objEvent.description);
                }},
            selectable:false,
            select: function(start, end, jsEvent, view){
                var obj = {};
                obj.title = prompt("Enter a title:", "Event");
                obj.start = moment(start).format("YYYY-MM-DD hh:mm");
                obj.end = moment(end).format("YYYY-MM-DD hh:mm");
                allDay = false;
            },
            // googleCalendarApiKey: 'AIzaSyBrdMz3MNGRudZfvIL5rhc7bO56J0W3u-k',
            // events: {
            //     googleCalendarId:'cuc1ieh5sg33in6dmfel61b6vg@group.calendar.google.com'
            // }

        });
    });
