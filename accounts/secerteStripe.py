import stripe

def initiate_payment(total_payment, tokenId):
    stripe.api_key = 'sk_test_51Oad4rK9FJ9sxaqhsEvY59vJpSptxiw5BxSuYOzF608SkhQABn5lO90C8wnbxFvRETDC4l2n8f693ZKuJg9rCpiK00O6rFN1pU'
    payment = stripe.Charge.create(
            amount= int(total_payment)*100,         
            currency='usd',
            description='Example charge',
            source=tokenId,
            )
    if payment['paid']:
        return True
    else:
        return False
