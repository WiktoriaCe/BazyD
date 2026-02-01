"""
API endpoints and DRF-based viewsets have been removed from this module.
If you need to add non-API views (template views or helpers), add them here.
"""

from django.shortcuts import render

# API removed: this file is intentionally minimal to avoid exposing endpoints.


def placeholder(request):
    return render(request, "landing.html")
