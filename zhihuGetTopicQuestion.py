#coding=utf-8
# nlp
from __future__ import print_function, unicode_literals

# HTMLParser
import re
pattern = re.compile(r'<.*?>')

# zhihu
from zhihu_oauth import ZhihuClient
import json
import requests

# sqlite3
import sqlite3
conn = sqlite3.connect('zhihuInfomation.db')

conn.execute('''
        CREATE TABLE USER_TABLE
       (U_ID INT     NOT NULL,
        U_EMAIL TEXT NOT NULL,
        U_PASSWORD TEXT NOT NULL,
        U_TOPIC1 INT,
        U_TOPIC2 INT,
        U_TOPIC3 INT,
        PRIMARY KEY (U_ID,U_EMAIL));
        ''')

conn.execute('''
        CREATE TABLE ANSWER_TABLE
       (A_QUESTION_ID INT     NOT NULL,
        A_ID INT    NOT NULL,
        A_QUESTION_TITLE TEXT NOT NULL,
        A_FEELING      REAL ,
        A_AUTHOR  TEXT NOT NULL,
        A_CONTENT   TEXT  NOT NULL,
        A_CLASS TEXT NOT NULL,
        A_UPDATED_TIME TEXT NOT NULL,
        PRIMARY KEY (A_QUESTION_ID,A_ID));
        ''')

conn.execute('''
        CREATE TABLE COMMENTS_TABLE
        (C_QUESTION_ID INT     NOT NULL,
        C_ANSER_ID INT    NOT NULL,
        C_AUTHOR TEXT NOT NULL,
        C_VOTECOUNT TEXT NOT NULL,
        C_CONTENT TEXT NOT NULL,
        C_CREATEDTIME TEXT NOT NULL);
        ''')

conn.execute('''
        CREATE TABLE TOPIC_TABLE
        (T_ID INT PRIMARY KEY NOT NULL,
        T_BEST_ANSWERS_COUNT TEXT NOT NULL,
        T_FOLLOWERS_COUNT TEXT NOT NULL,
        T_QUESTIONS_COUNT TEXT NOT NULL);
        ''')

# posturl
SUMMARY_URL = 'http://api.bosonnlp.com/summary/analysis'
SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
CLASSIFY_URL = 'http://api.bosonnlp.com/classify/analysis'

# X-Token
headers = {'X-Token': 'afA7ckHA.7771.3EQV8MutdTWw'}

client = ZhihuClient()
client.load_token('token.pkl')
# replace it  as user input

# topic
internet = client.from_url('https://www.zhihu.com/topic/19550517')
sport = client.from_url('https://www.zhihu.com/topic/19554827')
education = client.from_url('https://www.zhihu.com/topic/19553176')
bussiness = client.from_url('https://www.zhihu.com/topic/19555457')
society = client.from_url('https://www.zhihu.com/topic/19566933')
entertain = client.from_url('https://www.zhihu.com/topic/19553632')
military = client.from_url('https://www.zhihu.com/topic/19553911')
nation = client.from_url('https://www.zhihu.com/topic/19553911')
science = client.from_url('https://www.zhihu.com/topic/19556664')
realestate = client.from_url('https://www.zhihu.com/topic/19555559')
international = client.from_url('https://www.zhihu.com/topic/19561759')
female = client.from_url('https://www.zhihu.com/topic/19556945')
automoile = client.from_url('https://www.zhihu.com/topic/19551915')
game = client.from_url('https://www.zhihu.com/topic/19550994')

# internet

print(internet.id)
print(internet.best_answers_count)
print(internet.followers_count)
print(internet.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(internet.id)+", "+str(internet.best_answers_count)+", "+str(internet.followers_count)+","+str(internet.questions_count)+" )");
conn.commit()

for answer in internet.best_answers:

    print('internet')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()

# sport

print(sport.id)
print(sport.best_answers_count)
print(sport.followers_count)
print(sport.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(sport.id)+", "+str(sport.best_answers_count)+", "+str(sport.followers_count)+","+str(sport.questions_count)+" )");
conn.commit()

for answer in sport.best_answers:

    print('sport')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()
    
# education

print(education.id)
print(education.best_answers_count)
print(education.followers_count)
print(education.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(education.id)+", "+str(education.best_answers_count)+", "+str(education.followers_count)+","+str(education.questions_count)+" )");
conn.commit()

for answer in education.best_answers:

    print('education')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()


# business

print(business.id)
print(business.best_answers_count)
print(business.followers_count)
print(business.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(business.id)+", "+str(business.best_answers_count)+", "+str(business.followers_count)+","+str(business.questions_count)+" )");
conn.commit()

