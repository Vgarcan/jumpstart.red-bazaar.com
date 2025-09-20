# MTG Collection Manager - Django Templates

A comprehensive set of Django templates and partials for managing Magic: The Gathering deck collections. Built with Bootstrap 5 and designed to work seamlessly with the [Magic: The Gathering API](https://magicthegathering.io/).

## 📁 Project Structure

```
templates/
├── base.html                    # Base template with Bootstrap setup
├── home.html                    # Landing page with statistics
├── deck_list.html              # Main deck collection view
├── deck_detail.html            # Individual deck details
├── partials/                   # Reusable components
│   ├── navbar.html             # Navigation bar
│   ├── breadcrumb.html         # Breadcrumb navigation
│   ├── filters.html            # Deck filtering system
│   ├── deck_card.html          # Individual deck card
│   ├── deck_stats.html         # Deck statistics display
│   ├── deck_export.html        # Export and sharing options
│   ├── color_badges.html       # MTG color identity badges
│   ├── mana_cost.html          # Mana cost with icons
│   ├── mana_curve.html         # Mana curve visualization
│   ├── rarity_badge.html       # Card rarity badges
│   ├── card_detailed.html      # Detailed card information
│   ├── card_list_table.html    # Card list in table format
│   ├── card_grid.html          # Card list in grid format
│   └── card_search.html        # Advanced card search
└── templatetags/
    ├── __init__.py
    └── mtg_extras.py           # Custom template tags
```

## 🚀 Quick Start

1. **Copy the templates folder** to your Django project
2. **Install template tags** by adding the templatetags folder to your app
3. **Add required URLs** to your Django urlpatterns
4. **Configure your views** to pass the expected context variables

### Required Django Settings

```python
# settings.py
INSTALLED_APPS = [
    # ... your apps
    'your_app_name',  # App containing the templatetags
]
```

### Required URLs

```python
# urls.py
urlpatterns = [
    path('', views.home, name='home'),
    path('decks/', views.deck_list, name='deck_list'),
    path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('decks/<int:deck_id>/export/<str:format>/', views.deck_export, name='deck_export'),
]
```

## 📋 Template Usage Guide

### Base Template (`base.html`)

The foundation template that includes:
- Bootstrap 5.3.2 CSS/JS
- Font Awesome 6.4.0 icons
- Mana Font for MTG symbols
- Global utility functions

**Blocks available:**
- `{% block title %}` - Page title
- `{% block extra_css %}` - Additional CSS
- `{% block content %}` - Main content
- `{% block extra_js %}` - Additional JavaScript

### Home Page (`home.html`)

Landing page with statistics and features showcase.

**Required context variables:**
```python
context = {
    'total_decks': int,
    'total_cards': int,
    'formats_count': int,
    'mythic_count': int,
    'recent_decks': QuerySet,  # Recent deck objects
}
```

### Deck List (`deck_list.html`)

Main collection view with filtering and pagination.

**Required context variables:**
```python
context = {
    'decks': QuerySet,  # Deck objects
    'is_paginated': bool,
    'page_obj': Page,  # Django pagination object
    'show_advanced_search': bool,  # Optional
}
```

### Deck Detail (`deck_detail.html`)

Individual deck view with complete information.

**Required context variables:**
```python
context = {
    'deck': Deck,  # Deck object
    'cards': QuerySet,  # Card objects in deck
    'deck_stats': dict,  # Statistics breakdown
    'mana_curve': dict,  # Mana cost distribution
    'max_mana_count': int,  # For mana curve scaling
    'breadcrumbs': list,  # Navigation breadcrumbs
}
```

## 🧩 Partials Reference

### Navigation Components

#### `navbar.html`
Main navigation bar with responsive design.
```django
{% include 'partials/navbar.html' %}
```

#### `breadcrumb.html`
Breadcrumb navigation for deep pages.
```django
{% include 'partials/breadcrumb.html' with breadcrumbs=breadcrumbs %}
```

### Deck Components

#### `deck_card.html`
Individual deck card for grid layouts.
```django
{% include 'partials/deck_card.html' with deck=deck %}
```

**Expected deck object fields:**
- `name`, `description`, `format`, `total_cards`
- `colorIdentity`, `average_cmc`, `image_url`

#### `deck_stats.html`
Visual statistics breakdown by card type.
```django
{% include 'partials/deck_stats.html' with stats=deck_stats %}
```

**Expected stats structure:**
```python
deck_stats = {
    'creatures': int,
    'instants': int,
    'sorceries': int,
    'lands': int,
}
```

#### `deck_export.html`
Export and sharing functionality.
```django
{% include 'partials/deck_export.html' with deck=deck %}
```

### Card Components

#### `card_detailed.html`
Complete card information with image.
```django
{% include 'partials/card_detailed.html' with card=card %}
```

**Expected card object fields (from MTG API):**
- `name`, `manaCost`, `cmc`, `type`, `text`
- `power`, `toughness`, `rarity`, `set`, `artist`
- `imageUrl`, `quantity`

#### `card_list_table.html`
Card list in table format.
```django
{% include 'partials/card_list_table.html' with cards=cards %}
```

#### `card_grid.html`
Card list in visual grid format.
```django
{% include 'partials/card_grid.html' with cards=cards %}
```

### MTG-Specific Components

#### `mana_cost.html`
Renders mana cost with official MTG icons.
```django
{% include 'partials/mana_cost.html' with mana_cost=card.manaCost %}
```

**Input format:** `"{3}{W}{W}"` → Displays as mana symbols

#### `color_badges.html`
MTG color identity badges.
```django
{% include 'partials/color_badges.html' with colors=deck.colorIdentity %}
```

**Expected colors:** List of color codes `['W', 'U', 'B', 'R', 'G']`

#### `rarity_badge.html`
Card rarity with appropriate styling.
```django
{% include 'partials/rarity_badge.html' with rarity=card.rarity %}
```

#### `mana_curve.html`
Visual mana curve with progress bars.
```django
{% include 'partials/mana_curve.html' with mana_curve=mana_curve max_count=max_mana_count average_cmc=deck.average_cmc %}
```

### Utility Components

#### `filters.html`
Deck filtering system.
```django
{% include 'partials/filters.html' %}
```

#### `card_search.html`
Advanced card search form.
```django
{% include 'partials/card_search.html' %}
```

## 🏷️ Custom Template Tags

### MTG Extras (`mtg_extras.py`)

Load in templates:
```django
{% load mtg_extras %}
```

#### `parse_mana_cost`
Converts mana cost string to symbol list.
```django
{{ card.manaCost|parse_mana_cost }}
```

#### `mana_symbol_class`
Returns CSS class for mana symbols.
```django
{{ symbol|mana_symbol_class }}
```

#### `card_type_icon`
Returns Font Awesome icon for card types.
```django
{{ card.type|card_type_icon }}
```

#### `color_name`
Converts color code to full name.
```django
{{ 'W'|color_name }}  <!-- Returns "White" -->
```

#### `widthratio`
Calculates width ratios for progress bars.
```django
{% widthratio count max_count 100 %}
```

## 🎨 Styling Philosophy

These templates use **Bootstrap classes exclusively** for structure and layout. All visual styling is handled by Bootstrap's utility classes, making it easy to override with custom CSS.

### Key Bootstrap Components Used:
- **Grid System**: `container`, `row`, `col-*`
- **Cards**: `card`, `card-body`, `card-header`
- **Badges**: `badge`, `bg-*` variants
- **Buttons**: `btn`, `btn-*` variants
- **Forms**: `form-control`, `form-select`, `input-group`
- **Navigation**: `navbar`, `breadcrumb`, `pagination`
- **Utilities**: `d-*`, `text-*`, `bg-*`, `m-*`, `p-*`

### Customization Tips:
1. **Override Bootstrap variables** in your CSS
2. **Add custom classes** alongside Bootstrap classes
3. **Use CSS specificity** to override default styles
4. **Maintain responsive behavior** when customizing

## 🔧 Customization Guide

### Adding New Partials

1. **Create new partial** in `templates/partials/`
2. **Follow naming convention**: `component_name.html`
3. **Document required context** in comments
4. **Use Bootstrap classes** for structure
5. **Include in main templates** with `{% include %}`

### Modifying Existing Partials

1. **Identify the partial** you want to modify
2. **Check dependencies** - which templates include it
3. **Maintain context variable names** for compatibility
4. **Test responsive behavior** after changes
5. **Update documentation** if context changes

### Adding Custom Template Tags

1. **Add functions** to `templatetags/mtg_extras.py`
2. **Use `@register.filter`** decorator
3. **Handle edge cases** and None values
4. **Document usage** in docstrings
5. **Test with various inputs**

## 🌐 API Integration

These templates are designed for the [Magic: The Gathering API](https://magicthegathering.io/).

### Key API Fields Used:
- `name`, `manaCost`, `cmc`, `colors`, `colorIdentity`
- `type`, `types`, `subtypes`, `supertypes`
- `rarity`, `set`, `text`, `artist`
- `power`, `toughness`, `imageUrl`
- `multiverseid`, `number`, `layout`

### Sample API Response Handling:
```python
# In your views.py
def process_api_card(api_card):
    return {
        'name': api_card.get('name'),
        'manaCost': api_card.get('manaCost', ''),
        'cmc': api_card.get('cmc', 0),
        'type': api_card.get('type', ''),
        'rarity': api_card.get('rarity', ''),
        'imageUrl': api_card.get('imageUrl'),
        # ... other fields
    }
```

## 📱 Responsive Design

All templates are fully responsive using Bootstrap's grid system:

- **Mobile First**: Designed for mobile, enhanced for desktop
- **Breakpoints**: `sm`, `md`, `lg`, `xl`, `xxl`
- **Flexible Grids**: Cards adapt to screen size
- **Touch Friendly**: Large tap targets on mobile
- **Readable Text**: Appropriate font sizes for all devices

## 🔍 SEO Considerations

- **Semantic HTML**: Proper heading hierarchy
- **Alt Tags**: Images include descriptive alt text
- **Meta Tags**: Title blocks for each page
- **Structured Data**: Ready for JSON-LD implementation
- **Clean URLs**: SEO-friendly URL patterns expected

## 🚀 Performance Tips

1. **Lazy Loading**: Add `loading="lazy"` to card images
2. **Image Optimization**: Use appropriate image sizes
3. **Caching**: Cache deck statistics and mana curves
4. **Pagination**: Limit cards per page for large decks
5. **CDN**: Use CDN for Bootstrap and Font Awesome

## 🐛 Troubleshooting

### Common Issues:

**Mana symbols not showing:**
- Check Mana Font CDN link in base.html
- Verify `parse_mana_cost` template tag is loaded

**Bootstrap styles not applying:**
- Confirm Bootstrap CDN link is correct
- Check for CSS conflicts with custom styles

**Template tags not working:**
- Ensure templatetags folder is in your app
- Add `{% load mtg_extras %}` to templates
- Check Django app is in INSTALLED_APPS

**Images not loading:**
- Verify imageUrl field from API
- Add fallback images for missing cards
- Check CORS settings for external images

## 📄 License

These templates are provided as-is for educational and development purposes. Bootstrap, Font Awesome, and Mana Font have their own respective licenses.

---

**Need help?** Check the Magic: The Gathering API documentation at https://docs.magicthegathering.io/