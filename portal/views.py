from django.shortcuts import render
from portales.models import Page, Design

# Show portal
def portal_index(request, portal_url):

  # Get design for requested pages
  design = Design.objects.filter(url=portal_url).last()
  print(design)

  # Get requested pages
  pages = Page.objects.filter(design=design, active=True)

  return render(request, "portal/index.html", {
    "pages": pages,
    "design": design,
  })

# Show page
def portal_show_page(request, portal_url, page_id):

    # Get design
    design = Design.objects.filter(url=portal_url).last()

    if request.method == "GET":

        try:
            # Get data
            page = Page.objects.get(id=page_id)

        except Page.DoesNotExist:
            # If page doesn't exist
            return render(request, "portal/show_page.html", {
                "message": "ERROR 404: Page or design not found.",
                "design": design,
            })

        # Show page
        return render(request, "portal/show_page.html", {
            "page": page,
            "design": design,
        })
    
    # If method is not GET
    return render(request, "portal/show_page.html", {
        "message": "Request method need to be GET.",
        "design": design,
    })