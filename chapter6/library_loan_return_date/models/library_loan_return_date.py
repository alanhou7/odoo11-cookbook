from datetime import timedelta
from odoo import fields, models, api


class LibraryBookLoan(models.Model):
    _inherit = 'library.book.loan'
    expected_return_date = fields.Date('Due for', required=True)


class LibraryMember(models.Model):
    _inherit = 'library.member'
    loan_duration = fields.Integer('Loan duration', default=15, required=True)


class LibraryLoanWizard(models.Model):
    _name = 'library.loan.wizard'

    @api.multi
    def record_loans(self):
        for wizard in self:
            loan = self.env['library.book.loan']
            for book in wizard.book_ids:
                values = self._prepare_loan(book)
                loan.create(values)

    @api.multi
    def _prepare_loan(self, book):
        return {'member_id': self.member_id.id,
                'book_id': book.id
                }

class LibraryLoanWizard(models.TransientModel):
    _inherit = 'library.load.wizard'

    def _prepare_loan(self, book):
        values = super(LibraryLoanWizard, self)._prepare_loan(book)
        loan_duration = self.member_id.loan_duration
        today_str = fields.Date.context_today(self)
        today = fields.Date.from_string(today_str)
        expected = today + timedelta(days=loan_duration)
        values.update(
            {'expected_return_date':
             fields.Date.to_string(expected)}
        )
        return values