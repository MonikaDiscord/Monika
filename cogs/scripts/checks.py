import discord
from discord.ext import commands
from .settings import settings
import aiohttp
import sqlite3
import psycopg2

s = settings()

def admin_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT staff FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    return int(status) == 1


def dev_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT staff FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    print(status)
    return int(status) == 1 or int(status) == 2


def mod_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT staff FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    return int(status) == 1 or int(status) == 3


def staff_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT staff FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    return int(status) == 1 or int(status) == 2 or int(status) == 3


def patron_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT patron FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    return int(status) == 1 or int(status) == 2


def gold_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT patron FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    return int(status) == 2


def upvoter_check(ctx):
    db = psycopg2.connect(s.dsn)
    cursor = db.cursor()
    sql = "SELECT upvoter FROM users WHERE id = {}".format(ctx.author.id)
    cursor.execute(sql)
    status = cursor.fetchall()[0][0]
    return status == True


def is_admin():
    return commands.check(admin_check)


def is_dev():
    return commands.check(dev_check)


def is_mod():
    return commands.check(mod_check)


def is_staff():
    return commands.check(staff_check)


def is_patron():
    return commands.check(patron_check)


def is_gold():
    return commands.check(gold_check)


def is_upvoter():
    return commands.check(upvoter_check)
