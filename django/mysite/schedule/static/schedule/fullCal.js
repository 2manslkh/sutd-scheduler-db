$(document).ready(function(){
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
                    title: "Event1",
                    start: "2019-02-25", //YYYY-MM-DD
                    end: "2019-02-25",
                    allDay:true
                },
                {
                    title: "Event2",
                    start: "2019-02-27",
                    end: "2019-02-28 09:00",
                    allDay:false
                }
            ],
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
