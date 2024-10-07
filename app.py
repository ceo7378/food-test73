from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ホームページ
@app.route('/')
def index():
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM stocks').fetchall()
    conn.close()
    return render_template('index.html', stocks=stocks)

# 購入品一覧ページ
@app.route('/items')
def item_list():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('item_list.html', items=items)

# 在庫一覧ページ
@app.route('/stocks')
def stock_list():
    conn = get_db_connection()
    stocks = conn.execute('SELECT items.name, stocks.quantity, stocks.last_updated FROM stocks JOIN items ON stocks.item_id = items.id').fetchall()
    conn.close()
    return render_template('stock_list.html', stocks=stocks)

# 廃棄品一覧ページ
@app.route('/discards')
def discard_list():
    conn = get_db_connection()
    discards = conn.execute('SELECT items.name, discards.discard_date, discards.reason, discards.discarded_quantity FROM discards JOIN items ON discards.item_id = items.id').fetchall()
    conn.close()
    return render_template('discard_list.html', discards=discards)

# 購入品追加フォーム
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        expiration_date = request.form['expiration_date']
        purchase_date = datetime.now().strftime('%Y-%m-%d')

        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, quantity, purchase_date, price, expiration_date) VALUES (?, ?, ?, ?, ?)', 
                     (name, quantity, purchase_date, price, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('item_list'))
    
    return render_template('add_item.html')

# 廃棄品登録フォーム
@app.route('/discard_item', methods=['GET', 'POST'])
def discard_item():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        discarded_quantity = int(request.form['discarded_quantity'])
        reason = request.form['reason']
        discard_date = datetime.now().strftime('%Y-%m-%d')

        conn = get_db_connection()
        conn.execute('UPDATE stocks SET quantity = quantity - ? WHERE item_id = ?', (discarded_quantity, item_id))
        conn.execute('INSERT INTO discards (item_id, discard_date, reason, discarded_quantity) VALUES (?, ?, ?, ?)', 
                     (item_id, discard_date, reason, discarded_quantity))
        conn.execute('DELETE FROM stocks WHERE item_id = ? AND quantity = 0', (item_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('discard_list'))

    return render_template('discard_item.html')

# 合計金額をグラフで表示するページ
@app.route('/total_graph')
def total_graph():
    conn = get_db_connection()
    items = conn.execute('SELECT name, price FROM items').fetchall()
    conn.close()
    return render_template('total_graph.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
