def split_card_description(card):
    return [part.strip() for part in card.cardDetail.split('Or.') if part.strip()]

def role_display_names(role):
    return role.replace('_', ' ').title()