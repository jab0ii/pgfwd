# Authors: Feiyang Xue, Noah Gold
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from pageitforward.utils import createErrorDict
from users.models import UserData, ContactMethodData


@require_GET
def APILoginStatus(request):
    if request.user.is_authenticated():
        userPCM = request.user.toUserPCM().toDict()
        return JsonResponse({'loggedIn': True, 'userPCM': userPCM})
    else:
        return JsonResponse({'loggedIn': False})


@login_required
def APIContactMethodUpdateDelete(request, contactMethodID):
    contactMethod = ContactMethodData.objects.filter(pk=contactMethodID)

    # Users can only update/delete their own CMs
    if contactMethod.count() == 1 and contactMethod[0].user == request.user:
        contactMethod = contactMethod[0]

        if request.method == 'POST':
            jsonData = json.loads(request.body)
            contactMethod.contactType = jsonData['contactType']
            contactMethod.contactData = jsonData['contactData']
            contactMethod.title = jsonData['title']
            contactMethod.priority = jsonData['priority']
            contactMethod.save()
            return JsonResponse({'success': True, 'error': None})

        elif request.method == 'DELETE':
            contactMethod.delete()
            return JsonResponse({'success': True, 'error': None})

        else:
            return JsonResponse({'error':
                                createErrorDict(title='Invalid verb.')})

    else:
        return JsonResponse({'error':
                            createErrorDict(title='Invalid CM.')})


@login_required
def APIContactMethods(request):
    if request.method == 'GET':
        userPCM = request.user.toUserPCM()
        contactMethods = [method.toDict() for method in userPCM.contactMethods]
        return JsonResponse({'contactMethods': contactMethods, 'error': None})
    elif request.method == 'POST':
        jsonData = json.loads(request.body)
        ContactMethodData.objects.create(
            title=jsonData['title'],
            contactType=jsonData['contactType'],
            contactData=jsonData['contactData'],
            user=request.user,
            priority = jsonData['priority'])
        return JsonResponse({'success': True, 'error': None})
    else:
        return JsonResponse({'error': createErrorDict(title='Invalid verb.')})


@require_POST
def APILogin(request):

    jsonData = json.loads(request.body)
    user = authenticate(username=jsonData['username'],
                        password=jsonData['password'])

    # Login the user and return their user data
    if user is not None and user.is_active:
        login(request, user)
        userPCMDict = user.toUserPCM().toDict()
        return JsonResponse({'userPCM': userPCMDict, 'error': None})
    else:
        return JsonResponse({'error': createErrorDict(
                            title='Invalid username/pw.')})


@login_required
@require_POST
def APILogout(request):
    logout(request)
    return JsonResponse({'success': True, 'error': None})


@require_POST
def APIUsers(request):
    jsonData = json.loads(request.body)

    if UserData.objects.filter(email=jsonData['email']).count() == 0:
        user = UserData.createUser(jsonData['firstName'],
                                   jsonData['lastName'],
                                   jsonData['email'],
                                   jsonData['password'])
        userPCMDict = user.toUserPCM().toDict()
        user = authenticate(username=jsonData['email'],
                            password=jsonData['password'])
        login(request, user)
        return JsonResponse({'userPCM': userPCMDict, 'error': None})
    else:
        return JsonResponse({'error': createErrorDict(
            title='User already exists.')})
