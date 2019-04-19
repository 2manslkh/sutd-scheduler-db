$(document).ready(function(){;
    $(".view-request-accept").click(function(e){
        var bid = this.id;
        var btnr = "#btnr-" + bid.substring(bid.indexOf('-')+1,bid.length)
        var str_bid ="#"+bid;

        if($(str_bid).hasClass('button-clicked')){
            $(str_bid).removeClass('button-clicked');
            $(btnr).removeAttr('disabled');
        }
        else{
            $(str_bid).addClass('button-clicked');
            $(btnr).attr('disabled', 'disabled');
        }
    })

    $(".view-request-reject").click(function(e){
        var bid = this.id;
        var btna = "#btna-" + bid.substring(bid.indexOf('-')+1,bid.length)
        var str_bid ="#"+bid;

        if($(str_bid).hasClass('button-clicked')){
            $(str_bid).removeClass('button-clicked');
            $(btna).removeAttr('disabled');
        }
        else{
            $(str_bid).addClass('button-clicked');
            $(btna).attr('disabled', 'disabled');
        }
    })
})
