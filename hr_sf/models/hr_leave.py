
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    include_holidays = fields.Boolean()


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    @api.model
    def create(self, values):
        res = super(HrLeave, self).create(values)
        if not res.sudo().employee_id.contract_id or res.sudo().employee_id.contract_id.state != 'open':
            raise UserError(
                _('This Employee Contract not in running state'),
            )
        return res

    include_holidays = fields.Boolean(invisible=1)
    old_employee_no = fields.Char(related="employee_id.old_employee_number")
    x_employee_code = fields.Char('Old Employee Number')

    @api.onchange('date_from', 'date_to', 'employee_id', 'include_holidays','holiday_status_id')
    def _onchange_leave_dates(self):
        if self.date_from and self.date_to:
            self.number_of_days = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)['days']
            if self.holiday_status_id.include_holidays:
                count = 0.0
                if self.employee_id and self.employee_id.resource_calendar_id:
                    day_count = (self.date_to - self.date_from).days + 1
                    for i in (self.date_from + timedelta(n) for n in range(day_count)):
                        day = int(i.strftime("%w")) - 1
                        if day == -1:
                            day = 6
                        day = str(day)
                        days = []
                        for x in self.employee_id.resource_calendar_id.attendance_ids:
                            if x.dayofweek == str(day) and x.day_period == 'morning':
                                days.append(x.dayofweek)
                        if not day in days:
                            count = count + 1.0
                self.number_of_days = self.number_of_days + count
        else:
            self.number_of_days = 0

class HrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    x_employee_code = fields.Char('Old Employee Number')
