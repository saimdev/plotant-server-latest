import stripe

def generate_token(card_number, expiration_month, expiration_year, cvv):
    stripe.api_key = 'pk_test_51Oad4rK9FJ9sxaqhWukm7uEPfivaSxs71WhRkmrJcxEw9w5ovPXnZp2usLL8Dgqw2Nwnoixu6Q6rKuoEr7sv4ZSu00aRqndBVQ'
    token_response = stripe.Token.create(
            card={
                'number': card_number,
                'exp_month': expiration_month,
                'exp_year': expiration_year,
                'cvc': cvv
            }
        )
    tokenId = token_response['id']

    return tokenId

















