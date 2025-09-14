from django.db import models

# Create your models here.


class Format(models.Model):
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

    name = models.CharField(max_length=50, choices=FORMAT_CHOICES, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Decks(models.Model):
    title = models.CharField(max_length=100)
    format = models.ForeignKey(
        Format, default='Jumpstart', on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, related_name='cards_in_deck')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
