from models import db, MarketplaceItem, UserPurchase

def initialize_marketplace():
    existing_items = MarketplaceItem.query.count()
    if existing_items > 0:
        return
    
    themes = [
        {
            'name': 'Ocean Blue Theme',
            'description': 'Calming blue tones inspired by the ocean',
            'item_type': 'theme',
            'cost': 100,
            'theme_data': '{"primary": "#0077be", "secondary": "#4FC3F7", "background": "#E1F5FE"}',
            'icon': '🌊',
            'required_level': 1
        },
        {
            'name': 'Forest Green Theme',
            'description': 'Natural green shades from the forest',
            'item_type': 'theme',
            'cost': 150,
            'theme_data': '{"primary": "#2E7D32", "secondary": "#66BB6A", "background": "#E8F5E9"}',
            'icon': '🌲',
            'required_level': 3
        },
        {
            'name': 'Sunset Orange Theme',
            'description': 'Warm sunset colors for a cozy feel',
            'item_type': 'theme',
            'cost': 200,
            'theme_data': '{"primary": "#E65100", "secondary": "#FF9800", "background": "#FFF3E0"}',
            'icon': '🌅',
            'required_level': 5
        },
        {
            'name': 'Purple Royalty Theme',
            'description': 'Elegant purple hues fit for royalty',
            'item_type': 'theme',
            'cost': 250,
            'theme_data': '{"primary": "#6A1B9A", "secondary": "#AB47BC", "background": "#F3E5F5"}',
            'icon': '👑',
            'required_level': 7
        },
        {
            'name': 'Midnight Dark Theme',
            'description': 'Sleek dark mode for night owls',
            'item_type': 'theme',
            'cost': 300,
            'theme_data': '{"primary": "#263238", "secondary": "#546E7A", "background": "#37474F"}',
            'icon': '🌙',
            'required_level': 10
        },
        {
            'name': 'Cherry Blossom Theme',
            'description': 'Delicate pink sakura aesthetics',
            'item_type': 'theme',
            'cost': 350,
            'theme_data': '{"primary": "#E91E63", "secondary": "#F48FB1", "background": "#FCE4EC"}',
            'icon': '🌸',
            'required_level': 12
        },
        {
            'name': 'Gold Premium Theme',
            'description': 'Luxurious gold accents for elite users',
            'item_type': 'theme',
            'cost': 500,
            'theme_data': '{"primary": "#FFB300", "secondary": "#FFD54F", "background": "#FFF8E1"}',
            'icon': '✨',
            'required_level': 15
        }
    ]
    
    for theme_data in themes:
        item = MarketplaceItem(
            name=theme_data['name'],
            description=theme_data['description'],
            item_type=theme_data['item_type'],
            cost=theme_data['cost'],
            theme_data=theme_data['theme_data'],
            icon=theme_data['icon'],
            required_level=theme_data['required_level']
        )
        db.session.add(item)
    
    db.session.commit()

def get_available_items(user_level):
    return MarketplaceItem.query.filter(
        MarketplaceItem.is_available == True,
        MarketplaceItem.required_level <= user_level
    ).all()

def get_user_purchases(user_id):
    return UserPurchase.query.filter_by(user_id=user_id).all()

def has_purchased(user_id, item_id):
    return UserPurchase.query.filter_by(
        user_id=user_id,
        item_id=item_id
    ).first() is not None

def purchase_item(user_id, item_id, user_gamification):
    item = MarketplaceItem.query.get(item_id)
    if not item:
        return False, "Item not found"
    
    if user_gamification.level < item.required_level:
        return False, f"Requires level {item.required_level}"
    
    if has_purchased(user_id, item_id):
        return False, "Already purchased"
    
    if user_gamification.health_points < item.cost:
        return False, "Not enough points"
    
    user_gamification.health_points -= item.cost
    
    purchase = UserPurchase(
        user_id=user_id,
        item_id=item_id
    )
    db.session.add(purchase)
    db.session.commit()
    
    return True, "Purchase successful"
