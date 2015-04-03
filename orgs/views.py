# Authors: Noah Gold, Jaspreet Singh

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from models import OrgData, OrgAlreadyExistsException
from users.models import UserData
from pageitforward.utils import createErrorDict
import json


@require_GET
@login_required
def APIOrgsGet(request, orgID):
    orgs = OrgData.objects.filter(pk=orgID)
    if orgs.count() == 1 and request.user.org == orgs[0]:
        return JsonResponse({'org': orgs[0].toDict(),
                             'error': None})
    else:
        return JsonResponse({'error':
                            createErrorDict(title='Invalid org ID.')})


@require_GET
@login_required
def APIOrgMembers(request, orgID):

    # Try to get the org
    orgs = OrgData.objects.filter(pk=orgID)
    if orgs.count() == 1 and request.user.org == orgs[0]:

        # Get the users
        users = UserData.objects.filter(org=orgs[0])
        retUsers = []
        for user in users:
            retUsers.append({'id': user.pk,
                             'firstName': user.firstName,
                             'lastName': user.lastName})
        return JsonResponse({'users': retUsers, 'error': None})
    else:
        return JsonResponse({'error':
                            createErrorDict(title='Invalid org ID.')})


@require_POST
@login_required
def APIOrgsPost(request):
    try:
        # Is the user in an org?
        if request.user.org is None:
            orgName = json.loads(request.body)['orgName']
            org = OrgData.createOrg(orgName)
            request.user.org = org
            request.user.save()
            return JsonResponse({'org': org.toDict(), 'error': None})
        else:
            return JsonResponse({'error':
                                 createErrorDict(
                                     title='User already in an org.',
                                     details=request.user.org.pk)})
    except (KeyError, ValueError):
        return JsonResponse({'error':
                             createErrorDict(title='Invalid parameters.')})
    except OrgAlreadyExistsException:
        return JsonResponse({'error':
                             createErrorDict(title='Org already exists.')})

@require_POST
@login_required
def APIJoinOrg(request):
    try:
        # Is the user in an org?
        if request.user.org is None:
            orgName = json.loads(request.body)['orgName']
            org = OrgData.objects.filter(orgName=orgName)
            # Org not Found
            if len(org) == 0:
                return JsonResponse({'error': createErrorDict(
                        title='User trying to join imaginary organization',
                        details=request.user.org)})
            else:
                request.user.org = org[0]
                request.user.save()
                return JsonResponse({'org': org[0].toDict(), 'error': None})
        else:
            return JsonResponse({'error':
                                 createErrorDict(
                                     title='User already in an org.',
                                     details=request.user.org.pk)})
    except (KeyError, ValueError):
        return JsonResponse({'error':
                             createErrorDict(title='Invalid parameters.')})