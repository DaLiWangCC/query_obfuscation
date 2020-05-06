#-*- coding:utf-8 -*-
from flask import Flask, url_for, request, render_template ,jsonify,send_from_directory,make_response
from app import app
import time
import getMostQueriesUser
import os

count = 100
userIndex = 0 #用户编号




@app.route('/homepage')
def hello():
    url = url_for('about')
    link = '<a href="' + url + '">About us!</a>'

    url2 = url_for('downloadtmn')
    link2 = '<a href="' + url2 + '">TrackMeNot_Enhanced.zip</a>'

    return link


# 下载TMN插件
@app.route("/downloadtmn", methods=['GET'])
def downloadtmn():
    directory = os.getcwd()  # 假设在当前目录
    filename = "TrackMeNot_Enhanced.zip"
    print(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/export_xls', methods=['GET'])
def return_file():
    directory = os.getcwd()  # 假设在当前目录
    filename = "TrackMeNot_Enhanced.zip"

    file =  send_from_directory(directory, filename, as_attachment=True)
    response = make_response(file)
    return response


@app.route('/about')
def about():
    print("about")

    return render_template('index.html');

    return 'We are the knights who say Ni!!';

@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    print("question")
    print(title)

    if request.method == 'GET':
        question = title
        return render_template('AnswerQuestion.html',
                               question = question)
    elif request.method == 'POST':
        submittedAnswer = request.form['submittedAnswer'];

        answer = title

        if submittedAnswer == answer:
            return render_template('Correct.html');
        else:
            return render_template('Incorrect.html',
                                   answer = answer,
                                   submittedAnswer = submittedAnswer);

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        print("get")

        return render_template('CreateQuestion.html');
    elif request.method == 'POST':
        question = request.form['question'];
        answer = request.form['answer'];
        title = request.form['title'];

        # r.set(title+':question',question);
        # r.set(title+':answer',answer);
        print(question)
        print(answer)


        return render_template('CreatedQuestion.html',
                               question = question);
    return;


# get queries from aol
@app.route('/aol/<index>', methods=['GET', 'POST'])
def getFromAOL(index):
    print("someone query")

    allUserDic = getMostQueriesUser.getTop10User(index)

    # userQuery["anonID"] = anonID
    # userQuery["query"] = query
    # userQuery["queryTime"] = queryTime
    # userQuery["itemRank"] = itemRank
    # userQuery["clickURL"] = clickURL
    print("someone query ok")
    print(allUserDic[0])
    global userIndex
    userIndex = index
    return jsonify(allUserDic)


# receive user queries from tmn plugin
@app.route('/postUserSearch', methods=['POST'])
def postUserSearch():
    print(request.form)
    print("USER")

    query = request.form['query']
    query_date = request.form['date']
    strLine = "user" + "\t\t" + query + "\t\t" + query_date

    date = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    directory = os.getcwd()  # 假设在当前目录

    path = directory + "/saveData/combination/"
    filename = path + "User_queries_"+str(userIndex)+"_" + date+".txt"

    writeTofile(filename, strLine)
    return jsonify({'info': 'success'})

# receive TMN queries from tmn plugin
@app.route('/postTMNSearch', methods=['POST'])
def postTMNSearch():
    print(request.form)
    print("TMN")
    query = request.form['query']
    query_date = request.form['date']
    strLine = "tmn" + "\t\t" + query + "\t\t" + query_date

    date = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    directory = os.getcwd()  # 假设在当前目录

    path = directory + "/saveData/combination/"
    filename = path + "TMN_queries_"+str(userIndex)+"_"  + date + ".txt"


    writeTofile(filename,strLine)
    return jsonify({'info': 'success'})

#写入文件
def writeTofile(filename,str):
    outfile = open(filename,'a')
    outfile.write(str)
    outfile.write("\n")
    outfile.close()

