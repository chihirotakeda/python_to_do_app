from bottle import route, run, template, request, redirect
# from today_command import today_command
import sqlite3

dbname = 'to_do_items.db'
# conn = sqlite3.connect(dbname)
# c = conn.cursor()


@route("/list")
def index():
    item_list = get_list()
    return template('to_do_temp', item_list=item_list)


def get_list():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('select id, name from items order by id')
    item_list = []
    for row in c.fetchall():
        item_list.append({
            "id": row[0],
            "name": row[1]
        })
    conn.close()
    return item_list
    # return template('to_do_temp', item_list=item_list)


# @route("/to_do")
# def to_do():
#     return template('to_do_temp.html', add_item='', today_date='')
#
#
# @route("/to_do", method='POST')
# def do_to_do():
#     add_item = request.forms.add_item
#     today_date = today_command()
#     return template('to_do_temp.html', add_item=add_item, today_date=today_date)


@route("/list", method='POST')
def add_to_list():
    add_item = request.forms.getunicode('add_item')
    save_to_do(add_item)
    return redirect("/list")


def save_to_do(add_item):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    new_id = c.execute('SELECT max(id) + 1 FROM items').fetchone()[0]
    r = (new_id, add_item)
    c.execute('INSERT INTO items (id, name) VALUES (?, ?)', r)
    conn.commit()
    conn.close()


@route("/del/<item_id:int>")
def delete(item_id):
    del_item(item_id)
    redirect("/list")


def del_item(item_id):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()


run(host='localhost', port=8080, debug=True)

