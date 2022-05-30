// -----------------------Form Validation--------------------------------//
const MarkSubmission = document.getElementById('info');
const markfv = FormValidation.formValidation(MarkSubmission, {
    fields: {
        class_test_1: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min:2,
                    message: 'The Phone number must be 2 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        CA: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min:2,
                    message: 'The Phone number must be 2 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        mid_term: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min:2,
                    message: 'The Phone number must be 2 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        annual_exam: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min:2,
                    message: 'The Phone number must be 2 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        class_test_2: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                },
                stringLength: {
                    min:2,
                    message: 'The Phone number must be 2 digits'
                },
                numeric: {
                    message: 'The value is not a number',
                    // The default separators
                    thousandsSeparator: '',
                    decimalSeparator: '.',
                },
            },
        },
        std_status: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                }
            }
        },
        punctuality: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                }
            }
        },
        discipline: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                }
            }
        },
        socialservice: {
            validators: {
                notEmpty: {
                    message: 'This field is required',
                }
            }
        },
        leadership: {
                validators: {
                    notEmpty: {
                        message: 'This field is required',
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
    std_detail_validation();
    alert('hi')

}).on('core.form.invalid', function (e) {
    swal("Validation failed !!!", "Some required fields are empty", "error")
});
