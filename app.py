from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('food_stock07.db')
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

# 廃棄品一覧ページ
@app.route('/discards')
def discard_list():
    conn = get_db_connection()
    discards = conn.execute('''
        SELECT items.name, discards.discard_date, discards.reason, discards.discarded_quantity, items.price
        FROM discards
        JOIN items ON discards.item_id = items.id
    ''').fetchall()
    
    # 合計金額を計算
    total_price = sum(discard['discarded_quantity'] * discard['price'] for discard in discards)
    
    conn.close()
    return render_template('discard_list.html', discards=discards, total_price=total_price)

# 廃棄品登録フォーム
@app.route('/register_disposal', methods=['GET', 'POST'])
def register_disposal():
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
        
        flash('廃棄品が登録されました。')
        return redirect(url_for('discard_list'))
    
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('register_disposal.html', items=items)

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

# 合計金額をグラフで表示するページ
@app.route('/total_graph')
def total_graph():
    conn = get_db_connection()
    items = conn.execute('SELECT name, price FROM items').fetchall()
    conn.close()
    items_list = [{'name': item['name'], 'price': item['price']} for item in items]
    return render_template('total_graph.html', items=items_list)

# 月間廃棄数量グラフページ
@app.route('/monthly_discards')
def monthly_discards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y-%m', discard_date) as month, SUM(discarded_quantity) as total_quantity
        FROM discards
        GROUP BY month
        ORDER BY month
    ''')
    monthly_data = cursor.fetchall()
    conn.close()
    months = [row['month'] for row in monthly_data]
    quantities = [row['total_quantity'] for row in monthly_data]
    
    # デバッグ用に出力
    print("Months:", months)
    print("Quantities:", quantities)
    
    return render_template('monthly_discards.html', months=months, quantities=quantities)

# 購入品編集用のルート
@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        # 購入品の更新処理
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        purchase_date = request.form['purchase_date']
        expiration_date = request.form['expiration_date']

        conn.execute('UPDATE items SET name = ?, quantity = ?, price = ?, purchase_date = ?, expiration_date = ? WHERE id = ?',
                     (name, quantity, price, purchase_date, expiration_date, id))
        conn.commit()
        conn.close()

        return redirect(url_for('item_list'))

    return render_template('edit_item.html', item=item)

# 廃棄品編集用のルート
@app.route('/edit_discard/<int:item_id>', methods=['GET', 'POST'])
def edit_discard(item_id):
    conn = get_db_connection()
    discard = conn.execute('SELECT * FROM discards WHERE item_id = ?', (item_id,)).fetchone()

    if discard is None:
        # データが見つからない場合の処理
        return "指定された廃棄品が見つかりませんでした", 404

    if request.method == 'POST':
        # 廃棄品の更新処理
        discard_date = request.form['discard_date']
        reason = request.form['reason']
        discarded_quantity = int(request.form['discarded_quantity'])

        conn.execute('UPDATE discards SET discard_date = ?, reason = ?, discarded_quantity = ? WHERE item_id = ?',
                     (discard_date, reason, discarded_quantity, item_id))
        conn.commit()
        conn.close()

        return redirect(url_for('discard_list'))

    return render_template('edit_discard.html', discard=discard)





if __name__ == '__main__':
    app.run(debug=True)
