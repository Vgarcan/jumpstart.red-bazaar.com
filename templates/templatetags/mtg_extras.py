from django import template
import re

register = template.Library()

@register.filter
def parse_mana_cost(mana_cost):
    """
    Parse mana cost string like '{3}{W}{W}' into individual symbols
    Returns a list of symbols: ['3', 'W', 'W']
    """
    if not mana_cost:
        return []
    
    # Extract symbols from {symbol} format
    symbols = re.findall(r'\{([^}]+)\}', mana_cost)
    return symbols

@register.filter
def mana_symbol_class(symbol):
    """
    Convert mana symbol to CSS class for mana font
    """
    symbol_map = {
        'W': 'ms-w',
        'U': 'ms-u', 
        'B': 'ms-b',
        'R': 'ms-r',
        'G': 'ms-g',
        'C': 'ms-c',
        'X': 'ms-x',
    }
    
    # Handle numbers
    if symbol.isdigit():
        return f'ms-{symbol}'
    
    # Handle hybrid mana (like W/U)
    if '/' in symbol:
        return f'ms-{symbol.lower().replace("/", "")}'
    
    return symbol_map.get(symbol, f'ms-{symbol.lower()}')

@register.filter
def card_type_icon(card_type):
    """
    Return appropriate icon for card type
    """
    type_icons = {
        'Creature': 'fas fa-fist-raised',
        'Instant': 'fas fa-bolt',
        'Sorcery': 'fas fa-scroll',
        'Enchantment': 'fas fa-magic',
        'Artifact': 'fas fa-cog',
        'Planeswalker': 'fas fa-crown',
        'Land': 'fas fa-mountain',
    }
    
    for card_type_key, icon in type_icons.items():
        if card_type_key.lower() in card_type.lower():
            return icon
    
    return 'fas fa-question'

@register.filter
def color_name(color_code):
    """
    Convert color code to full name
    """
    color_names = {
        'W': 'White',
        'U': 'Blue', 
        'B': 'Black',
        'R': 'Red',
        'G': 'Green',
    }
    return color_names.get(color_code, color_code)

@register.filter
def widthratio(value, max_value, scale):
    """
    Calculate width ratio for progress bars
    """
    try:
        return int((float(value) / float(max_value)) * float(scale))
    except (ValueError, ZeroDivisionError):
        return 0