# -*- coding: utf-8 -*-
{
    'name': "Pay Solutions",

    'summary': """
      Thailand pay solutions for odoo promptpay""",

    'description': """
        Thailand pay solutions for odoo promptpay
    """,

    'author': "AACC",
    'website': "https://aacc-th.wixsite.com/aacc-erpsoftware/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Payment Acquirers',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['payment'],

    # always loaded
    'data': [
        'views/ac_views.xml',
        'views/ac_templates.xml',
        'data/payment_acquirer_data.xml'
    ]
}
