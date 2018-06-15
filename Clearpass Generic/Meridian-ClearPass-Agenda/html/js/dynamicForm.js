var maxEntries = 20;

$(function () {
  $('#btnAddClient').click(function () {
    var num = $('.clonedInputClient').length;    // how many "duplicatable" input fields we currently have
    var newNum = num + 1;                   // the numeric ID of the new input field being added

    // create the new element via clone(), and manipulate it's ID using newNum value
    var newElem = $('#input' + num).clone().find('[id]').andSelf().attr('id', function(index, attr) {
      return attr.replace(/[0-9]*$/, '') + newNum;
    }).attr('name', function(index, attr) {
      return (attr === undefined) ? undefined : attr.replace(/[0-9]*$/, '') + newNum;
    }).eq(0);

    // insert the new element after the last "duplicatable" input field
    $('#input' + num).after(newElem);

    // enable the "remove" button
    $('#btnDelClient').prop('disabled', false);

    // business rule: you can only add "maxEntries" names
    if (newNum == maxEntries)
      $('#btnAddClient').attr('disabled', 'disabled');
  });

  $('#btnDelClient').click(function () {
    var num = $('.clonedInputClient').length;    // how many "duplicatable" input fields we currently have
    $('#input' + num).remove();        // remove the last element

    // enable the "add" button
    $('#btnAddClient').prop('disabled', false);

    // if only one element remains, disable the "remove" button
    if (num - 1 == 1)
      $('#btnDelClient').prop('disabled', true);
  });


  $('#btnDelClient').prop('disabled', true);

});


$(function () {
  $('#btnAddTimeSlot').click(function () {
    var num = $('.clonedInputTimeSlot').length;    // how many "duplicatable" input fields we currently have
    var newNum = num + 1;                   // the numeric ID of the new input field being added

    // create the new element via clone(), and manipulate it's ID using newNum value
    var newElem = $('#TimeSlot' + num).clone().find('[id]').andSelf().attr('id', function(index, attr) {
      return attr.replace(/[0-9]*$/, '') + newNum;
    }).attr('name', function(index, attr) {
      return (attr === undefined) ? undefined : attr.replace(/[0-9]*$/, '') + newNum;
    }).eq(0);

    // insert the new element after the last "duplicatable" input field
    $('#TimeSlot' + num).after(newElem);

    // enable the "remove" button
    $('#btnDelTimeSlot').prop('disabled', false);

    // business rule: you can only add "maxEntries" names
    if (newNum == maxEntries)
      $('#btnAddTimeSlot').attr('disabled', 'disabled');
  });

  $('#btnDelTimeSlot').click(function () {
    var num = $('.clonedInputTimeSlot').length;    // how many "duplicatable" input fields we currently have
    $('#TimeSlot' + num).remove();        // remove the last element

    // enable the "add" button
    $('#btnAddTimeSlot').prop('disabled', false);

    // if only one element remains, disable the "remove" button
    if (num - 1 == 1)
      $('#btnDelTimeSlot').prop('disabled', true);
  });


  $('#btnDelTimeSlot').prop('disabled', true);

});


var token;
   $('form input[type="submit"]').on('click', function () {
       var $btn = $(this).button('loading')
       $(this).closest('form').submit();
   });
   $("#auth form").on('submit', function(e) {
           e.preventDefault();
           u = $("#username").val();
           p = $("#password").val();
           console.log(u + " " + p);
           $("#auth .alert").first().hide();
           $.getJSON("/cgi-bin/auth_v2.py",{"username": u, "password": p}, function( data ) {
                   console.log(data);
                   if("token" in data) {
                           console.log("Auth ok");
                           $("#token").val(data['token']);
                           $("#auth").fadeOut(500, function() {$("#creation").fadeIn(500)});
                   } else {
                           $("#auth .alert.alert-danger").first().show();
                           console.log("Auth failed");
                   }
           });
   });


   $('#creation form').on('submit', function(e) {
   $(".alert").hide();
   e.preventDefault();  //J'empêche le comportement par défaut du navigateur, c-à-d de soumettre le formulaire
   console.log("Submitting...");
   var $this = $(this);
   var d = new FormData($this[0]);
   console.log("Submitting2...");
   console.log(d);
       $.ajax({
           url: $this.attr('action'),
           type: $this.attr('method'),
           data: d,
           dataType: "json",
           cache: false,
           contentType: false,
           processData: false,
           success: function(data) {
                   console.log(data);
                   var response = data['response'];
                   if('result' in response) {
                           $("#creation .alert-danger .error-message").html(response['result']['message']);
                           $("#creation .alert-danger").show();
                           console.log("Issue: some guests already exist and can't be updated");
                   } else {
                           $this[0].reset();
                           $("#creation .alert-success").show();
                           console.log(data);
                           console.log("Success");
                   }
           },
           error: function(data) {
                   $("#creation .alert-danger .error-message").html(data);
                   $("#creation .alert-danger").show();
                   console.log("Issue somewhere");
           }
   });
   console.log("SubmittingEnd...");
});

$(document).ready(function() {
    $('#datePicker')
        .datepicker({
            format: 'mm/dd/yyyy'
        })
        .on('changeDate', function(e) {
            // Revalidate the date field
            $('#creation orm').formValidation('revalidateField', 'date');
        });
        $('#creation form').formValidation({
            framework: 'bootstrap',
            icon: {
                   valid: 'glyphicon glyphicon-ok',
                   invalid: 'glyphicon glyphicon-remove',
                   validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
//                    name: {
//                          validators: {
//                                      notEmpty: {
//                                                message: 'The name is required'
//                                                }
//                                      }
//                        },
                      date: {
                             validators: {
                                         notEmpty: {
                                                   message: 'The date is required'
                                         },
                                         date: {
                                               format: 'MM/DD/YYYY',
                                               message: 'The date is not a valid'
                                         }
                              }
                      }
            }
    });
});
