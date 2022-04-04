from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import User



def geco_index(request):
  # Authenticated users view their index page
  if request.user.is_authenticated:
      return render(request, "geco/index.html", {
          "user_id": request.user.id,
      })

  # Everyone else is prompted to sign in
  else:
      return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("geco_index"))

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("geco_index"))
        else:
            return render(request, "geco/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "geco/login.html")


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse("geco_index"))


def register(request):

  if request.user.is_authenticated:
      return HttpResponseRedirect(reverse("geco_index"))

  if request.method == "POST":
      username = request.POST["username"]
      email = request.POST["email"]

      # Ensure password matches confirmation
      password = request.POST["password"]
      confirmation = request.POST["confirmation"]
      if password != confirmation:
          return render(request, "geco/register.html", {
              "message": "Passwords must match."
          })

      # Attempt to create new user
      try:
          user = User.objects.create_user(username, email, password)
          user.save()
      except IntegrityError:
          return render(request, "geco/register.html", {
              "message": "Username already taken."
          })
      login(request, user)
      return HttpResponseRedirect(reverse("geco_index"))
  else:
      return render(request, "geco/register.html")