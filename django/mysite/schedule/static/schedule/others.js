$(document).ready(function(){
        $('.selectpicker').selectpicker();

        $('.button-submit').click(function(){
            alert("THIS WORKS!");
        })

        $('#export-button').click(function(){
            alert("THIS NEEDS TO EXPORT CSV")
            var toexport;
            var request = new XMLHttpRequest();
            request.open("GET", urlconfig);
            request.onreadystatechange = function() {
                if (this.readyState == this.DONE && this.status == 200) {
                    if (this.responseText) { 
                        toexport = this.responseText;
                        
                        // alert(ahem);
                    }
                    else {
                        console.log("Error: Data is empty");
                    }
                };
            }
            
        })


        $('select').on('change', function(e){
            $('#calendar').fullCalendar( 'removeEventSources');
            var targets = [];
            $.each($(".selectpicker option:selected"), function(){
            targets.push($(this).val());
            });
            // alert("You have selected the targets: " + targets.join(", "));
            // alert("tahgets: " + targets)
            const urlconfig = "/return_data/"+targets.join("+");
            if (targets.join(", ") !=""){
            var request = new XMLHttpRequest();
            request.open("GET", urlconfig);
            request.onreadystatechange = function() {
                if (this.readyState == this.DONE && this.status == 200) {
                    if (this.responseText) { 
                        ahem = this.responseText;
                        // alert(ahem);
                        $('#calendar').fullCalendar('addEventSource',urlconfig);
                        $('#calendar').fullCalendar('refetchEvents');
                    }
                else {
                        alert("no response");
                        console.log("Error: Data is empty");
                    }
                };
            }
            request.send();
            }
            else{
                // $('#calendar').fullCalendar( 'removeEventSources');
                // alert("DO NOTHING")
            }
            
            // alert(urlconfig)
            // alert("get sent")
        });

        $('button.actions-btn.bs-deselect-all.btn.btn-light').click(function() {
            alert( "Handler for .click() called." );
            $('#calendar').fullCalendar( 'removeEventSources');
        })
        $('div.filter-option-inner-inner').click(function() {
            var select = document.getElementById("course-selector");
            var ahem = '';
            var request = new XMLHttpRequest();
            request.open("GET", "/return_data/courses");
            request.onreadystatechange = function() {
                if (this.readyState == this.DONE && this.status == 200) {
                    if (this.responseText) { 
                        ahem = this.responseText;
                        // alert(ahem);
                        Ahem = JSON.parse(ahem);
                        select.options.length = 0;
                        for (var i = 0; i < Ahem.length; i++){
                            //$("#course-selected").append($('<option>', {value: 4, text: index}));
                            select.options[select.options.length] = new Option(Ahem[i].title);
                        };
                        // alert(select.options.length);
                        var txt = "";
                        var i;
                        for (i = 0; i < select.length; i++) {
                          txt = txt + " " + select.options[i].text;
                        };
                        // alert("there are" + select.options.length + " option objects in the selectpicker");
                        $('.selectpicker').selectpicker('refresh');
                        // alert("selectpicker refresh");
                    }
                    else {
                        console.log("Error: Data is empty");
                    }
                };
            }
            request.send();

          });

    });
// });

