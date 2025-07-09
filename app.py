import base64
import json

from flask import Flask, session, render_template
from database.models.assortment import Assortment
from database.database_session_manager import SessionManager
app = Flask(__name__)


@app.route('/KikFronPage')
def fron_page():
    session_object = SessionManager()
    items_list = session_object.session.query(Assortment).all()
    json_list = json.dumps([
                {'id':item.id,
                 'name':item.name,
                 'picture': base64.b64encode(item.img).decode('utf-8'),
                 'price':item.price,
                 'amount':item.amount,
                 'type':item.type,
                 'genre':item.genre,
                 'character_source':item.character_source,
                 'renewable': item.renewable,
                 'drop_data':item.drop_data.isoformat()
                 } for item in items_list ])
    return render_template("fron_page.html",
                           items= json_list
                           )

@app.route('/KikList')
def list_page():
    return render_template("list_page.html")


if __name__ == '__main__':
    app.run()

def session_setting():
    app.secret_key = "super duper secret key, no one gonna know"
    session.clear()
