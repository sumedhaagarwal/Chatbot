from flask import Flask, render_template, request
from Summarizer import *
import sqlite3
import datetime
from sqlite3 import Error
from operator import itemgetter


def get_date():
    now = datetime.datetime.now()
    return now.strftime("%Y:%m:%d")


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Posts")

    rows = cur.fetchall()

    for row in rows:
        print(row)


# def select_task_by_priority(conn, priority):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
#
#     rows = cur.fetchall()
#
#     for row in rows:
#         print(row)

def get_last_date(currdate):
    past_date = datetime.datetime.now() - datetime.timedelta (days = 15)
    # print(past_date.strftime("%Y:%m:%d"))
    return past_date.strftime("%Y:%m:%d")

def get_posts_by_company(conn, companyname, currdate):
    lastDate = get_last_date(currdate)
    cur = conn.cursor()
    cur.execute("SELECT Post FROM Posts WHERE lower(CompanyName)=? and PostDate>=? ", (companyname.lower(), lastDate))
    rows = cur.fetchall()
    allposts = []
    for row in rows:
        allposts.append("".join(row))
        # print(row)
    return "".join(allposts)

def skills_score(row, selected_skills):
    selected_skills = selected_skills.split(",")
    present_skills = row.split(",")

    s1=set(selected_skills)
    s2=set(present_skills)
    return len(s1&s2)

def find_people_like_me(conn):
    selected_experience=2
    selected_skills='PHP, Python, Ruby on Rails, Machine Learning, Artificial Intelligence, Database Management'
    cur = conn.cursor()
    cur.execute("SELECT * FROM Connections WHERE Experience BETWEEN ? AND ?", (str(selected_experience-1), str(selected_experience+9)))
    # cur.execute("SELECT * FROM Connections")
    rows = cur.fetchall()
    allposts = []
    for row in rows:
        # print(row)
        # allposts.append("\t".join(row))
        # print(row)
        # print('\n')
        # print(row[5])
        tot = skills_score(row[4], selected_skills)
        # row.append(tot)
        li=list(row)
        li.append(tot)
        allposts.append(li)
    # print(allposts)
    allposts.sort(key=lambda x: x[6],reverse=True)
    # print(allposts)
    # for post in allposts:
    #     print(post[6])
    # return "".join(allposts)
    ret_list=[]
    for post in allposts:
        li=[]
        li.append(post[0])
        li.append(post[1])
        li.append(post[2])
        # print(li)
        ret_list.append(li)
    # print(ret_list)
    return ret_list


def main():
    database = "/home/nimisha/wintathon19/database/data.sqlite"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("1. Query task by priority:")
        # select_task_by_priority(conn,1)

        # print("2. Query all tasks")
        # select_all_tasks(conn)
        l = get_posts_by_company(conn, "Google", get_date())
        print(get_date())

        print(l)


def get_summary(companyname):
    return companyname

def get_jobs(companyname):
    return "These are the job openings in "+ companyname

app = Flask(__name__, static_folder='static')

@app.route('/')
def display():
    return render_template('frontend.html')

# @app.route('/plm')
# def show_ppl_like_me():
#     l = find_people_like_me(conn)
#     arr = []
#     for item in l:
#         arr.append(' '.join(item))
#     brr = '\n'.join(arr)
#     return brr

@app.route('/login')
def loginUser():
    render_template('login.html')

@app.route('/summary')
def displaySummary():

    if 'company' in request.args:
        companyname = request.args.get('company')
        allposts = get_posts_by_company(conn, companyname, get_date())
        summary = final_summarize(allposts)
        return summary
    else:
        return "No company specified"

@app.route('/jobs')
def displayJobs():
    if 'company' in request.args:
        companyname = request.args.get('company')
        jobs = get_jobs(companyname)
        return jobs
    else:
        return "No company specified"


if __name__=='__main__':
    database = "data.sqlite"

    # create a database connection
    conn = sqlite3.connect(database, check_same_thread=False)
    with conn:
        app.run(debug=True, port = 4567)
        # print("1. Query task by priority:")
        # select_task_by_priority(conn,1)

        # print("2. Query all tasks")
        # select_all_tasks(conn)
        # l = get_posts_by_company(conn, "Google", get_date())
        # print(get_date())

        # print(l)
    # app.run(debug=True, port = 1412)
