# -*- coding: utf-8 -*-
__author__ = 'Alan Hou'

from odoo.tests.common import TransactionCase


class LibraryTestCase(TransactionCase):

    def setUp(self):
        super(LibraryTestCase, self).setUp()
        demo_user = self.env.ref('base.user_demo')
        demo_user.groups_id |= self.env.ref('my_module.group_librarian')
        book_model = self.env['library.book'].sudo(demo_user)
        self.book = book_model.create(
            {'name': 'Test book',
             'state': 'draft',
             }
        )

    def test_change_draft_available(self):
        '''test changing state from draft to available'''
        self.book.change_state('available')
        self.assertEqual(self.book.state, 'available')

    def test_change_available_draft_no_effect(self):
        '''test forbidden state change from available to draft'''
        self.book.change_state('available')
        self.book.change_state('draft')
        self.assertEqual(
            self.book.state,
            'draft',
            'the state cannot change from %s to draft' % self.book.state
        )
