$(document).ready(function(){;
    $(".view-request-accept").click(function(e){
        var bid = this.id;
        var btnr = "#btnr-" + bid.substring(bid.indexOf('-')+1,bid.length)

        if($(bid).hasClass('button-clicked')){
            $(bid).removeClass('button-clicked');
            $(btnr).removeAttr('disabled');
        }
        else{
            $(bid).addClass('button-clicked');
            alert($(bid).attr('class'));
            $(btnr).attr('disabled', 'disabled');
        }
    })

    var reject = false;
    $(".view-request-reject").click(function(e){
        if(reject!=true){
            reject = true;
            $(".view-request-reject").addClass('button-clicked');
            $(".view-request-accept").attr('disabled', 'disabled');

        }
        else{
            reject = false;
            $(".view-request-reject").removeClass('button-clicked');
            $(".view-request-accept").removeAttr('disabled');
        }
    })
})
