# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count, F
from django.shortcuts import render

from crawler import bl
from crawler import models
# Create your views here.


def index(request):
    res = file_upload(request)
    return render(request, 'crawler/upload.html', {'res': res})


def file_upload(request):
    if request.method == "POST" and request.FILES:
        file = request.FILES['document']
        filename = file.name

        if file.content_type != 'application/pdf':
            return bl.serializer({}, status=False)

        urls = bl.find_document_urls(file)
        created_urls = bl.store_data(filename, urls)

        return bl.serializer({'urls_created': len(created_urls), 'filename': filename})


def get_documents(request):
    if request.method != "GET":
        return {'status': False}

    data = list(models.URL.objects.values(
        'document_id',
    ).annotate(urls_count=Count('id'), document_name=F('document__name')))

    return bl.serializer(data)


def get_document_urls(request, document_name):
    if request.method != "GET":
        return {'status': False}

    data = list(models.URL.objects.filter(document__name=document_name).values_list('name', flat=True))
    return bl.serializer(data)


def get_all_urls(request):
    if request.method != "GET":
        return {'status': False}

    data = list(models.Document.objects.values(
        url_name=F('url__name'),
    ).annotate(document_count=Count('id')))

    return bl.serializer(data)
