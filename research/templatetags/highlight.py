from django import template
from django.utils.safestring import mark_safe
import re
import html

register = template.Library()

@register.filter(is_safe=True)
def highlight(text, query):
    """Podświetla fragmenty `query` w `text` używając <mark> (case-insensitive).
    Zwraca bezpieczny HTML (escaped + <mark> wokół dopasowań).
    """
    if not query or not text:
        return text
    try:
        s = str(text)
        escaped = html.escape(s)
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        def repl(m):
            return f"<mark>{m.group(0)}</mark>"
        highlighted = pattern.sub(repl, escaped)
        return mark_safe(highlighted)
    except Exception:
        return text
