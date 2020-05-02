#coding=utf-8

import web
import json
import time
import excel
import utils
# from dailyReport import DailyReportHandle
from urllib.parse import quote,unquote

render = web.template.render("templates")
#非调试模式
web.config.debug = False
web.config.session_parameters['timeout'] = 60*10

urls = (
    "/safe", "Safe", 
    '/', 'Handle', 
    '/daily/report', 'DailyHandle', 
    '/daily/reort/table', 'DailyReportHandle', 
    '/daily/reort/table/edit', 'DailyReportEditHandle', 
    '/daily/reort/table/del', 'DailyReportDelHandle', 
    '/login', 'LoginHandle',
    '/logout', 'LogoutHandle',
    '/table', 'TableHandle',
    '/table/del', 'TableDelHandle',
    '/table/edit', 'TableEditHandle',
    '/excel', 'ExcelHandle'
)
app = web.application(urls, globals())

# session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
session = web.session.Session(   # 设置session
               app, 
               web.session.DiskStore('sessions'),  # sessionDiskStore将session存到内存
               initializer={  # initializer这个参数是个字典，字典内的参数根据自己需求随便设置
                               'login': False,
                               'user': ""
                               }) 


def session_hook():
    web.ctx.session = session


class ExcelHandle(object):
  def GET(self):
    f = open('data.json', 'r', encoding='UTF-8')
    dataObj = json.loads(f.read())
    if f:
      f.close()
    str_time = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
    download_url = excel.writeExcel(dataObj['data'], 'test_' + str_time + '.xls')

    web.header('content-type','text/json')
    return json.dumps({'status': 1, 'download_url': download_url})


class Safe(object):
    def GET(self):
        return render.abc()
        # print('session.session_id : ', session.session_id)
        # return "name: " + session.user

class Handle(object):
  def GET(self):
    try:
      if session.user == '' or session.user is None:
        web.seeother('/login')
      else:
        return render.index()
    # except Exception as Argument:
    except Exception as err:
      return err


class DailyHandle(object):
  def GET(self):
    try:
      if session.user == '' or session.user is None:
        web.seeother('/login')
      else:
        return render.dailyreport()
    # except Exception as Argument:
    except Exception as err:
      return err



