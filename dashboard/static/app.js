$(document).ready(function () {
    // device data from server
    
    // console.log(devices);
    console.log(window.device_data);
    // map functionalities
    $("#goole_live_map").googleMap({
        zoom: 15, // Initial zoom level (optional)
        coords: [23.7738159, 90.4106463], // Map center (optional)
        type: "ROADMAP" // Map type (optional)
    });

    $.each(window.device_data, function (index, element) {
        single_device = element.fields;
        if (single_device.device_status == 'inactive') {
            var icon = 'https://www.google.com/mapfiles/marker_black.png';
        } else {
            var icon = 'https://www.google.com/mapfiles/marker_green.png';
        }
        
        var marker = $("#goole_live_map").addMarker({
            coords: [single_device.lattitude, single_device.longitude], // GPS coords
            title: '<a href="http://' + single_device.device_ip + ':'+ single_device.device_port +'" target="_blank">' + single_device.device_code_name + '</a>', // Title
            text: single_device.position_address,
            icon: icon,
            success: function (e) {
                console.log(e)
            }
        });
        
    });

    // notification toastr
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
    // connect to local socket server
    namespace = '/test';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function () {
        socket.emit('my_event', {
            data: 'I\'m connected!'
        });
        toastr.success("Device Connected to " + document.domain);
    });

    socket.on('disconnect', function () {
        toastr.error("Device Disconnected from " + document.domain + " Retrying To Connect.");
    });

    socket.on('my_response', function (msg) {
        console.log('<br>Received: ' + msg.data);
    });


    // flame response 
    socket.on('flame_response', function (msg) {
        // console.log(msg);

        if (msg.flame) {
            $.playSound('./static/fire.mp3')
            toastr.error("Fire/Gas/Smoke Detected!", 'Alarm!!!', {
                timeOut: 10000,
                "tapToDismiss": false,
                "timeOut": 0,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        }
    });

    // temp_hum response 
    socket.on('temp_hum_response', function (msg) {
        // console.log(msg);
        $('#temp_id').html(msg.temp);
        $('#hum_id').html(msg.hum);

        console.log(msg.temp + ', ' + msg.hum);
    });

    // motion response 
    socket.on('motion_response', function (msg) {
        // console.log(msg);
        $('#motion_id').html(msg.detected);
        if (msg.detected) {
            $.playSound('./static/nsound.mp3')
            toastr.warning('Unusual Motion Detected!', {
                "tapToDismiss": false,
                "timeOut": 10000,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        }
    });
    // vibration response 
    socket.on('vibration_response', function (msg) {
        // console.log(msg);
        $('#vibration_id').html(msg.detected);
        if (msg.detected) {
            $.playSound('./static/nsound.mp3')
            toastr.warning('Unusual Vibration Detected!', {
                "tapToDismiss": false,
                "timeOut": 10000,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        }
    });
    // magnetic response 
    socket.on('magnetic_response', function (msg) {
        $.playSound('./static/nsound.mp3')
        // console.log(msg);
        if (msg.state) {
            $('#magnetic_id').html("Open");
            toastr.warning('Door Opened', {
                timeOut: 10000,
                "tapToDismiss": false,
                "timeOut": 0,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        } else {
            $('#magnetic_id').html("Closed");
            toastr.warning('Door Opened', {
                timeOut: 10000,
                "tapToDismiss": false,
                "timeOut": 0,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        }
    });
    // siren response 
    socket.on('siren_response', function (msg) {
        // console.log(msg);

        if (!msg.state) {
            $.playSound('./static/fire.mp3')
            $('#log').append('<br>' + $('<div/>').text('Received Panic Call #' + msg.time + ': ' + msg.state).html());
            toastr.error('Got a Panic Call!!!', {
                "tapToDismiss": false,
                "timeOut": 10000,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        } else {
            $('#siren_id').html('Safe');
        }
    });
    // attend_response
    socket.on('attend_response', function (msg) {
        // console.log(msg);

        if (!msg.state) {
            // $('#log').append('<br>' + $('<div/>').text('Received Attendance #' + msg.time + ': ' + msg.state).html());

            toastr.error('Got a Attendance Call!!!', {
                "tapToDismiss": false,
                "timeOut": 10000,
                "extendedTimeOut": 0,
                "progressBar": false,
            });
        } else {
            $('#siren_id').html('Safe');
        }
    });
});