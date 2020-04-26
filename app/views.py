"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .forms import NoteForm
from .models import Note


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    notes = Note.objects.filter(is_deleted=False)
    return render(
        request,
        'app/index.html',
        {
            'title': 'My Notes',
            'year': datetime.now().year,
            'notes': notes
        }
    )


def note_detail(request, pk):
    """Renders the note detail page."""
    assert isinstance(request, HttpRequest)
    note = get_object_or_404(Note, pk=pk)
    return render(
        request,
        'app/note_detail.html',
        {
            'title': 'Note Detail',
            'year': datetime.now().year,
            'note': note
        }
    )


def create_note(request):
    """Renders the create note page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.create()
            return redirect("home")
    else:
        form = NoteForm
        return render(
            request,
            'app/create_note.html',
            {
                'title': 'New Note',
                'year': datetime.now().year,
                'form': form
            }
        )


def edit_note(request, pk):
    """Renders the edit note page."""
    assert isinstance(request, HttpRequest)

    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.edit()
            return redirect("home")
    else:
        form = NoteForm(instance=note)
        return render(
            request,
            'app/edit_note.html',
            {
                'title': 'Edit Note',
                'year': datetime.now().year,
                'form': form,
                'id': note.id
            }
        )


def delete_note(request, pk):
    """deletes note and return to home page."""
    assert isinstance(request, HttpRequest)

    note = get_object_or_404(Note, pk=pk)
    note.delete()

    return redirect("home")


