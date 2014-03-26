from django.shortcuts import RequestContext, loader

from django.http import HttpResponse


from pprint import pprint
# Create your views here.
from usermanagement.models import users,devices,billboards,messages
# Create your views here.
def data(request):
    pprint("Got Post Request")
    jsonMsg = request.POST['jsonMsg']
    json_req = json.loads(jsonMsg)
    
    # get Post Data json string for filter and ordering
    # return new table
    return HttpResponse("Got Message %s"%jsonMsg)

def index(request):
    template = loader.get_template('usermanagement/index.html')
    #get table data - all of it
    message = messages.objects.all()
    billboard = billboards.objects.all()
    user = users.objects.all()
    #pprint("who ra ")
    #pprint(data)
    context =  RequestContext(request, {'messages': message,'billboards': billboard,'users':user})
    return HttpResponse(template.render(context))
