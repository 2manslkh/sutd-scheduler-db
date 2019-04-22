$(document).ready(function(){
        $('.selectpicker').selectpicker();

        $('.button-submit').click(function(){
            alert("THIS WORKS!");
        })

        $('#export-button').click(function(){
            alert("THIS NEEDS TO EXPORT CSV")
            // TODO: EXPORT EVENTS FROM 2
        })


        $('select').on('change', function(e){
            var targets = [];
            $.each($(".selectpicker option:selected"), function(){
            targets.push($(this).val());
            });
            alert("You have selected the targets: " + targets.join(", "))
        });

});
