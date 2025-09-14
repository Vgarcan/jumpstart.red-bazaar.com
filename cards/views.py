from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Decks, Cards

# Create your views here.

# ? READ
# get all decks view


class PostListView(ListView):
    """Displays a list of posts."""
    model = Decks
    template_name = "cards/decks_list.html"
    context_object_name = "decks"  # Custom context variable
    ordering = ['-created_at']  # Order by latest posts first
    paginate_by = 5  # Show 5 posts per page

# get single deck view


class PostDetailView(DetailView):
    """Displays a single post's details."""
    model = Cards
    template_name = "cards/deck_detail.html"
    context_object_name = "post"


# ? CREATE
# create deck view
class PostCreateView(CreateView):
    """Creates a new post."""
    model = Decks
    template_name = "cards/deck_form.html"
    fields = ['title', 'content']  # Fields to include in the form
    success_url = reverse_lazy('post_list')  # Redirect after success

# ? UPDATE
# update deck view


class PostUpdateView(UpdateView):
    """Updates an existing post."""
    model = Decks
    template_name = "cards/deck_form.html"
    fields = ['title', 'content']  # Fields to include in the form
    success_url = reverse_lazy('post_list')  # Redirect after success

# ? DELETE
# delete deck view


class PostDeleteView(DeleteView):
    """Deletes an existing post."""
    model = Decks
    template_name = "cards/deck_confirm_delete.html"
    success_url = reverse_lazy('post_list')  # Redirect after success


# delete all decks view
class PostDeleteAllView(DeleteView):
    """Deletes all existing posts."""
    model = Decks
    template_name = "cards/deck_confirm_delete_all.html"
    success_url = reverse_lazy('post_list')  # Redirect after success

# delete all cards in a deck view


class PostDeleteAllCardsView(DeleteView):
    """Deletes all cards in a deck."""
    model = Decks
    template_name = "cards/deck_confirm_delete_all_cards.html"
    success_url = reverse_lazy('post_list')  # Redirect after success


# delete single card in a deck view
class PostDeleteCardView(DeleteView):
    """Deletes a single card in a deck."""
    model = Card
    template_name = "cards/deck_confirm_delete_card.html"
    success_url = reverse_lazy('post_list')  # Redirect after success

# ? EXTRA
