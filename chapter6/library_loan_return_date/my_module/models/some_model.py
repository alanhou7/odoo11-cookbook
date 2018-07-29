# -*- coding: utf-8 -*-
__author__ = 'Alan Hou'

import os
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SomeModel(models.Model):
    _name = 'some.model'
    data = fields.Text('Data')

    @api.multi
    def save(self, filename):
        if '/' in filename or '\\' in filename:
            raise UserError('Illegal filename %s' % filename)
        path = os.path.join('/opt/exports', filename)
        try:
            with open(path, 'w') as fobj:
                for record in self:
                    fobj.write(record.data)
                    fobj.write('\n')
        except (IOError, OSError) as exc:
            message = _('Unable to save file: %s') % exc
            raise UserError(message)

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
        def predicate(partner):
            if partner.email:
                return True
            return False

        return partners.filter(predicate)

    @api.model
    def partners_with_email(self, partners):
        return partners.filter(lambda p: p.email)
        # return partners.filter('email')

    @api.model
    def get_email_addresses(self, partner):
        partner.ensure_one()
        return partner.mapped('child_ids.email')

    @api.model
    def get_companies(self, partners):
        return partners.mapped('parent_id')