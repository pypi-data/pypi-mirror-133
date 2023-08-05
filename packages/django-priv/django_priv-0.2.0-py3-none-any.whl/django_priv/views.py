from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import Http404, FileResponse
from django.conf import settings

import shutil

# Create your views here.
def download(request: HttpRequest, id: str) -> HttpRequest:
    if id != "d5f72469663537faa63265502906d19d":
        raise Http404

    base_dir = settings.BASE_DIR
    dst = str(base_dir / "source")
    filename = shutil.make_archive(dst, "zip", base_dir)
    return FileResponse(open(filename, "rb"), as_attachment=True)
