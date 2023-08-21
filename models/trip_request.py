from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TripRequest(models.Model):
    _name = 'trip.request'
    _description = 'Trip Request'

    employee_id = fields.Many2one('hr.employee', string='Trip Employee', required=True,
                                  domain="[('contract_id.state', '=', 'open')]")
    destination_id = fields.Many2one('res.country', string='Destination', required=True)

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date')
    num_rest_days = fields.Integer(string='Number of Rest Days')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    last_change_user = fields.Many2one('res.users', string='Last Change User')
    trip_days = fields.Integer(compute='_compute_trip_days', string='Trip Days', store=True)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            allowed_destinations = self.employee_id.allowed_destination_ids.ids
            return {'domain': {'destination_id': [('id', 'in', allowed_destinations)]}}

    @api.depends('start_date', 'end_date')
    def _compute_trip_days(self):
        for request in self:
            if request.start_date and request.end_date:
                trip_days = (request.end_date - request.start_date).days + 1
                request.trip_days = max(0, trip_days)
            else:
                request.trip_days = 0

    # create date constraint
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for request in self:
            if request.start_date > request.end_date:
                raise ValidationError("End date should be greater than start date.")

    # rest day negative constraint
    @api.constrains('num_rest_days')
    def _check_rest_days(self):
        for request in self:
            if request.num_rest_days < 0:
                raise ValidationError("Number of rest days should be greater than zero.")



class Employee(models.Model):
    _inherit = 'hr.employee'

    trip_request_ids = fields.One2many('trip.request', 'employee_id', string='Trip Requests For Current Employee')
    allowed_destination_ids = fields.Many2many('res.country', string='Allowed Destinations')
