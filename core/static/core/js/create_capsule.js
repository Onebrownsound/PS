/**
 * Created by root on 4/10/16.
 */

$(document).ready(function () {
    var result = $('#id_delivery_condition').val();
    console.log(result);
    if (result == 'SD'){
        $('#div_id_delivery_date').removeClass('hidden');
    }
    else{
        $('#div_id_delivery_date').addClass('hidden');
    }
});




$('#id_delivery_condition').change(function(){
    var result = $('#id_delivery_condition').val();
    console.log(result);
    if (result == 'SD'){
        $('#div_id_delivery_date').removeClass('hidden');
    }
    else{
        $('#div_id_delivery_date').addClass('hidden');
    }
});