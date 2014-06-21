from django.shortcuts import RequestContext, loader, render
from django.template import loader

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User

from pprint import pprint
from datetime import datetime
import dateutil.parser as parser
from django.utils import timezone
# Create your views here.
from usermanagement.models import user_policy,devices,billboards,messages
# Create your views here.
import json
from django.utils import simplejson
#random get
import string,random


_SESSION_TIME=300

@csrf_exempt
def system_register(request):
    jsonMsg = request.POST['jsonMsg']
    json_req = json.loads(jsonMsg)
    try:
        active_session = request.session['billboard_session']
        return HttpResponse("Registration Session Already exists and had received a un / pw ")
    except:
        pprint("first time session has tried to register")
        
    
    pprint("Got Post Request ---k %s"%json_req['request'])
    if json_req['request'] == 'auto_register_device':
        pprint("register attempt - so create a new user for the device request")
        un = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        pw = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        pprint("register attempt - so create a new user for the device request %s %s"%(un,pw))
        user = User.objects.create_user(un, 'bloggins@cdnnavy.com', pw)
        response ={}
        response['un']=un
        response['pw']=pw
        response['error']="none"
        json_req['response']=response
        request.session['billboard_session']="active"
        return HttpResponse(json.dumps(json_req))
    elif json_req['request'] == 'manual_register_device':
        pprint("register attempt - so create a new user for the device request")
        response = {}
        try:
            un = json_req['un']
            pw = json_req['pw']
            email = json+req['email']
            pprint("register attempt - so create a new user for the device request %s %s"%(un,pw))
            user = User.objects.create_user(un, email, pw)
            response['success']=True
            request.session['billboard_session']="active"
        except:
            response['success']=False
       
        json_req['response']=response
        return HttpResponse(json.dumps(json_req))
    return HttpResponse("Registration Error")

@csrf_exempt
def system_login(request):
    pprint("login attempt")
    jsonMsg = request.POST['jsonMsg']
    json_req = json.loads(jsonMsg)
    pprint("Got Post Request ---k %s"%json_req['request'])
    if json_req['request'] == 'login_request':
        pprint("found a match")
        un = json_req['username']
        pw = json_req['password']
        pprint("auth %s %s"%(un,pw))
        user = authenticate(username=un, password=pw)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request,user)
                request.session.set_expiry(_SESSION_TIME)
                pprint("return success %s"%request.session.get_expiry_date())
                
                return HttpResponse("You are Logged in expires in %s"%request.session.get_expiry_date() );
            else:
                pprint("return fail1")
                return HttpResponse("Correct Login, but account has been disabled");
        else:
            # the authentication system was unable to verify the username and password
            pprint("return failt2")
            return HttpResponse("UN or PW is wrong");
    else:
        pprint("return fail3 match")
    return HttpResponse("JSON Error");
    

def _is_time_up(request):
    request.session.set_expiry(_SESSION_TIME)

@csrf_exempt
@login_required
def data(request):
    _is_time_up(request)
    jsonMsg = request.POST['jsonMsg']
    json_req = json.loads(jsonMsg)
    retstring = ""
    if json_req['request'] == "search_billboards":
        sLat = json_req['latitude']
        sLng=json_req['longitude']
        sLatRng=json_req['lat_rng']
        sLngRng=json_req['lng_rng']
        bb_context = RequestContext(request, {'billboards': billboards.objects.filter(lat__gt=(sLat-sLatRng),lat__lt=(sLat+sLatRng),lng__gt=(sLng-sLngRng),lng__lt=(sLng+sLngRng)).values('pk','owner','name','lat','lng') } )
        template = loader.get_template('usermanagement/jsons/billboards.json')
        retstring = template.render(bb_context)
    elif json_req['request'] == "get_billboard_messages":
        key = json_req['billboard_id']
        date_time = datetime.now()
        msgs=messages.objects.filter(billboard=key,stop_date__gt=date_time).values('text')
        msg_context = RequestContext(request, {'Messages':msgs } )
        template_msg = loader.get_template('usermanagement/jsons/messages.json')
        retstring = template_msg.render(msg_context)    
    elif json_req['request'] == "list_your_billboards":
        user_billboards = request.user.billboards_set.filter().values('pk','owner','name','lat','lng')
        bb_context = RequestContext(request, {'billboards': user_billboards } )
        template = loader.get_template('usermanagement/jsons/billboards.json')
        retstring = template.render(bb_context)
    elif json_req['request'] == "add_billboard":
        bb = billboards(owner=request.user,name=json_req['name'],lat=json_req['lat'],lng=json_req['lng'])
        bb.save()
        bb_context = RequestContext(request, {'billboards': [bb] } )
        pprint("almost there")
        template = loader.get_template('usermanagement/jsons/billboards.json')
        retstring = template.render(bb_context)
    elif json_req['request'] == 'add_msg_to_billboard':
        bb = billboards.objects.filter(pk=json_req['billboard_id'])
        pprint("ex date %s"%json_req['message']['exp_date'])
        msg = messages(owner=request.user,billboard=bb[0],text=json_req['message']['text'],start_date=datetime.now(),stop_date=parser.parse(json_req['message']['exp_date']) )
        msg.save()
        retstring="saved message to bb"
    elif json_req['request'] == 'remove_billboard':
        pprint("try to remove bb")
        #bb = billboards.objects.filter(pk=json_req['billboard_id'])
        bb = request.user.billboards_set.filter(pk=json_req['billboard_id'])
        bb.delete()
        retstring="bb removed ... maybe"
    elif json_req['request'] == 'update_billboard':
        pprint("try to update bb")
        #bb = billboards.objects.filter(pk=json_req['billboard_id'])
        bb = request.user.billboards_set.get(pk=json_req['billboard_id'])
        bb.name = json_req['name']
        bb.lat = json_req['lat']
        bb.lng = json_req['lng']
        bb.save()
        retstring="bb updated... maybe %s"%bb.name
    elif json_req['request'] == 'remove_msg_from_billboard':
        pprint("try to remove msg from bb")
        #bb = billboards.objects.filter(pk=json_req['billboard_id'])
        bb = request.user.billboards_set.filter(pk=json_req['billboard_id'])
        msg = request.user.messages_set.filter(billboard=bb[0],pk=json_req['message_id'])
        msg.delete()
        retstring="bb msg removed ... maybe"
    elif json_req['request'] == 'update_msg_on_billboard':
        pprint("try to update msg on bb")
        #bb = billboards.objects.filter(pk=json_req['billboard_id'])
        bb = billboards.objects.filter(pk=json_req['billboard_id'])
        msg = request.user.messages_set.filter(billboard=bb[0],pk=json_req['message_id'])
        #parser.parse(json_req['message']['exp_date'])
        msg.text = json_req['message']['text']
        msg.stop_date = parser.parse(json_req['message']['exp_date'])
        retstring="bb msg updated ... maybe"   
    elif json_req['request'] == "list_your_messages":
        user_messages = request.user.messages_set.filter().values('pk','owner','billboard','text','start_date','stop_date')
        bb_context = RequestContext(request, {'Messages': user_messages } )
        template = loader.get_template('usermanagement/jsons/messages.json')
        retstring = template.render(bb_context)
    return HttpResponse( "Got it %s ::: %s"%(jsonMsg,retstring) );

def index(request):
    template = loader.get_template('usermanagement/index.html')
    message = messages.objects.all()
    billboard = billboards.objects.all()
    user_pols = user_policy.objects.all()
    
    context =  RequestContext(request, {'Messages': message,'billboards': billboard,'users':user_pols})
    return HttpResponse(template.render(context))
