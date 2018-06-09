from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import databasequeries


def home(request):
    return render(request, 'lifeInvaderHome.html')

def login(request):
    return render(request, 'lifeInvaderLogin.html')

def signup(request):
    return render(request, 'lifeInvaderSignup.html')

@csrf_exempt
def success(request):
    print("Success was called.")
    name = request.POST.get('uname', '')
    email = request.POST.get('uemail', '')
    password = request.POST.get('upassword', '')
    print(name, email, password)


    return render(request, 'lifeInvaderSucess.html',
        {'name': name}
    )

def profile(request):
    user_data = databasequeries.get_info_from_id(id)


@csrf_exempt
def user_login(request):

    email = request.POST.get('umail', '')
    password = request.POST.get('upassword', '')
    # print(email, password)

    status = ''
    status, user_id = databasequeries.login_check(email, password)
    request.session['user_id'] = user_id

    if status:
        return render(request, 'lifeInvaderLogin.html',
            {'status': status }
        )

    print("Logged.")
    return show_profile(request)


@csrf_exempt
def show_profile(request):
    id = request.session['user_id']
    print("Logged user with id: ", id)

    posts = databasequeries.get_posts(id, id)
    name, age, email = databasequeries.get_info_from_id(id)
    friends = databasequeries.get_friends(id)
    groups = databasequeries.get_groups(id)

    return render(request, 'lifeInvaderProfile.html',
    {'name':name,
    'age':age,
    'email':email,
    'posts':posts,
    'friends':friends,
    'groups':groups})

def show_timeline(request):
    print("Timelining with id ", request.session['user_id'])
    id = request.session['user_id']

    name, age, email = databasequeries.get_info_from_id(id)
    friends = databasequeries.get_friends(id)
    groups = databasequeries.get_groups(id)
    posts = databasequeries.get_timeline_posts(id)
    all_users = databasequeries.get_all_users(id)
    all_groups = databasequeries.get_all_groups()

    return render(request, 'lifeInvaderTimeline.html',
    {'name':name,
    'age':age,
    'email':email,
    'posts':posts,
    'friends':friends,
    'groups':groups,
    'all_users':all_users,
    'all_groups':all_groups})
    #ok

def visit_profile(request, id):


    posts = databasequeries.get_posts(id, id)
    name, age, email = databasequeries.get_info_from_id(id)
    friends = databasequeries.get_friends(id)
    groups = databasequeries.get_groups(id)

    return render(request, 'lifeInvaderProfile.html',
    {'name':name,
    'age':age,
    'email':email,
    'posts':posts,
    'friends':friends,
    'groups':groups})
