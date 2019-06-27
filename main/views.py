from main import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json


@login_required(login_url='/admin/')
def index(request):
    with open('json_data/main.json') as json_file:
        params = json.load(json_file)

    return render(request, "report.html", params)