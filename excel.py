#coding=utf-8

import xlwt
import xlrd
import time

# 导出excel
def writeExcel(json_data, file_name):
  wb = xlwt.Workbook() 
  # 添加一个表
  ws = wb.add_sheet('test')               
  # 3个参数分别为行号，列号，和内容
  # 需要注意的是行号和列号都是从0开始的
  ws.write(0, 0, '登记日期')
  ws.write(0, 1, '模号')
  ws.write(0, 2, '钳工')     
  ws.write(0, 3, '零件名称')
  ws.write(0, 4, '数量')
  ws.write(0, 5, '加工内容')     
  ws.write(0, 6, '申请日期')
  ws.write(0, 7, '预计到料日期')
  ws.write(0, 8, '要求完成日期')     
  ws.write(0, 9, '数据下发日期')
  ws.write(0, 10, '工艺要求')
  if type(json_data) is list:
    for index in range(len(json_data)):
      print('json_data[index]========>')
      print(json_data[index])
      reg_date = time.strptime(json_data[index]['reg_date'],'%Y-%m-%d') if json_data[index]['reg_date'] != '' else ''
      ws.write(index+1, 0, time.strftime(u"%m月%d日", reg_date))
      ws.write(index+1, 1, json_data[index]['module_no'])
      ws.write(index+1, 2, json_data[index]['username'])
      ws.write(index+1, 3, json_data[index]['module_name'])
      module_num = '' if json_data[index]['module_num'] == '' else int(json_data[index]['module_num'])
      ws.write(index+1, 4, module_num)
      ws.write(index+1, 5, json_data[index]['info'])

      apply_date = ''
      if json_data[index]['apply_date'] != '':
        apply_date = time.strptime(json_data[index]['apply_date'],'%Y-%m-%d')
        apply_date = time.strftime(u"%m月%d日", apply_date)
      ws.write(index+1, 6, apply_date)

      stuff_date = ''
      if json_data[index]['stuff_date'] != '':
        stuff_date = time.strptime(json_data[index]['stuff_date'],'%Y-%m-%d')
        stuff_date = time.strftime(u"%m月%d日", stuff_date)
      ws.write(index+1, 7, stuff_date)

      expected_date = ''
      if json_data[index]['expected_date'] != '':
        expected_date = time.strptime(json_data[index]['expected_date'],'%Y-%m-%d')
        expected_date = time.strftime(u"%m月%d日", expected_date)
      ws.write(index+1, 8, expected_date)

      distributed_date = ''
      if json_data[index]['distributed_date'] != '':
        distributed_date = time.strptime(json_data[index]['distributed_date'],'%Y-%m-%d')
        distributed_date = time.strftime(u"%m月%d日", distributed_date)
      ws.write(index+1, 9, distributed_date)

      ws.write(index+1, 10, json_data[index]['tech_require'])

  wb.save('./static/'+ file_name)
  return '/static/'+ file_name


# 导出excel
def writeDailyExcel(json_data, file_name):
  _apartment = []
  if type(json_data) is list:
    for index in range(len(json_data)):
      _apartment.append(json_data[index]['apartment'])
  print(_apartment)

  wb = xlwt.Workbook() 
  # 添加一个表
  ws = wb.add_sheet('test')               
  # 3个参数分别为行号，列号，和内容
  # 需要注意的是行号和列号都是从0开始的
  ws.write(0, 0, '部门')
  ws.write(0, 1, '模号')
  ws.write(0, 2, '担当')
  ws.write(0, 3, '异常类别')
  ws.write(0, 4, '问题点描述')
  ws.write(0, 5, '对应人员')
  ws.write(0, 6, '日期')
  
  if type(json_data) is list:
    for index in range(len(json_data)):
      c = _apartment.count(json_data[index]['apartment'])
      if index == 0:
        ws.write_merge(index+1, index+c, 0, 0, json_data[index]['apartment'])
        ws.write(index+1, 1, json_data[index]['problem'])
        ws.write(index+1, 2, json_data[index]['undertake'])
        ws.write(index+1, 3, json_data[index]['exception'])
        ws.write(index+1, 4, json_data[index]['desc'])
        ws.write(index+1, 5, json_data[index]['reporter'])
        ws.write(index+1, 6, json_data[index]['report_date'])
      elif json_data[index - 1]['apartment'] != json_data[index]['apartment']:
        ws.write_merge(index+1, index+c, 0, 0, json_data[index]['apartment'])
        ws.write(index+1, 1, json_data[index]['problem'])
        ws.write(index+1, 2, json_data[index]['undertake'])
        ws.write(index+1, 3, json_data[index]['exception'])
        ws.write(index+1, 4, json_data[index]['desc'])
        ws.write(index+1, 5, json_data[index]['reporter'])
        ws.write(index+1, 6, json_data[index]['report_date'])
      elif json_data[index - 1]['apartment'] == json_data[index]['apartment']:
        ws.write(index+1, 1, json_data[index]['problem'])
        ws.write(index+1, 2, json_data[index]['undertake'])
        ws.write(index+1, 3, json_data[index]['exception'])
        ws.write(index+1, 4, json_data[index]['desc'])
        ws.write(index+1, 5, json_data[index]['reporter'])
        ws.write(index+1, 6, json_data[index]['report_date'])

  # ws.write_merge(1, 4, 0, 0, u'加工')
  # ws.write(1, 1, u'临时加急改模插机床')
  # ws.write(1, 2, u'xcvdf46u789')
  # ws.write(1, 3, u'全体')

  # ws.write(2, 1, u'追加程序')
  # ws.write(2, 2, u'xcvojdfj')
  # ws.write(2, 3, u'全体')

  # ws.write(3, 1, u'追加电报')
  # ws.write(3, 2, u'xklvjsdpifhghp')
  # ws.write(3, 3, u'排产/跟进')

  # ws.write(4, 1, u'追加程序')
  # ws.write(4, 2, u'sadfadg34545')
  # ws.write(4, 3, u'sdfbsfbfs')
  wb.save('./static/'+ file_name)
  return '/static/'+ file_name