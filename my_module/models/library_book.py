from datetime import timedelta
from odoo import models, fields, api
from odoo.fields import Date as fDate


class LibraryBook(models.Model):
	_name = 'library.book'
	_description = 'Library Book Description'
	_order = 'date_release desc,name'
	_inherit = ['base.archive']
	name = fields.Char('Title', required=True)
	date_release = fields.Date('Release Date')
	author_ids = fields.Many2many(
		'res.partner',
		string='Authors'
	)
	short_name = fields.Char(
			'Short Title',
			size=100,
			translate=False,
			required=True
	)
	notes = fields.Text('Internal Notes')
	state = fields.Selection(
			[('draft', 'Not Available'),
			('available', 'Available'),
			('lost', 'Lost')],
			'State'
	)
	description = fields.Html(
			'Description',
			sanitize=True,
			strip_style=False,
			translate=False
	)
	cover = fields.Binary('Book Cover')
	out_of_print = fields.Boolean('Out of Print?')
	date_updated = fields.Datetime('Last Updated')
	pages = fields.Integer(
			'Number of Pages',
			default=0,
			help='Total book page count',
			groups='base.group_user',
			states={'lost': [('readonly', True)]},
			copy=True,
			index=False,
			readonly=False,
			required=False,
			company_dependent=False
	)
	reader_rating = fields.Float(
			'Reader Average Rating',
			digits=(14, 4)
	)
	active = fields.Boolean('Active', default=True)
	from odoo.addons import decimal_precision as dp
	cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
	currency_id = fields.Many2one('res.currency', string='Currency')
	retail_price = fields.Monetary('Retail Price')
	_rec_name = 'short_name'
	publisher_id = fields.Many2one(
		'res.partner', 
		string='Publisher',
		ondelete='set null', # restrict, cascade
		context={},
		domain={}
	)
	age_days = fields.Float(
		string = 'Days Since Release',
		compute = '_compute_age',
		inverse = 'inverse_age',
		search = '_search_age',
		store = False,
		compute_sudo = False
	)
	publisher_city = fields.Char(
		'Publisher City',
		related = 'publisher_id.city',
		readonly = True
	)
	ref_doc_id = fields.Reference(
		selection = '_referencable_models',
		string = 'Reference Document'
	)

#	 def name_get(self):
#	 	result = []
#		for record in self:
#			result.append(
#			(
#				record.id,
#				"%s (%s)" % (record.name, record.date_release)
#			))
#		return result

	@api.constrains('date_release')
	def _check_release_date(self):
		for record in self:
			if(record.date_release and record.date_release > fields.Date.today()):
				raise models.ValidationError('Release date must be the past')

	@api.depends('date_release')
	def _compute_age(self):
		today = fDate.from_string(fDate.today())
		for book in self.filtered('date_release'):
			delta = (today - fDate.from_string(book.date_release))
			book.age_days = delta.days

	def _inverse_age(self):
		today = fDate.from_string(fDate.context_today(self))
		for book in self.filtered('date_release'):
			d = today - timedelta(days=book.age_days)
			book.date_release = fDate.to_string(d)

	def _search_age(self, operator, value):
		today = fDate.from_string(fDate.context_today(self))
		value_days = timedelta(days=value)
		value_date = fDate.to_string(today - value_days)
		operator_map = {
			'>': '<', '>=': '<=',
			'<': '>', '<=': '>='
		}
		new_op = operator_map.get(operator, operator)
		return [('date_release', new_op, value_date)]
	
	@api.model
	def _referencable_models(self):
		models = self.env['res.request.link'].search([])
		return [(x.object, x.name) for x in models]


class ResPartner(models.Model):
	_inherit = 'res.partner'
	_order = 'name'
	published_book_ids = fields.One2many(
		'library.book',
		'publisher_id',
		string = 'Published Books'
	)
	authored_book_ids = fields.Many2many(
		'library.book',
		string='Authored Books'
	)
	count_books = fields.Integer(
		'Number of Authored Books',
		compute = '_compute_count_books'
	)

	@api.depends('authored_book_ids')
	def _compute_count_books(self):
		for r in self:
			r.count_books = len(r.authored_book_ids)


class BaseArchive(models.AbstractModel):
	_name = 'base.archive'
	active = fields.Boolean(defautl=True)

	def do_archive(self):
		for record in self:
			record.active = not record.active


class LibraryMemeber(models.Model):
	_name = 'library.member'
	_inherits = {'res.partner': 'parent_id'}
	partner_id = fields.Many2one(
		'res.partner',
		ondelete = 'cascade'
	)
	date_start = fields.Date('Member Since')
	date_end = fields.Date('Termination Date')
	member_number = fields.Char()
	date_of_birth = fields.Date('Date of Birth')
