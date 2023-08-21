{
    'name': 'Trip Request',
    'summary': " Customers Contract Summmary ",
    'version': '1.0',
    'author': "Itqan Systems",
    'website': "http://www.itqansystems.com",
    'category': 'Trip Request Category',
    'depends': [
        'base',
        'hr',
    ],
    'description': 'Odoo module for managing trip requests.',
    'data': [
        # Security files:
        'security/res_groups.xml',
        'security/group_access_rights.xml',
        'security/ir.model.access.csv',

        # Data files:

        # Root menu items files:

        # View files:
        'views/trip_request_views.xml',
        'views/employee_views.xml',
        'views/report_trip_request.xml',

        # Menu items files:
    ],
}
