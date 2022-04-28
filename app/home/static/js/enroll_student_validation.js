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

    },

    plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap: new FormValidation.plugins.Bootstrap(),
        // tachyons: new FormValidation.plugins.Tachyons(),
        submitButton: new FormValidation.plugins.SubmitButton(),

    },
}).on('core.form.valid', function (e) {
    alert("hi")
    studentDetail();

}).on('core.form.invalid', function (e) {
    swal("Validation Error", "Some required field are empty.", "error")
});


