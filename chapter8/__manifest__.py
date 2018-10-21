{
    'name': 'My Module',
    'summary': 'My module summary demo',
    'description': '''Long description demo
            second line''',
    'author': 'Alan Hou',
    'license': "AGPL-3",
    'website': 'https://alanhou.org',
    'category': 'Demo Module',
    'version': '0.1',
    'application': True,
    'data': [
        'views/library_book.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        # 'data/res_partner.xml',
        'data/res_partner.yml'
    ],
    'demo': [
        'data/demo.xml',
        # 'data/demo.yml'
    ],
    'depends': ['base', 'decimal_precision', 'product', 'stock']
}
