from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

u = User.objects.first()
print('USER', bool(u), getattr(u, 'id', None))
if not u:
    print('No users present')
else:
    url = reverse('person_detail', args=[u.id])
    print('REVERSED URL:', url)
    c = Client()
    resp = c.get(url)
    print('STATUS:', resp.status_code)
    if resp.status_code != 200:
        print('CONTENT SNIPPET:', resp.content[:800])
