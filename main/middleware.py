from django.http import HttpResponse, HttpResponseRedirect
from main.models import *
import re


class AuthMiddleware:
    def process_request(self, request):
        # pour supprimer les résidus de sessions expirées TODO peut etre à faire dans un thread
        request.user = None
        request.session.clear_expired()
        if request.path_info == "/" and request.POST.get('username', 'false') != 'false' \
                and request.POST.get('password', 'false') != 'false':
            # reinitialise la session et les cookies
            request.session.flush()
            filter_users = User.objects.filter(username=request.POST.get('username'),
                                               password=request.POST.get('password'))
            if (len(filter_users) > 0):
                current_user = filter_users[0]

                # pour que la session et les cookies expirent quand l'utilisateur ferme son navigateur TODO peut etre à modifier
                request.session.set_expiry(0)

                request.user = current_user

                request.session['username'] = current_user.username

                return HttpResponseRedirect('/')
            else:
                request.session['bad_login'] = True
                return HttpResponseRedirect('.')
        if request.session.get('username', None) != None:
            filter_users = User.objects.filter(username=request.session.get('username', ''))
            if (len(filter_users) > 0):
                request.user = filter_users[0]

                # on vérifie que l'utilisateur n'essaye pas d'accéder à une page interdite
                if(type(request.user) != Admin):
                    if(re.compile('^/admin').match(request.path_info)):
                        return HttpResponseRedirect('/')
                if(type(request.user) != Teacher):
                    if(re.compile('^/teacher').match(request.path_info)):
                        return HttpResponseRedirect('/')
                return None
            else:
                request.session.flush()
                return HttpResponseRedirect('/')
        else:
            if (request.path_info != "/"):
                return HttpResponseRedirect('/')
            else:
                return None
