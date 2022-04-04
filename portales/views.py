from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Page, Design

# Create your views here.
def portales_index(request):

  # Authenticated users view their index page
  if request.user.is_authenticated:

      # Get pages
      pages = Page.objects.filter(user=request.user)

      # Get last design 
      design = Design.objects.filter(user=request.user).last()

      if(not design):
          desing = Design.objects.create(user=request.user, url=f'mi_portal_{request.user.username}')
          return HttpResponseRedirect(reverse("portales_index"))

      return render(request, "portales/index.html", {
          "user_id": request.user.id,
          "pages": pages,
          "design": design,
      })

  # Everyone else is prompted to sign in
  else:
      return HttpResponseRedirect(reverse("login"))


@csrf_exempt
# Show new page form
def new_page(request):

    # Get last design 
    design = Design.objects.filter(user=request.user).last()

    # If the method is POST
    if request.method == "POST":

        # Get data
        title = request.POST.get("title")
        body = request.POST.get("body")

        try:
            # Create new page
            new_page = Page.objects.create(user=request.user, title=title, body=body, design=design)
            new_page.save()
        except:
            return render(request, "portales/new_page.html", {
                "message": "Something was wrong, please  try again.",
                "design": design,
            }) 

        return HttpResponseRedirect(reverse("portales_index"))

    return render(request, "portales/new_page.html", {
        "design": design,
    })



# Show page content
def show_page(request, page_id):

    # Get last design 
    design = Design.objects.filter(user=request.user).last()

    if request.method == "GET":

        try:
            # Get page data
            page = Page.objects.get(id=page_id, user=request.user)

        except Page.DoesNotExist:
            # If page doesn't exist
            return render(request, "portales/show_page.html", {
                "message": "ERROR 404: Page not found.",
                "design": design,
            })

        # Show page
        return render(request, "portales/show_page.html", {
            "page": page,
            "design": design,
        })
    
    # If method is not GET
    return render(request, "portales/show_page.html", {
        "message": "Request method need to be GET.",
        "design": design,
    })


# Edit the given page 
def edit_page(request, page_id):

    # Get last design 
    design = Design.objects.filter(user=request.user).last()

    try:
        page = Page.objects.get(id=page_id, user=request.user)
    
    except Page.DoesNotExist:
        return render(request, "portales/edit_page.html", {
            "message": "ERROR 404: Page not found.",
            "design": design,
        })

    if request.method == "POST":

        # Get data
        title = request.POST.get("title")
        body = request.POST.get("body")

        # Change page content and save
        page.title = title
        page.body = body
        page.save()

        # Show page updated
        return HttpResponseRedirect(reverse("show_page", args=(page.id,)))

    elif request.method == "GET":
        # Show editor
        return render(request, "portales/edit_page.html", {
            "page": page,
            "design": design,
        })

    else: 
        # If method is not GET or POST
        return render(request, "portales/show_page.html", {
            "message": "Request method should be GET or POST.",
            "design": design,
        })        


# Delete the given page
def delete_page(request, page_id):

    # Get last design 
    design = Design.objects.filter(user=request.user).last()

    try:
        page = Page.objects.get(id=page_id, user=request.user)
    
    except Page.DoesNotExist:
        return render(request, "portales/edit_page.html", {
            "message": "ERROR 404: Page not found. Can't delete this page.",
            "design": design,
        })

    # Delete the page
    page.delete()

    # Show index page
    return HttpResponseRedirect(reverse("portales_index"))


# Edit portal's design
def edit_design(request):

    if request.method == "POST":

        # Get data
        url = request.POST.get("url")

        # Create object
        try:
            design = Design.objects.create(user=request.user, url=url)
            design.save()
        except:
            return render(request, "portales/edit_design.html", {
                "message": "Something was wrong, please  try again.",
                "design": design,
            })
            
        # Change pages design
        pages = Page.objects.filter(user=request.user)

        for page in pages:
            page.design = design
            page.save()

        return render(request, "portales/edit_design.html", {
            "design": design,
            "message": "Design successfully updated."
        })

    # Get last design 
    design = Design.objects.filter(user=request.user).last()

    return render(request, "portales/edit_design.html", {
        "design": design,
    })


# Update changes 
@csrf_exempt
def upload_changes(request):

    if request.method == "POST":

        # Update 'active' field from pages
        try:
            pages = Page.objects.filter(user=request.user)
        except Page.DoesNotExist:
            return JsonResponse({"message": "Error 404: Page not found."}, status=404)

        try:
            for page in pages:
                page.active = True
                page.save()
        except:
            return JsonResponse({"message": "Error 500: Something went wrong, please try again."}, status=500)
    else:
        return JsonResponse({"message": "Error 500: POST method is requerid."}, status=500)

    return JsonResponse({"message": "success"})
    

# Recuperar las páginas del portal y mostrarlas en el portal.

# Se puede agregar un campo "subido" al modelo de cada página para diferenciar entre las páginas que
# deben mostrarse y las que no.