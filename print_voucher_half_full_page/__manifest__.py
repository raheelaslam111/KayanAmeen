
{
    "name": 'Print Payment Receipt/Voucher in Half & Full Page',
    'version': '.12.13',
    'category': 'Sale',
        "author": 'Zero Systems',
        "company": 'Zero for Information Systems',
         "website": "https://www.erpzero.com",
        "email": "sales@erpzero.com",
	"sequence": 0,
    "summary": " print payment voucher and payment receipt in half page and full page paper format.",
    "description": """ 
half receipt half Customer Receipt
half receipt Print half Receipt Print half payment Receipt
Print Customer Receipt Print half Customer Receipt
Receipt and Payment Voucher Print(Payment Receipt)
Receipt & Payment Voucher Print receipt voucher Account Report
Supplier Purchase Payment Receipt 
Receipt / Payment Voucher Half & Full Page Print 
payment receipt Account Payment Receipt
Account Payment Receipt Customer Payment Report
Customer Payment Receipt Payment Details on Invoice Report
Invoice Report Account Voucher payment receipt Report payment receipt
Account Voucher Report payment receipt
Advance Payment Receipt print payment receipt
Multiple Invoice Payment Receipt / Payment Voucher Half & Full Page Print
                  """,
    "depends": ['base','account'],
    "data": [
            'report/full_payment_voucher.xml',
            'report/half_payment_voucher.xml',
            ],
	"auto_install": False,
	"installable": True,
	"application": False,
    'images': ['static/description/logo.PNG'],
	'license': 'LGPL-3',
    "price": 55,
    "currency": "USD",
}

