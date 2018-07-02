from odoo import fields, models, api


class ResPartner(models.Model):
    _name = 'res.partner'
    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean(
        'Is a company',
        help = "Check if the contact is a company, "
            "otherwise it is a person"
    )
    parent_id = fields.Many2one('res.partner', 'Related Company')
    child_ids = fields.One2many('res.partner', 'parent_id',
                                'Contacts')

    def some_method(self):
        today_str = fields.Date.context_today(self)
        val1 = {'name': 'Eric Idle',
                'email': 'eric.idle@example.com',
                'date': today_str}
        val2 = {'name': 'John Cleese',
                'email': 'john.cleese@example.com',
                'date': today_str}
        partner_val = {
            'name': 'Flying Circus',
            'email': 'm.python@example.com',
            'date': today_str,
            'is_company': True,
            'child_ids': [(0, 0, val1),
                          (0, 0, val2)]
        }
        record = self.env['res.partner'].create(partner_val)
        return record

    @api.model
    def add_contacts(self, partner, contacts):
        partner.ensure_one()
        if contacts:
            # partner.date = fields.Date.context_today(self)
            # partner.child_ids |= contacts
            today = fields.Date.context_today(self)
            partner.update(
                {'date': today,
                'child_ids': partner.child_ids | contacts}
            )

    @api.model
    def find_partners_and_contacts(self, name):
        partner = self.env['res.partner']
        domain = ['|',
                  '&',
                  ('is_company', '=', True),
                  ('name', 'like', name),
                  '&',
                  ('is_company', '=', False),
                  ('parent_id.name', 'like', name)
                  ]
        return partner.search(domain)

    @api.model
    def partners_with_email(self, partners):
        # return partners.filter(lambda p: p.email)
        def predicate(partner):
            if partner.email:
                return True
            return False
        return partners.filter(predicate)

    @api.model
    def get_email_addresses(self, partner):
        return partner.mapped('child_ids.email')

    @api.model
    def get_companies(self, partners):
        if __name__ == '__main__':
            return partners.mapped('parent_id')

