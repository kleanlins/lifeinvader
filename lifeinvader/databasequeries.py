import mysql.connector as mariadb
from . import secret_data

mariadb_connection = mariadb.connect(user='root', password=secret_data.password, database='redesocial')
cursor = mariadb_connection.cursor()



def login_check(email, password):
        cmmd = "select * from user where email='" + email + "'"
        cursor.execute(cmmd)


        for each in cursor:
            print(each)
            if each[3] != password:
                return "Your password is wrong", ''

            return '', each[0] # each[0] is the user ID


def get_posts(fromwho, qtd):
    if fromwho != '':
        cmmd = "select * from post where id_owner='{}'".format(fromwho)
        cursor.execute(cmmd)

        posts_list = list()

        for each in cursor:
            posts_list.append(each)

        return posts_list

    cmmd = "select * from post"
    cursor.execute(cmmd)

    posts_list = [each for each in cursor]

    # for each in cursor:
    #     posts_list.append(each)


def get_info_from_id(id):
    cmmd = "select name, age, email from user where id='{}'".format(id)
    cursor.execute(cmmd)

    name = ''
    age = ''
    email = ''

    for each in cursor:
        name, age, email = each

    return name, age, email


def get_friends(id):
    print("Getting friends from id={}".format(id))
    cmmd = "select user.id, user.name from user inner join friendship on "
    cmmd2 = "user.id=friendship.friend_id where friendship.user_id={}".format(id)
    cursor.execute(cmmd + cmmd2)

    friends_data = list()
    for each in cursor:
        friends_data.append(each)

    cmmd = "select user.id, user.name from user inner join friendship on "
    cmmd2 = "user.id=friendship.user_id where friendship.friend_id={}".format(id)
    cursor.execute(cmmd + cmmd2)

    for each in cursor:
        if each not in friends_data:
            friends_data.append(each)

    print(friends_data)
    return friends_data

def get_groups(id):
    print("Getting groups from id={}".format(id))
    cmmd = "select id, name, relationship from groups inner join user_group"
    cmmd2 = " on groups.id=user_group.group_id where id_user={}".format(id)
    cursor.execute(cmmd + cmmd2)

    groups_data = [each for each in cursor]

    print(groups_data)
    return groups_data;

def get_timeline_posts(id):

    friends = get_friends(id)
    friends_posts = list()


    for each in friends:

        cmmd="select user.name, user.id, post.content from user inner join post on "
        cmmd2 = "user.id=post.id_location and post.id_location=post.id_owner where user.id={} and post.type_owner='U'".format(each[0])

        cursor.execute(cmmd + cmmd2)

        for each in cursor:
            friends_posts.append(each)

    print(friends_posts)
    return friends_posts;


def get_all_users(id):
    cmmd = "select user.name, user.id from user where id!={}".format(id)
    cursor.execute(cmmd)

    all_users = [each for each in cursor]

    return all_users

def get_all_groups():
    cmmd = "select name from groups"

    cursor.execute(cmmd)

    all_groups = [each[0] for each in cursor]

    return all_groups
