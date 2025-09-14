from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Card(models.Model):
    TYPES_CHOICES = [
        # Permanentes principales
        ("Land", "Land"),
        ("Creature", "Creature"),
        ("Enchantment", "Enchantment"),
        ("Artifact", "Artifact"),
        ("Planeswalker", "Planeswalker"),

        # Hechizos no permanentes
        ("Sorcery", "Sorcery"),
        ("Instant", "Instant"),

        # Tipos adicionales / especiales
        ("Battle", "Battle"),            # Nuevo (March of the Machine, 2023)
        ("Tribal", "Tribal"),
        ("Conspiracy", "Conspiracy"),
        ("Plane", "Plane"),
        ("Scheme", "Scheme"),
        ("Vanguard", "Vanguard"),
    ]

    name = models.CharField(max_length=100)
    mana_cost = models.CharField(max_length=20, blank=True, null=True)
    type_line = models.CharField(max_length=100, choices=TYPES_CHOICES)
    primary_type = models.CharField(max_length=50, blank=True, null=True)
    secondary_types = models.CharField(max_length=100, blank=True, null=True)
    box_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Deck(models.Model):
    FORMAT_CHOICES = [
        ('Standard', 'Standard'),
        ('Modern', 'Modern'),
        ('Legacy', 'Legacy'),
        ('Vintage', 'Vintage'),
        ('Jumpstart', 'Jumpstart'),
        ('Commander', 'Commander'),
        ('Premondern', 'Premondern'),
        ('Pioneer', 'Pioneer'),
        ('Historic', 'Historic'),
        ('Brawl', 'Brawl'),
        ('Pauper', 'Pauper'),
        ('Frontier', 'Frontier'),
        ('Old School', 'Old School'),
        ('Singleton', 'Singleton'),
        ('Two-Headed Giant', 'Two-Headed Giant'),
        ('Oathbreaker', 'Oathbreaker'),
        ('Momir Basic', 'Momir Basic'),
        ('Peasant', 'Peasant'),
        ('Canadian Highlander', 'Canadian Highlander'),
        ('Tiny Leaders', 'Tiny Leaders'),
        ('Epic', 'Epic'),
        ('Conspiracy', 'Conspiracy'),
        ('Planechase', 'Planechase'),
        ('Archenemy', 'Archenemy'),
        ('Vanguard', 'Vanguard'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    format = models.CharField(
        max_length=50, choices=FORMAT_CHOICES, unique=True, default='Jumpstart')
    cards = models.ManyToManyField(Card, related_name='cards_in_deck')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CardInDeck(models.Model):
    """
    Relación Deck <-> Card con cantidad.
    Una fila = 'esta carta aparece N veces en este deck'.
    """
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE, related_name='card_links')
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='deck_links')
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])

    class Meta:
        # impide duplicar la misma carta en un deck
        unique_together = [('deck', 'card')]
        verbose_name = 'Card in Deck'
        verbose_name_plural = 'Cards in Deck'

    def __str__(self):
        return f"{self.card} x{self.quantity} in {self.deck}"


# Declara el ManyToMany a través de la tabla intermedia
Deck.add_to_class(
    'cards',
    models.ManyToManyField(Card, through=CardInDeck,
                           related_name='decks', blank=True)
)
