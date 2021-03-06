#coding: utf-8
import re
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model # If used custom user mode
from django.db.models import Q

from django.shortcuts import render_to_response
from django.template import RequestContext

User = get_user_model()


def search(request):
    query_string = ''
    found_entries = None
    if ('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET['search']

        entry_query = get_query(query_string, ['title', 'content',])

        found_entries = User.objects.filter(entry_query)

    return render_to_response('search_page.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    '''

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]



def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query