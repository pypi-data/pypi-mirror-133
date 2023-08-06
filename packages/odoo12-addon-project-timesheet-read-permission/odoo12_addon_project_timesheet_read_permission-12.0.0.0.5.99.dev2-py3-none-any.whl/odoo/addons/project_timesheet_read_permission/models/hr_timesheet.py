from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket',
        domain=[("project_id", "!=", False)],
        groups=False,
    )
    ticket_partner_id = fields.Many2one(
        comodel_name='res.partner',
        related="ticket_id.partner_id",
        string="Ticket partner",
        store=True,
        compute_sudo=True,
        groups=False,
    )

    @api.onchange("ticket_id")
    def onchange_ticket_id(self):
        for record in self:
            if not record.ticket_id:
                continue
            record.project_id = record.ticket_id.project_id
            record.task_id = record.ticket_id.task_id
