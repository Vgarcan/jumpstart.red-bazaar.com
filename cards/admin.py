# admin.py
from django.contrib import admin
from .models import Card, Deck, CardInDeck


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'mana_cost', 'type', 'subtypes',
                    'created_at')
    search_fields = ('name', 'type', 'subtypes', 'mana_cost')
    ordering = ('type', 'mana_cost', 'name')
    fieldsets = (
        (None,
         {'fields':
             ('name', 'mana_cost')
          }
         ),
        ('Types',
         {'fields':
             ('type', 'subtypes')
          }
         ),
        ('Description',
         {'fields':
             ('box_description',)
          }
         ),
        ('Timestamps',
         {'fields':
             ('created_at',),
             'classes':
                 ('collapse',)
          }
         ),
    )
    readonly_fields = ('created_at',)


class CardInDeckInline(admin.TabularInline):
    model = CardInDeck              # <- usa el through con quantity
    extra = 1
    autocomplete_fields = ('card',)  # opcional, útil si hay muchas cartas
    fields = ('card', 'quantity')   # <- aquí editas cantidad


class DeckAdmin(admin.ModelAdmin):   # (puedes renombrar desde DecksAdmin a DeckAdmin)
    list_display = ('title', 'format', 'created_at', 'updated_at')
    search_fields = ('title', 'format')
    ordering = ('-created_at',)
    inlines = [CardInDeckInline]
    exclude = ('cards',)            # evita el widget M2M cuando usas Inline
    fieldsets = (
        (None, {'fields': ('title', 'format', 'description')}),
        ('Timestamps', {'fields': ('created_at',
         'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Card, CardAdmin)
admin.site.register(Deck, DeckAdmin)
