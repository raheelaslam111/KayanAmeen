odoo.define('islamic_calendar.islamic_calendar', function(require) {
    "use strict"

    var core = require('web.core');
    var datepicker = require('web.datepicker');
    var datetimefield = require('web.basic_fields');
    var ListRenderer = require('web.ListRenderer');
    var ListController = require('web.ListController');
    var time = require('web.time');
    var FormController = require('web.FormController');
    var field_utils = require('web.field_utils');
    var session = require('web.session');
    var fieldRegistry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var _t = core._t;
    var qweb = core.qweb;
    var lang = '';
    var date_format = '%m/%d/%Y';

//    var FieldIslamicDate = AbstractField.extend({
//    className: 'd-block o_field_islamic_date',
//    _render: function () {
//        this.$el.html(QWeb.render('HijriDateWidget', {
////            embedCode: this.value,
//
//        }));
//         },
//        });

    datepicker.DateWidget.include({
        start: function() {
            var def = new $.Deferred();
            this.$input = this.$('input.oe_datepicker_master');
            this.$input_picker = this.$('input.oe_datepicker_container');
            this.$input_hijri = this.$el.find('input.oe_hijri');
            $(this.$input_hijri).val('');
            this._super();
            this.$input = this.$('input.oe_datepicker_master');
            var self = this;

            function convert_to_hijri(date) {
                if (date.length == 0) {
                    return false
                }
                var jd = $.calendars.instance('islamic').toJD(parseInt(date[0].year()), parseInt(date[0].month()), parseInt(date[0].day()));
                var date = $.calendars.instance('gregorian').fromJD(jd);
                var date_value = new Date(parseInt(date.year()), parseInt(date.month()) - 1, parseInt(date.day()));
                self.$el.find('input.oe_simple_date').val(self.formatClient(date_value, self.type_of_date));
                self.change_datetime();
            }
            try {
                this._rpc({
                    model: 'res.users',
                    method: 'get_localisation',
                    args: [session.uid],
                }).then(function(res) {
                    def.resolve(res);
                });
                def.done(function(val) {
                    var date =
                        $(self.$input_hijri).calendarsPicker({
                            calendar: $.calendars.instance('islamic', val.lang),
                            dateFormat: 'M d, yyyy',
                            onSelect: convert_to_hijri,
                        });
                    if (self.$el.find('.oe_hijri').val()) {
                        var datetime = moment(self.$el.find('.oe_hijri').val());
                        self.$el.find('.get_hijri').attr("value", "Young man");
                        var vnnn = self.$el.find('.get_hijri');
                        self.convert_greg_to_hijri(datetime);
                    }
                });
            } catch (e) {}

        },
        formatClient: function(value, type) {
            if (type == 'datetime') {
                var date_format = time.getLangDatetimeFormat();
            }
            if (type == 'date') {
                var date_format = time.getLangDateFormat();
            }
            return moment(value).format(date_format);
        },
        convert_greg_to_hijri: function(text) {
            if (text) {
                var cal_greg = $.calendars.instance('gregorian');
                var cal_hijri = $.calendars.instance('islamic');
                var text = text._i;
                if (text.indexOf('-') != -1) {
                    var lang_date_format = time.getLangDateFormat();
                    if (lang_date_format == 'MM-DD-YYYY') {
                        var text_split = text.split('-');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[1]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'DD-MM-YYYY') {
                        var text_split = text.split('-');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[1]);
                        var day = parseInt(text_split[0]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'YYYY-MM-DD') {
                        var text_split = text.split('-');
                        var year = parseInt(text_split[0]);
                        var month = parseInt(text_split[1]);
                        var day = parseInt(text_split[2]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'MM-YYYY-DD') {
                        var text_split = text.split('-');
                        var year = parseInt(text_split[1]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[2]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                }

                if (text.indexOf('/') != -1) {
                    var lang_date_format = time.getLangDateFormat();
                    if (lang_date_format == 'MM/DD/YYYY') {
                        var text_split = text.split('/');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[1]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'DD/MM/YYYY') {
                        var text_split = text.split('/');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[1]);
                        var day = parseInt(text_split[0]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'YYYY/MM/DD') {
                        var text_split = text.split('/');
                        var year = parseInt(text_split[0]);
                        var month = parseInt(text_split[1]);
                        var day = parseInt(text_split[2]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'MM/YYYY/DD') {
                        var text_split = text.split('/');
                        var year = parseInt(text_split[1]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[2]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                }
            }
        },
        _setValueFromUi: function() {
            var value = this.$input.val() || false;
            this.setValue(this._parseClient(value));

            var new_date = this.getValue();

            // @Jay: special fix for non English language date convert to English
            if (new_date && this.getValue().locale() != "en") {
                new_date = { '_i': new_date.locale('en').format('MM/DD/YYYY') };
            }
            this.convert_greg_to_hijri(new_date);
        },
        set_readonly: function(readonly) {
            this._super(readonly);
            this.$input_hijri.prop('readonly', this.readonly);
        },
        change_datetime: function(e) {
            this._setValueFromUi();
            this.trigger("datetime_changed");

            // Prevent to stop auto close filter popup to reopen
            // var $el = this.$el;
            // if ($el.closest('.o_filters_menu').length){
            //     setTimeout(function(){
            //         $('.o_filters_menu').parent().addClass('show');
            //         $('.o_filters_menu').addClass('show');
            //     }, 1000);
            // } else {
            //     this.trigger("datetime_changed");
            // }
        },
        changeDatetime: function() {
            if (this.__libInput > 0) {
                if (this.options.warn_future) {
                    this._warnFuture(this.getValue());
                }
                this.trigger("datetime_changed");
                return;
            }
            var oldValue = this.getValue();
            if (this.isValid()) {
                this._setValueFromUi();
                // this.set_value_from_ui();
                var newValue = this.getValue();
                var hasChanged = !oldValue !== !newValue;
                if (oldValue && newValue) {
                    var formattedOldValue = oldValue.format(time.getLangDatetimeFormat());
                    var formattedNewValue = newValue.format(time.getLangDatetimeFormat());
                    if (formattedNewValue !== formattedOldValue) {
                        hasChanged = true;
                    }
                }
                if (hasChanged) {
                    if (this.options.warn_future) {
                        this._warnFuture(newValue);
                    }
                    this.trigger("datetime_changed");
                }
            } else {
                var formattedValue = oldValue ? this._formatClient(oldValue) : null;
                this.$input.val(formattedValue);
            }
        },
    });

    datetimefield.FieldDate.include({
        start: function() {
            var self = this;
            var prom;
            if (this.mode === 'edit') {
                this.datewidget = this._makeDatePicker();
                this.datewidget.on('datetime_changed', this, function() {
                    var value = this._getValue();
                    if ((!value && this.value) || (value && !this._isSameValue(value))) {
                        this._setValue(value);
                    }
                });

                var date_value = this.value;
                if (this.datepickerOptions.defaultDate && this.datepickerOptions.defaultDate.locale() != 'en') {
                    var assign_dt = moment(date_value, 'DD MMM, YYYY').locale('ar');
                    date_value = assign_dt.locale("en").format('MM/DD/YYYY');
                }

                prom = this.datewidget.appendTo('<div>').then(function() {
                    self.datewidget.$el.addClass(self.$el.attr('class'));
                    self._prepareInput(self.datewidget.$input);
                    self._replaceElement(self.datewidget.$el);

                    if (date_value) {
                        if (date_value instanceof moment) {
                            date_value = date_value.format('MM/DD/YYYY');
                        }
                        var hij_date = self.convert_greg_to_hijri(date_value);

                        if (typeof(hij_date) == "undefined") {
                            self.datewidget.$el.find('.oe_hijri').val(date_value);
                            self.datewidget.$el.find('.oe_hijri').append("<div><span class='oe_hijri'>" + date_value + "</span></div>");
                        } else {
                            self.datewidget.$el.find('.oe_hijri').val(hij_date);
                            self.datewidget.$el.find('.oe_hijri').append("<div><span class='oe_hijri'>" + hij_date + "</span></div>");
                        }
                    }
                });
                return Promise.resolve(prom);
                //return Promise.resolve(prom).then(this._super.bind(this));
            }
            if (this.mode === 'readonly') {
                var date_value = this.value;
                if (this.datepickerOptions.defaultDate && this.datepickerOptions.defaultDate.locale() != 'en') {
                    var assign_dt = moment(date_value, 'DD MMM, YYYY').locale('ar');
                    date_value = assign_dt.locale("en").format('MM/DD/YYYY');
                }

                this.datewidget = this._makeDatePicker();
                prom = this.datewidget.appendTo('<div>').then(function() {
                    self.datewidget.$el.addClass(self.$el.attr('class'));
                    self._prepareInput(self.datewidget.$input);
                    self._replaceElement(self.datewidget.$el);
                    if (date_value) {
                        if (date_value instanceof moment) {
                            date_value = date_value.format('MM/DD/YYYY');
                        }
                        var hij_date = self.convert_greg_to_hijri(date_value);
                        if (typeof(hij_date) == "undefined") {
                            self.datewidget.$el.find('.oe_hijri').val(date_value);
                            self.datewidget.$el.find('.oe_hijri').append("<div><span class='oe_hijri'>" + date_value + "</span></div>");
                        } else {
                            self.datewidget.$el.find('.oe_hijri').val(hij_date);
                            self.datewidget.$el.find('.oe_hijri').append("<div><span class='oe_hijri'>" + hij_date + "</span></div>");
                        }
                        self.datewidget.$el.find('input').attr('disabled', 'disabled');
                    }
                });
                return Promise.resolve(prom);
            }
        },
        convert_greg_to_hijri: function(text) {
            if (text) {
                var cal_greg = $.calendars.instance('gregorian');
                var cal_hijri = $.calendars.instance('islamic');
                if (text.indexOf('-') != -1) {
                    var text_split = text.split('-');
                    var year = parseInt(text_split[0]);
                    var month = parseInt(text_split[1]);
                    var day = parseInt(text_split[2]);

                    var jd = cal_greg.toJD(year, month, day);
                    var date = cal_hijri.fromJD(jd);
                    var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                    var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                    return cal_hijri.formatDate('M d, yyyy', date);
                }

                if (text.indexOf('/') != -1) {
                    var text_split = text.split('/');
                    var year = parseInt(text_split[2]);
                    var month = parseInt(text_split[0]);
                    var day = parseInt(text_split[1]);

                    var jd = cal_greg.toJD(year, month, day);
                    var date = cal_hijri.fromJD(jd);
                    var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                    var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                    return cal_hijri.formatDate('M d, yyyy', date);
                }
            }
        },
    });

    ListRenderer.include({
        _renderBodyCell: function(record, node, colIndex, options) {
            var $cell = this._super.apply(this, arguments);
            var name = node.attrs.name;
            var field = this.state.fields[name];
            if (field) {
                if (field.type == 'datetime' || field.type == 'date' && options.mode == 'readonly') {
                    console.log('field',field);
                    var text = $cell.text();
                    var cal_greg = $.calendars.instance('gregorian');
                    var cal_hijri = $.calendars.instance('islamic');
                    if (text.indexOf('/') != -1) {
                        var text_split = text.split('/');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[1]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        var hijri_value = cal_hijri.formatDate('M d, yyyy', date);
                        var new_date = text + ' (' + hijri_value + ')';
                    }
                    if (field.name == 'dob_hijra') {
                        new_date = hijri_value;
                    }
                    else if (field.name == 'exp_date_istemara_hijry') {
                        new_date = hijri_value;
                    }
                    else {
                            new_date = text;
                        }

                    return $cell.text(new_date).attr('title', new_date);
                }
            }
            return $cell;
        },
    });

    FormController.include({
        _onSave: function(ev) {
            this._super(ev);
            $('.calendars-popup').hide();
            var datetime = moment(this.$el.find('.oe_hijri').val());
            var text = $('.oe_hijri').text();
            var hij_text = $('.get_hijri').text();
//        const result = await this._rpc({
//            model: 'client.vehicle.info',
//            method: 'assign_hijri_date',
//        });
//        this._rpc({
//                model: 'client.vehicle.info',
//                method: 'assign_hijri_date',
//                context: datetime._i,
//                }).then(function (res) {
//                this.displayNotification({ message: _t("The Line is Created!") });
//            });
        this._rpc({
                    model: 'client.vehicle.info',
                    method: 'write',
                    args: [this.initialState.data.id, {
                        'exp_date_istemara_hijry': datetime._i
                    }],
                })
//        this.$el.find('.exp_date_istemara_hijry').val('bbbbb');
//        this.initialState.data.exp_date_istemara_hijry = datetime._i;
//        $("input[name=exp_date_istemara_hijry]").val(datetime._i);
        },
//        val = this.$input_hijri.val();

    });

//    fieldRegistry.add('islamic_date', FieldIslamicDate);
//    return FieldIslamicDate;

});