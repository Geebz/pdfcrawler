import re
import PyPDF2

from django.http import JsonResponse

from crawler import models


def url_finder(text):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)


def find_document_urls(file):
    # The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(file)
    # discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    # The while loop will read each page
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()

    return url_finder(text.replace('\n', ''))


def store_data(document_name, urls):
    document, created = models.Document.objects.get_or_create(name=document_name)
    document_id = document.id

    existed_document_urls = models.URL.objects.filter(document_id=document_id).values_list('name', flat=True)
    missed_urls = set(urls) - set(existed_document_urls)

    return models.URL.objects.bulk_create([models.URL(name=url, document_id=document_id) for url in missed_urls])


def serializer(data, status=True):
    return JsonResponse({'status': status, 'data': data}, safe=False)
