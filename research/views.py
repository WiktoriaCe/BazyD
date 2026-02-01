"""API removed

The Django REST Framework based API (viewsets/serializers/routers) was removed per project maintainer request.
Files previously containing viewsets and serializers were replaced with informative placeholders.
Models and Django Admin remain intact.
"""

from django.shortcuts import render, get_object_or_404

# No API viewsets defined in this module.

from .models import Documentation


def documentation_detail(request, pk):
    """Public read-only view to display a single Documentation entry."""
    doc = get_object_or_404(Documentation, pk=pk)
    return render(request, "documentation_detail.html", {"doc": doc})
