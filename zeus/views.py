from django.shortcuts import render
from django.http import HttpResponse
import logging

from .controller import TokenController

logger = logging.getLogger("django.request")


def token(request):
    logger.info(request.GET['name'])
    return HttpResponse("123", content_type='text')
