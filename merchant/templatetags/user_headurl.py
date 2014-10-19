from django import template
from photos.models import *

register = template.Library()

def getuserheadurl(value, headtype):
    heads = Head.objects.filter(username = value)
    print
    if len(heads) == 0:
        print("$$$$yes, i'm custom filter: zero heads 0 len")
        full_url = ''.join([settings.DOMAIN, '/media/head/default.jpg'])
    else:
        head = list(heads)[-1]
        print("##username:", value)
        print("###head len:", len(heads))
        if headtype == 'orig':
            full_url = ''.join([settings.DOMAIN, head.head_orig.url])
        elif headtype == 'thumbnail':
            full_url = ''.join([settings.DOMAIN, head.head_thumbnail.url])
            print("$$$$yes, i'm custom filter, full url:", full_url)
    return full_url
    

register.filter("getuserheadurl", getuserheadurl) 
