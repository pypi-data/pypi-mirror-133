#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Author : quality assurance @软件质量保障
# @Time : 2022/1/8 6:49 下午
# @File : Assert-P.py
# @desc : 本工具支持两个字典一致性compare，可用于自动化断言，例如数据库实际落库数据与预期结果比较；
# 支持场景：1.落单条数据场景 2.落多条数据场景
# 使用本工具前注意事项：
# 1.安装依赖库，texttable，参见requirements.txt
# 2.需要将断言的字典值转化为string格式, 否则会报类型错误：
# 例如TypeError: argument of type 'int' is not iterable


import logging
import json
from texttable import Texttable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

table = Texttable()
table.set_cols_align(["l", "r", "c", "d"])
table.set_cols_valign(["t", "m", "b", "e"])


# 单条数据核心逻辑
def AssertPy(tbName, actual, expect):
	# 判断actual、expect数据类型，必须是dict
	if actual is None: return False
	if expect is None: return False
	# 增加一个title
	title = [tbName, "actual","expect","result"]
	# 定义一个数组用于存储结果
	values = []
	values.append(title)
	check_result = True
	# 断言逻辑
	for key in expect.keys():
		value = []
		# 如果值不为null
		if expect.get(key) is not None:
			# 将Key取出并赋值给数组
			value.append(key)
			# 如果实际结果key的value为null
			if actual.get(key) is None:
				value.append(None)
			else:
				value.append(str(actual.get(key)))
			# 取出预期数据
			value.append(expect.get(key))
			# 实际值与预期值相同，则true
			if value[1] == expect.get(key):
				value.append("true")
			# 预期的value为not null，非null check
			elif expect.get(key) == "NOT NONE" and (value[1] not in [None, ""]):
				value.append("true")
			# 包含check, 如果实际contains预期，则true
			elif "CONTAINS_CHECK:" in expect.get(key) and expect.get(key)[15:] in value[1]:
				value.append("true")
			elif "JSON:" in expect.get(key):
				exp = json.loads(expect.get(key).replace("JSON:", ""))
				act = json.loads((value[1]))
				if len(exp) != len(act):
					value.append("false")
					check_result = False
					continue
				# 升序排
				for eKey in sorted(exp.keys(), reverse=False):
					match = False
					for aKey in sorted(act.keys(), reverse=False):
						if eKey == aKey:
							match = True
							if act.get(aKey) != exp.get(eKey):
								value.append("false")
								check_result = False
					if match is False:
						value.append("false")
						check_result = False
				if match and len(value) == 3:
					value.append("true")
			elif value[1] != expect.get(key):
				value.append("false")
				check_result = False
		values.append(value)
	# print(values)
	# texttable需要过滤[]数据
	if [] in values: values.remove([])
	table.add_rows(values)
	print(table.draw())
	return check_result


# 多条数据check，针对一次请求需要罗同一表多条数据场景
def AssertPy_multi(tbName, actual, expect):
	if actual is None: return False
	if expect is None: return False
	check_result = True
	if len(actual) < len(expect):
		logger.info("实际查出来的结果, 比预期的结果还少, check failed, actual："+str(actual)+"\nexpect: "+str(expect))
		return False
	for i in range(len(expect)):
		logger.info("循环Check Starting")
		res = AssertPy(tbName, actual[i], expect[i])
		if not res:
			check_result = res
	return check_result


