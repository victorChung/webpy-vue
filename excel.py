#coding=utf-8

import xlwt
import xlrd

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
      print(json_data[index])
      ws.write(index+1, 0, json_data[index]['reg_date'])
      ws.write(index+1, 1, json_data[index]['module_no'])
      ws.write(index+1, 2, json_data[index]['username'])
      ws.write(index+1, 3, json_data[index]['module_name'])
      module_num = '' if json_data[index]['module_num'] == '' else int(json_data[index]['module_num'])
      ws.write(index+1, 4, module_num)
      ws.write(index+1, 5, json_data[index]['info'])
      ws.write(index+1, 6, json_data[index]['apply_date'])
      ws.write(index+1, 7, json_data[index]['stuff_date'])
      ws.write(index+1, 8, json_data[index]['expected_date'])
      ws.write(index+1, 9, json_data[index]['distributed_date'])
      ws.write(index+1, 10, json_data[index]['tech_require'])

  wb.save('./static/'+ file_name)
  return '/static/'+ file_name