$(document).ready(function(){
        $('.selectpicker').selectpicker();

        $('.button-submit').click(function(){
            alert("THIS WORKS!");
            $('#calendar').fullCalendar('rerenderEvents');
        })
});
