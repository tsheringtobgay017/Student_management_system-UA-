// -----------------------Form Validation--------------------------------//
const enrollForm = document.getElementById('registration_form');

const enrollfv = FormValidation.formValidation(enrollForm, {
    fields: {
        cid: {
            validators: {
                notEmpty: {
                    message: 'The CID field is required',
                },
                stringLength: {
                    max: 11,
                    message: 'The CID must be 11 characters'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        dob: {
            validators: {
                notEmpty: {
                    message: 'The DOB field is required',
                },
            },
        },

        email: {
            validators: {
                emailAddress: {
                        message: 'The value is not a valid email address',
                    },
                notEmpty: {
                    message: 'The email field is required',
                },
            },
        },
        phone_number: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min: 8,
                    message: 'The Phone number must be 8 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        first_name: {
            validators: {
                notEmpty: {
                    message: 'The Name field is required',
                },
            },
        },


        permanent_dzongkhag: {
            validators: {
                notEmpty: {
                    message: 'Please select Dzongkhag',
                }
            },
        },
        permanent_gewog: {
            validators: {
                notEmpty: {
                    message: 'Please select Gewog',
                }
            }
        },

        permanent_village: {
            validators: {
                notEmpty: {
                    message: 'Please select Village',
                }
            }
        },

        // academic details
        previous_school: {
            validators: {
                notEmpty: {
                    message: 'The Name field is required',
                },
            },
        },

        index_number: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min: 5,
                    message: 'The student index must be 5 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },

        percent: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min: 2,
                    message: 'The student index must be 2 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },

        supw: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                }
            }
        },
        
        parent_cid: {
            validators: {
               notEmpty: {
                    message: 'The CID field is required',
                },
                stringLength: {
                    max: 11,
                    message: 'The CID must be 11 characters'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            }
        },
        parent_name: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                }
            }
        },

       

        parent_number: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min: 8,
                    message: 'The Phone number must be 8 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },

        present_dzongkhag: {
            validators: {
                notEmpty: {
                    message: 'Please select Dzongkhag',
                }
            },
        },
        present_gewog: {
            validators: {
                notEmpty: {
                    message: 'Please select Gewog',
                }
            }
        },

        present_village: {
            validators: {
                notEmpty: {
                    message: 'Please select Village',
                }
            }
        },


    },

    plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap: new FormValidation.plugins.Bootstrap(),
        // tachyons: new FormValidation.plugins.Tachyons(),
        submitButton: new FormValidation.plugins.SubmitButton(),

    },
}).on('core.form.valid', function (e) {
    studentDetail();

}).on('core.form.invalid', function (e) {
    swal("Validation failed !!!", "Some required fields are empty", "error")
});

function studentDetail() { 
    var form = document.getElementById("registration_form");
    var data = new FormData(form);
    $.ajax({
        type: 'POST',
        url: '/store-student-info',
        data: data,
        processData: false,
        contentType: false,
        cache: false,

        success: function (res) {
            swal("Information successfully submitted", "Click Ok to continue", "success")
                .then(function () {
                    window.location = ""
                })
        },
        error: function () {
            swal("Infomation submission failed", "Click Ok to continue", "error")
                .then(function () {
                    window.location = ""
                })
        }
    });
};

//------------------------Script for fetching gewog list-------------------------//
$("#present_dzongkhag").on("change", function () {
    var gewog_id = $("#present_dzongkhag").val();
    $.ajax({
        url: "/get-gewog-list",
        method: "POST",
        data: { type: 'Gewog', gewog_id: gewog_id },
        dataType: "json",
        success: function (data) {
            
            var list = data.gewogList;
            var html = "<option value=''>---Select Gewog---</option>";
            for (var count = 0; count < list.length; count++) {
                html += "<option value='" + list[count].gewog_id + "'>" + list[count].gewog_name + "</option>"
            }
            $("#present_gewog").html(html);
        },
        error: function (e) {
            alert('error',e);
        }
    });
});
//-------------------------script ends-----------------------------------//

//--------------------------Script for fetching village list-------------------//
$("#present_gewog").on("change", function () {
    var village_id = $("#present_gewog").val();
    $.ajax({
        url: "/get-village-list",
        method: "POST",
        data: { type: 'village', village_id: village_id },
        dataType: "json",
        success: function (data) {
            var list = data.villageList
            var html = "<option value=''>---Select Village---</option>";
            for (var count = 0; count < list.length; count++) {
                html += "<option value='" + list[count].village_id + "'>" + list[count].village_name + "</option>"
            }

            $("#present_village").html(html);
        },
        error: function () {
            alert('error');
        }
    });
})
//-------------------------------Script ends--------------------------------//


//------------------------Script for fetching gewog list for permanent address-------------------------//
$("#permanent_dzongkhag").on("change", function () {
    var gewog_id = $("#permanent_dzongkhag").val();
    $.ajax({
        url: "/get-gewog-list",
        method: "POST",
        data: { type: 'Gewog', gewog_id: gewog_id },
        dataType: "json",
        success: function (data) {
            
            var list = data.gewogList;
            var html = "<option value=''>---Select Gewog---</option>";
            for (var count = 0; count < list.length; count++) {
                html += "<option value='" + list[count].gewog_id + "'>" + list[count].gewog_name + "</option>"
            }
            $("#permanent_gewog").html(html);
        },
        error: function () {
            alert('error');
        }
    });
});
//-------------------------script ends-----------------------------------//

//--------------------------Script for fetching village list-------------------//
$("#permanent_gewog").on("change", function () {
    var village_id = $("#permanent_gewog").val();
    $.ajax({
        url: "/get-village-list",
        method: "POST",
        data: { type: 'village', village_id: village_id },
        dataType: "json",
        success: function (data) {
            var list = data.villageList
            var html = "<option value=''>---Select Village---</option>";
            for (var count = 0; count < list.length; count++) {
                html += "<option value='" + list[count].village_id + "'>" + list[count].village_name + "</option>"
            }

            $("#permanent_village").html(html);
        },
        error: function () {
            alert('error');
        }
    });
})
//-------------------------------Script ends--------------------------------//



