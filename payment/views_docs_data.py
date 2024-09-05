from drf_spectacular.utils import OpenApiExample

payment_retrieve_API_view_example = [
    OpenApiExample(
        'Пример ответа',
        description='Полное описание можете получить https://docs.stripe.com/api/checkout/sessions/retrieve',
        value={
            "id": "cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u",
            "object": "checkout.session",
            "after_expiration": None,
            "allow_promotion_codes": None,
            "amount_subtotal": 2198,
            "amount_total": 2198,
            "automatic_tax": {
                "enabled": False,
                "liability": None,
                "status": None
            },
            "billing_address_collection": None,
            "cancel_url": None,
            "client_reference_id": None,
            "consent": None,
            "consent_collection": None,
            "created": 1679600215,
            "currency": "usd",
            "custom_fields": [],
            "custom_text": {
                "shipping_address": None,
                "submit": None
            },
            "customer": None,
            "customer_creation": "if_required",
            "customer_details": None,
            "customer_email": None,
            "expires_at": 1679686615,
            "invoice": None,
            "invoice_creation": {
                "enabled": False,
                "invoice_data": {
                    "account_tax_ids": None,
                    "custom_fields": None,
                    "description": None,
                    "footer": None,
                    "issuer": None,
                    "metadata": {},
                    "rendering_options": None
                }
            },
            "livemode": False,
            "locale": None,
            "metadata": {},
            "mode": "payment",
            "payment_intent": None,
            "payment_link": None,
            "payment_method_collection": "always",
            "payment_method_options": {},
            "payment_method_types": [
                "card"
            ],
            "payment_status": "unpaid",
            "phone_number_collection": {
                "enabled": False
            },
            "recovered_from": None,
            "setup_intent": None,
            "shipping_address_collection": None,
            "shipping_cost": None,
            "shipping_details": None,
            "shipping_options": [],
            "status": "open",
            "submit_type": None,
            "subscription": None,
            "success_url": "https://example.com/success",
            "total_details": {
                "amount_discount": 0,
                "amount_shipping": 0,
                "amount_tax": 0
            },
            "url": "https://checkout.stripe.com/c/pay/cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u#fidkdWxOYHwnPyd1blpxYHZxWjA0SDdPUW5JbmFMck1wMmx9N2BLZjFEfGRUNWhqTmJ%2FM2F8bUA2SDRySkFdUV81T1BSV0YxcWJcTUJcYW5rSzN3dzBLPUE0TzRKTTxzNFBjPWZEX1NKSkxpNTVjRjN8VHE0YicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
        },

        response_only=True,  # signal that example only applies to responses
    ),
]