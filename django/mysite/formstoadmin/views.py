from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RequestForm

# Create your views here.


@login_required
def index(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Request submitted')
            form.save()

    else:
        form = RequestForm()
    return render(request, 'formstoadmin/index.html', {'form': form})
