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
    pic = request.POST.get('pic','')

    user_info = databasequeries.register(name, email, password, pic)
    if user_info == 'deny':
        return render(request, 'lifeInvaderSignup.html',
            {'msg': "That e-mail is already in use. Choose another one."}
        )

    request.session['user_id'] = user_info

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

    posts = databasequeries.get_posts(id, "U")
    name, age, email, pic = databasequeries.get_info_from_id(id)
    friends = databasequeries.get_friends(id)
    groups = databasequeries.get_groups(id)
    friends_requests = databasequeries.get_requests(id)

    who = 'self'

    return render(request, 'lifeInvaderProfile.html',
    {'name':name,
    'age':age,
    'email':email,
    'pic':pic,
    'posts':posts,
    'friends':friends,
    'groups':groups,
    'requests':friends_requests,
    'who':who})

@csrf_exempt
def show_timeline(request):
    print("Timelining with id ", request.session['user_id'])
    id = request.session['user_id']

    try:
        post_text = request.POST.get('post_text', '')
        post_img = request.POST.get('pic', '')
        if(post_text != ''):
            databasequeries.post(id, id, "U", post_text, post_img);

    except Exception as e:
        print(e)

    name, age, email, pic = databasequeries.get_info_from_id(id)
    friends = databasequeries.get_friends(id)
    groups = databasequeries.get_groups(id)
    posts = databasequeries.get_timeline_posts(id)
    all_users = databasequeries.get_all_users(id)
    all_groups = databasequeries.get_all_groups()

    return render(request, 'lifeInvaderTimeline.html',
    {'name':name,
    'age':age,
    'email':email,
    'pic':pic,
    'posts':posts,
    'friends':friends,
    'groups':groups,
    'all_users':all_users,
    'all_groups':all_groups})


@csrf_exempt
def visit_profile(request, id):

    user_id = request.session['user_id']

    if id == request.session['user_id']:
        return show_profile(request)

    else:
        request.session['someoneelse_id'] = id

        try:
            post_text = request.POST.get('post_text', '')
            post_img = request.POST.get('pic', '')
            if(post_text != ''):
                databasequeries.post(user_id, id, "U", post_text, post_img);

        except Exception as e:
            print(e)


        posts = databasequeries.get_posts(id, "U")
        name, age, email, pic = databasequeries.get_info_from_id(id)
        friends = databasequeries.get_friends(id)
        groups = databasequeries.get_groups(id)
        status = databasequeries.is_friend(request.session['user_id'], id)
        print(request.session['user_id'], id, "are", status)

        who = id

        return render(request, 'lifeInvaderProfile.html',
        {'name':name,
        'age':age,
        'email':email,
        'pic':pic,
        'posts':posts,
        'friends':friends,
        'groups':groups,
        'who':who,
        'status':status})


def remove_friend(request):

    user_id = request.session['user_id']
    who = request.session['someoneelse_id']

    databasequeries.remove_friend(user_id, who)

    return visit_profile(request, who)


def add_friend(request):

    user_id = request.session['user_id']
    who = request.session['someoneelse_id']

    databasequeries.add_friend(user_id, who)

    return visit_profile(request, who)

def acc_friend(request, id):

    user_id = request.session['user_id']

    status = databasequeries.acc_friend(user_id, id)

    return show_profile(request)


def ref_friend(request, id):

    user_id = request.session['user_id']

    status = databasequeries.ref_friend(user_id, id)

    return show_profile(request)


def group_manager(request):

    id = request.session['user_id']
    groups = databasequeries.get_groups(id)
    not_member_groups = databasequeries.get_groups(id, "yes")


    return render(request, 'lifeInvaderProfileGroups.html',
    {'groups':groups,
    'nmgroups':not_member_groups})

@csrf_exempt
def visit_group(request, id):

    user_id = request.session['user_id']

    request.session['group_id'] = id

    try:
        post_text = request.POST.get('post_text', '')
        post_img = request.POST.get('pic', '')
        if(post_text != ''):
            databasequeries.post(user_id, id, "G", post_text, post_img);

    except Exception as e:
        print(e)

    name, pic = databasequeries.get_group_info(id)
    posts = databasequeries.get_posts(id, "G")
    members = databasequeries.get_members(id)
    relation = databasequeries.relation_group(user_id, id)

    return render(request, 'lifeInvaderGroup.html',
    {'name':name,
    'pic':pic,
    'posts':posts,
    'members':members,
    'relation':relation})


def members_manager(request):

    user_id = request.session['user_id']
    id = request.session['group_id']
    members = databasequeries.get_members(id)
    requests = databasequeries.get_group_requests(id)
    r = ''
    if len(requests)>0:
        r = 'yes'

    return render(request, "lifeInvaderGroupManager.html",
    {'user_id':user_id,
    'type':'group',
    'members':members,
    'requests':requests,
    'r':r})


@csrf_exempt
def create_group(request):

    user_id = request.session['user_id']
    group_id = ''

    try:
        post_text = request.POST.get('group_name', '')
        post_img = request.POST.get('pic', '')
        if(post_text != ''):
            group_id = databasequeries.create_group(user_id, post_text, post_img)

    except Exception as e:
        print(e)


    return visit_group(request, group_id)

def logout(request):
    request.session['user_id'] = 'none'

    return render(request, 'lifeInvaderLogin.html')