class DailyReportHandle(object):
  def GET(self):
    try:
      f = open('dailyReport.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()
      # print(dataObj)
      dataObj['data'].sort(key = lambda x:x['apartment'])
      
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
    except Exception as Argument:
      return Argument
  def POST(self):
    try:
      post_data = web.data()
      if post_data:
        print('post data: ', post_data)
        json_data = json.loads(post_data)
        json_data['apartment'] = unquote(json_data['apartment'])
        json_data['problem'] = unquote(json_data['problem'])
        json_data['desc'] = unquote(json_data['desc'])
        json_data['reporter'] = unquote(json_data['reporter'])
        json_data['report_date'] = unquote(json_data['report_date'])
        json_data['operator'] = session.user
        json_data['created_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        rand_arr = utils.getRandomId(10)
        json_data['id'] = ''.join(rand_arr)

      print('post data json_data: ', json_data)

      f = open('dailyReport.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()
      dataObj['data'].append(json_data)

      dataObj['data'].sort(key = lambda x:x['apartment'])

      print('--------------------after json.dumps(dataObj, ensure_ascii=False)')
      print(json.dumps(dataObj, ensure_ascii=False))
      jsonStr = json.dumps(dataObj, ensure_ascii=False)
      f = open('dailyReport.json', 'w', encoding='UTF-8')
      f.write(jsonStr)
      if f:
        f.close()
        
      # dataObj.sort()

      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
    except Exception as Argument:
      return Argument

class DailyReportDelHandle(object):
  def POST(self):
    try:
      if session.user != 'admin':
        web.header('content-type','text/json')
        return json.dumps({'status': 0, 'err': {'msg': '无权限进行该操作'}})

      f = open('dailyReport.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()

      post_data = web.data()
      if post_data:
        print('post data: ', post_data)
        json_data = json.loads(post_data)

      data_arr = dataObj['data']
      for idx in range(len(data_arr)):
        if data_arr[idx]['id'] == json_data['id']:
          data_arr.remove(data_arr[idx])
          break

      jsonStr = json.dumps(dataObj, ensure_ascii=False)
      f = open('dailyReport.json', 'w', encoding='UTF-8')
      f.write(jsonStr)
      if f:
        f.close()
      
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
      
    except Exception as Argument:
      return Argument


class DailyReportEditHandle(object):
  def POST(self):
    try:
      if session.user != 'admin':
        web.header('content-type','text/json')
        return json.dumps({'status': 0, 'err': {'msg': '无权限进行该操作'}})

      f = open('dailyReport.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()

      post_data = web.data()
      if post_data:
        print('post data: ', post_data)
        json_data = json.loads(post_data)


      data_arr = dataObj['data']
      for idx in range(len(data_arr)):
        if data_arr[idx]['id'] == json_data['id']:
          data_arr[idx]['apartment'] = unquote(json_data['apartment'])
          data_arr[idx]['problem'] = unquote(json_data['problem'])
          data_arr[idx]['desc'] = unquote(json_data['desc'])
          data_arr[idx]['reporter'] = unquote(json_data['reporter'])
          data_arr[idx]['report_date'] = unquote(json_data['report_date'])
          # data_arr[idx] = json_data
          print("dataObj['data'][idx]")
          print(dataObj['data'][idx])
          break

      jsonStr = json.dumps(dataObj, ensure_ascii=False)
      f = open('dailyReport.json', 'w', encoding='UTF-8')
      f.write(jsonStr)
      if f:
        f.close()
      
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
      
    except Exception as Argument:
      return Argument

class TableEditHandle(object):
  def POST(self):
    try:
      if session.user != 'admin':
        web.header('content-type','text/json')
        return json.dumps({'status': 0, 'err': {'msg': '无权限进行该操作'}})

      f = open('data.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()

      post_data = web.data()
      if post_data:
        # print('post data: ', post_data)
        json_data = json.loads(post_data)

      data_arr = dataObj['data']
      for idx in range(len(data_arr)):
        if data_arr[idx]['id'] == json_data['id']:
          data_arr[idx] = json_data
          print("dataObj['data'][idx]")
          print(dataObj['data'][idx])
          break

      jsonStr = json.dumps(dataObj, ensure_ascii=False)
      f = open('data.json', 'w', encoding='UTF-8')
      f.write(jsonStr)
      if f:
        f.close()
      
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
      
    except Exception as Argument:
      return Argument

class TableDelHandle(object):
  def POST(self):
    try:
      if session.user != 'admin':
        web.header('content-type','text/json')
        return json.dumps({'status': 0, 'err': {'msg': '无权限进行该操作'}})

      f = open('data.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()

      post_data = web.data()
      if post_data:
        print('post data: ', post_data)
        json_data = json.loads(post_data)

      data_arr = dataObj['data']
      for idx in range(len(data_arr)):
        if data_arr[idx]['id'] == json_data['id']:
          data_arr.remove(data_arr[idx])
          break

      jsonStr = json.dumps(dataObj, ensure_ascii=False)
      f = open('data.json', 'w', encoding='UTF-8')
      f.write(jsonStr)
      if f:
        f.close()
      
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
      
    except Exception as Argument:
      return Argument


class TableHandle(object):
  def GET(self):
    try:
      f = open('data.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()

      # dataObj['data'].sort()
      # print(dataObj['data'])
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
    except Exception as Argument:
      return Argument
  def POST(self):
    try:
      post_data = web.data()
      if post_data:
        print('post data: ', post_data)
        json_data = json.loads(post_data)
        json_data['module_name'] = unquote(json_data['module_name'])
        json_data['info'] = unquote(json_data['info'])
        json_data['tech_require'] = unquote(json_data['tech_require'])
        json_data['operator'] = session.user
        json_data['created_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        rand_arr = utils.getRandomId(10)
        json_data['id'] = ''.join(rand_arr)

      print('post data json_data: ', json_data)

      f = open('data.json', 'r', encoding='UTF-8')
      dataObj = json.loads(f.read())
      if f:
        f.close()
      # print('--------------------original dataObj')
      # print(dataObj)
      # dataObj['data'].append({"name": name, "age": age, "address": address, "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
      dataObj['data'].append(json_data)

      # print('--------------------after dataObj.data')
      # print(dataObj['data'])
      # print('--------------------after dataObj')
      # print(dataObj)

      print('--------------------after json.dumps(dataObj, ensure_ascii=False)')
      print(json.dumps(dataObj, ensure_ascii=False))
      jsonStr = json.dumps(dataObj, ensure_ascii=False)
      f = open('data.json', 'w', encoding='UTF-8')
      f.write(jsonStr)
      if f:
        f.close()
      
      # print('--------------------type dataObj')
      # print(type(dataObj))
      # print('--------------------after dataObj')
      # print(dataObj)
      web.header('content-type','text/json')
      return json.dumps({'status': 1, 'data': dataObj})
    except Exception as Argument:
      return Argument



# 注销
class LogoutHandle(object):
  def POST(self):
    # if session.user != '':
    session.kill()
    return json.dumps({'status': 1, 'data': 'user had logout'})

# 登录
class LoginHandle(object):
  def GET(self):
    if session.user != '':
      web.seeother('/')
    else:
      return render.login()
  def POST(self):
    try:
      # inputData = web.input()
      # print('input data: ', inputData)
      # name = inputData.get('name')
      # pwd = inputData.get('pwd')

      post_data = web.data()
      if post_data:
        print('post data: ', post_data)
        json_data = json.loads(post_data)
        name = json_data['name']
        pwd = json_data['pwd']
        
      f = open('login.json', 'r', encoding='UTF-8')
      loginList = json.loads(f.read())
      print(loginList)
      web.header('content-type','text/json')
      if f:
          f.close()
      login = False
      for item in loginList:
        print('item')
        print(item)
        if item['name'] == name and item['pwd'] == pwd:
          login = True
          session.login = True
          session.user = name
          break
      if login == True:
        print('login success')
        # return {'status': 1}
        userObj = {
          'name': session.user,
          'session_id': session.session_id
        }
        return json.dumps({'status': 1, 'data': userObj})
      else:
        print('login fail')
        return json.dumps({'status': 0})
    except Exception as Argument:
      return Argument
    # finally:
    #   if f:
    #       f.close()


if __name__ == '__main__':
  # app.add_processor(web.loodhook(session_hook))  #添加钩子，在每一个接口之前都执行
  app.run()