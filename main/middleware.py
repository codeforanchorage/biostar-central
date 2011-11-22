import datetime
from django.contrib.auth import logout
from django.contrib import messages

class LastVisit(object):
    """
    Updates the last visit stamp at MINIMUM_TIME intervals
    """
    # minimum elapsed time
    MINIMUM_TIME = 60 * 5 # every 5 minutes

    def process_request(self, request):
        
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            
            if profile.suspended:
                logout(request)
                messages.error(request, 'Sorry, this account has been suspended. Please contact the administrators.')
                return None
            
            now = datetime.datetime.now()
            diff = (now - profile.last_visited).seconds
            
            # Prevent writing to the database too often
            if diff > self.MINIMUM_TIME:
                profile.last_visited = now
                profile.save()
    
        return None


class PermissionsMiddleware(object):
    ''' Calculates the logged-in user's permissions and adds it to the request object. '''
    def process_request(self, request):
        pass