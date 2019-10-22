from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

from .models import (
    Book,
    Member,
)
from .utils import validate_book_data

# Create your views here.
def home(req):
    context = {
    }
    return render(req, "lms/home.html", context=context)


def about(req):
    context = {
    }
    return render(req, "lms/about.html", context=context)

def book_list(req):
    books = Book.objects.all()

    context = {
        'books': books
    }
    return render(req, "lms/book_list.html", context=context)

def member_list(req):
    members = [
        {
            "id": 1,
            "name": "Shisihr",
            "e_mail": "shishir@example.com",
            "bio": "I Am The Boss"
        },
        {
            "id":2,
            "name":"Taukir",
            "e_mail": "taukir@example.com",
            "bio":"I Am Donkey"
        }
    ]


    context = {

            'members': members
    }
    return render (req,"lms/member_list.html",context=context)

def addbook(request):
    if request.method == 'GET':
        context = {
        }
        return render(request, "lms/add_book.html", context=context)
    else:
        assert request.method == 'POST'
        # TODO: process the form, validate it, save into db and report to the user - on failure report error.
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        return HttpResponse(f"""
Title: {title}
Author: {author}
Description: {description}
""")

class AddBookView(View):
    def get(self, request):
        context = {
            'errors': {}
        }
        return render(request, "lms/add_book.html", context=context)

    def post(self, request):
        # TODO: process the form, validate it, save into db and report to the user - on failure report error.
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        # TODO: validate - pure python validator
        errors = validate_book_data(request.POST)
        if errors:
            context = {
                'errors': errors
            }
            return render(request, "lms/add_book.html", context=context)
        else:
            book = Book()
            book.title = title
            book.author = author
            book.description = description
            book.save()
            messages.add_message(request, messages.INFO, f'Saved successfully with id {book.id}, title {book.title}')
            return redirect('add-book')
