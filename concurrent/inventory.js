$(document).ready(function(){
    document.session = $('#session').val();

    setTimeout(requestInventory, 100);

    $('#add-button').click(function(event){
        jQuery.ajax({
            url: '//localhost:8888/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'add'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings){
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#add-to-cart').hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });

    $('#remove-button').click(function(event){
        jQuery.ajax({
            url: '//localhost:8888/cart',
            type: 'POST',
            data: {
                session: document.session,
                active: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disabled');
            }
        });
    });
});

function requestInventory() {
    jQuery.getJSON('//localhost:8888/cart/status', {session: document.session}, 
        function(data, status, xhr) {
            $('#count').html(data['inventoryCount']);
            setTimeout(requestInventory, 0);
        }
    );
}

function requestInventory() {
    var host = 'ws://localhost:8888/cart/status';
    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) { };
    websocket.onmessage = function(evt) {
        $('#count').html($.parseJSON(evt.data)['inventoryCount']);
    };
    websocket.onerror = function (evt) {  };
}