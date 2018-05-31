#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__ = 'Steven Duan'

import asyncio, logging

import aiomysql   #连接数据库

def log(sql, args = ()):
	logging.info('SQL: %s' % sql)

#创建连接池，连接数据库
async def create_pool(loop, **kw):
	logging.info('create database connction pool...')
	global __pool
	__pool = await aiomysql.create_pool(
		host = kw.get('host','localhost'),
		port = kw.get('port', 3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charset = kw.get('charset','utf-8'),
		autocommit = kw.get('autocommit', True),
		maxsize = kw.get('maxsize', 10),
		minsize = kw.get('minsize', 1),
		loop = loop
		)

#要执行select语句，用select函数执行，需要传入sql语句和sql参数
async def select(sql, args, size = None):
	log(sql, args)
	global __pool
	async with __pool.get() as conn:
		async cur.execute(sql.replace('?', '%s'), args or ())
		if size:
			rs = await cur.fetchmany(size):
		else:
			rs = await cur.fatchall()
	logging.info('rows returned: %s' % len(rs))
	return rs




