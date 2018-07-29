# -*- coding: utf-8 -*-
__author__ = 'Alan Hou'

from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    cr.execute('ALTER TABLE library_book RENAME COLUMN date_release TO date_release_char')
    # env = api.Environment(cr, SUPERUSER_ID, {})
    # env holds all currently loaded models