for answer in business.best_answers:

    print('business')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# society

print(society.id)
print(society.best_answers_count)
print(society.followers_count)
print(society.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(society.id)+", "+str(society.best_answers_count)+", "+str(society.followers_count)+","+str(society.questions_count)+" )");
conn.commit()

for answer in society.best_answers:

    print('society')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()


# entertain

print(entertain.id)
print(entertain.best_answers_count)
print(entertain.followers_count)
print(entertain.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(entertain.id)+", "+str(entertain.best_answers_count)+", "+str(entertain.followers_count)+","+str(entertain.questions_count)+" )");
conn.commit()

for answer in entertain.best_answers:

    print('entertain')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# military

print(military.id)
print(military.best_answers_count)
print(military.followers_count)
print(military.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(military.id)+", "+str(military.best_answers_count)+", "+str(military.followers_count)+","+str(military.questions_count)+" )");
conn.commit()

for answer in military.best_answers:

    print('military')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# nation

print(nation.id)
print(nation.best_answers_count)
print(nation.followers_count)
print(nation.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(nation.id)+", "+str(nation.best_answers_count)+", "+str(nation.followers_count)+","+str(nation.questions_count)+" )");
conn.commit()

for answer in nation.best_answers:

    print('nation')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# science

print(science.id)
print(science.best_answers_count)
print(science.followers_count)
print(science.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(science.id)+", "+str(science.best_answers_count)+", "+str(science.followers_count)+","+str(science.questions_count)+" )");
conn.commit()

for answer in science.best_answers:

    print('science')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# realestate

print(realestate.id)
print(realestate.best_answers_count)
print(realestate.followers_count)
print(realestate.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(realestate.id)+", "+str(realestate.best_answers_count)+", "+str(realestate.followers_count)+","+str(realestate.questions_count)+" )");
conn.commit()

for answer in realestate.best_answers:

    print('realestate')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# international

print(international.id)
print(international.best_answers_count)
print(international.followers_count)
print(international.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(international.id)+", "+str(international.best_answers_count)+", "+str(international.followers_count)+","+str(international.questions_count)+" )");
conn.commit()

for answer in international.best_answers:

    print('international')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# female

print(female.id)
print(female.best_answers_count)
print(female.followers_count)
print(female.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(female.id)+", "+str(female.best_answers_count)+", "+str(female.followers_count)+","+str(female.questions_count)+" )");
conn.commit()

for answer in female.best_answers:

    print('female')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()


# automobile

print(automobile.id)
print(automobile.best_answers_count)
print(automobile.followers_count)
print(automobile.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(automobile.id)+", "+str(automobile.best_answers_count)+", "+str(automobile.followers_count)+","+str(automobile.questions_count)+" )");
conn.commit()

for answer in automobile.best_answers:

    print('automobile')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()



# game

print(game.id)
print(game.best_answers_count)
print(game.followers_count)
print(game.questions_count)

conn.execute(
            "INSERT INTO TOPIC_TABLE (T_ID, T_BEST_ANSWERS_COUNT, T_FOLLOWERS_COUNT, T_QUESTIONS_COUNT) \
            VALUES ("+str(game.id)+", "+str(game.best_answers_count)+", "+str(game.followers_count)+","+str(game.questions_count)+" )");
conn.commit()

for answer in game.best_answers:

    print('game')
    print(answer.question.title)
    print(answer.author.name)

    re = pattern.sub('', answer.content)
    source = {
        'not_exceed': 0,
        'percentage': 0.2,
        'title': '',
        'content': re
    }
    resp = requests.post(
        SUMMARY_URL,
        headers = headers,
        data = json.dumps(source).encode('utf-8'))



    # what we want!
    print(resp.text)

    data = json.dumps(resp.text)
    respSentiment = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
    respclass = requests.post(CLASSIFY_URL, headers=headers, data=data.encode('utf-8'))
    print(respSentiment.text)
    print(respclass.text)

    params = (answer.question.id, answer.id, answer.question.title, respSentiment.text, answer.author.name, resp.text, respclass.text, answer.updated_time)

    conn.execute("INSERT INTO ANSWER_TABLE VALUES(?,?,?,?,?,?,?,?)", params)

    conn.commit()

    for comments in answer.comments:
        print(comments.content)

        print(comments.vote_count)

        params = (answer.question.id, answer.id, comments.author.name, comments.vote_count, comments.content, comments.created_time)
        conn.execute("INSERT INTO COMMENTS_TABLE VALUES(?,?,?,?,?,?)", params)
        conn.commit()

