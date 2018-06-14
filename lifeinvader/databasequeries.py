import mysql.connector as mariadb
from . import secret_data

mariadb_connection = mariadb.connect(user='root', password=secret_data.password, database='redesocial')
cursor = mariadb_connection.cursor()


def register(name, email, password, pic):

    cmmd = "select * from user where email='{}'".format(email)
    cursor.execute(cmmd)
    status = [each for each in cursor]

    if len(status) > 0:
        return 'deny'

    cmmd = "insert into user(name, email, password, pic) "
    cmmd2 = "value('{}','{}','{}','{}')".format(name, email, password, pic)
    cursor.execute(cmmd + cmmd2)

    mariadb_connection.commit()
    return cursor.lastrowid


    return status


def login_check(email, password):
        cmmd = "select * from user where email='" + email + "'"
        cursor.execute(cmmd)

        for each in cursor:
            # print(each)
            if each[3] != password:
                return "Your password is wrong", ''

            return '', each[0] # each[0] is the user ID


def get_posts(location, type):

    cmmd = "select user.id, user.name, user.pic, post.content, post.image from post inner "
    cmmd2 = "join user on user.id=post.id_owner where id_location='{}' and type_owner='{}' order by post.id desc".format(location, type)
    cursor.execute(cmmd + cmmd2)

    posts_list = list()

    for each in cursor:
        posts_list.append(each)

    return posts_list



def get_info_from_id(id):

    # global cursor
    # cursor = mariadb_connection.cursor()

    cmmd = "select name, age, email, pic from user where id='{}'".format(id)
    cursor.execute(cmmd)

    name = ''
    age = ''
    email = ''
    pic = ''

    for each in cursor:
        name, age, email, pic = each

    return name, age, email, pic


def get_friends(id):
    print("Getting friends from id={}".format(id))
    cmmd = "select user.id, user.name, user.pic from user inner join friendship on "
    cmmd2 = "user.id=friendship.friend_id where friendship.user_id={} and friendship.type='friends'".format(id)
    cursor.execute(cmmd + cmmd2)

    friends_data = list()
    for each in cursor:
        friends_data.append(each)

    cmmd = "select user.id, user.name, user.pic from user inner join friendship on "
    cmmd2 = "user.id=friendship.user_id where friendship.friend_id={} and friendship.type='friends'".format(id)
    cursor.execute(cmmd + cmmd2)

    for each in cursor:
        if each not in friends_data:
            friends_data.append(each)

    # print(friends_data)
    return friends_data

def get_groups(id, exc=None):
    print("Getting groups from id={}".format(id))
    cmmd = "select id, name, relationship, groups.image from groups inner join user_group"
    if exc == None:
        cmmd2 = " on groups.id=user_group.group_id where id_user={}".format(id)
    else:
        cmmd2 = " on groups.id=user_group.group_id where id_user!={}".format(id)
    cursor.execute(cmmd + cmmd2)

    groups_data = [each for each in cursor]

    # print(groups_data)
    return groups_data;

def get_timeline_posts(id):
    print("Getting friend posts from id={}".format(id))

    friends = get_friends(id)
    friends.append([id])
    friends_posts = list()


    for each in friends:

        cmmd="select post.id, user.name, user.id, user.pic, post.content from user inner join post on "
        cmmd2 = "user.id=post.id_location and post.id_location=post.id_owner where user.id={} and post.type_owner='U'".format(each[0])

        cursor.execute(cmmd + cmmd2)

        for each in cursor:
            friends_posts.append(each)

    friends_posts = sorted(friends_posts, key=lambda x:x[0], reverse=True)
    return friends_posts;


def get_all_users(id):
    cmmd = "select user.name, user.id, user.pic from user where id!={}".format(id)
    cursor.execute(cmmd)

    all_users = [each for each in cursor]

    return all_users

def get_all_groups():
    cmmd = "select * from groups"

    cursor.execute(cmmd)

    all_groups = [each for each in cursor]

    return all_groups

def is_friend(id, id2):
    cmmd = "select type from friendship where (user_id={0} and friend_id={1}) or (friend_id={0} and user_id={1})".format(id, id2)
    cursor.execute(cmmd)

    status = [each[0] for each in cursor]

    return status[0] if len(status) > 0 else 'not friends'

def post(id_owner, id_location, type_owner, text, pic):

    # insert into post(id_owner, id_location, type_owner, content, image) value(,,'','','')"

    cmmd = "insert into post(id_owner, id_location, type_owner, content, image) "
    cmmd2 = "value({},{},'{}','{}','{}')".format(id_owner, id_location, type_owner, text, pic)

    cursor.execute(cmmd + cmmd2)
    mariadb_connection.commit()


def add_friend(user_id, friend_id):

    print("user {} is adding {}".format(user_id, friend_id))

    cmmd = "insert into friendship value({},{},'requested')".format(user_id, friend_id)

    cursor.execute(cmmd)
    mariadb_connection.commit()

def remove_friend(user_id, friend_id):

    print("user {} is removing {}".format(user_id, friend_id))

    cmmd = "delete from friendship where (user_id={} and friend_id={}) ".format(user_id, friend_id)
    cmmd2 = "or (user_id={} and friend_id={})".format(friend_id, user_id)

    cursor.execute(cmmd + cmmd2)
    mariadb_connection.commit()


def acc_friend(user_id, friend_id):

    print("user {} is acepting {}".format(user_id, friend_id))

    cmmd = "update friendship set type='friends' "
    cmmd2 = "where user_id={} and friend_id={}".format(friend_id, user_id)

    cursor.execute(cmmd + cmmd2)
    mariadb_connection.commit()

    return 'ok'


def ref_friend(user_id, friend_id):

    print("user {} is refusing {}".format(user_id, friend_id))

    cmmd = "delete from friendship where "
    cmmd2 = "user_id={} and friend_id={}".format(friend_id, user_id)

    cursor.execute(cmmd + cmmd2)
    mariadb_connection.commit()

    return 'ok'


def get_requests(user_id):

    cmmd = "select user.id, user.name, user.pic from user inner join "
    cmmd2 = "friendship on user.id=friendship.user_id where "
    cmmd3 = "friendship.type='requested' and friendship.friend_id={}".format(user_id)

    cursor.execute(cmmd + cmmd2 + cmmd3)

    requests = [each for each in cursor]

    return requests
