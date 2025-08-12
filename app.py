import base64
import json
from datetime import timedelta

import jwt, datetime
from flask import Flask, session, render_template, request, jsonify
from sqlalchemy import and_, select, extract

from database.database_session_manager import SessionManager
from database.models.assortment import Assortment
from database.models.order import Order
from database.models.staristic import Statistic
from database.models.statistic_monthly import StatisticMonth

app = Flask(__name__)

total_number_of_visits = 0
total_number_of_items = 0
amount_of_item_on_page = 0


def stats_update():
    session_objet = SessionManager().session
    stats: Statistic = session_objet.query(Statistic).first()
    stats.visits += 1
    global total_number_of_visits
    global total_number_of_items
    total_number_of_items = stats.amount_of_item_in_stock
    total_number_of_visits = stats.visits
    session_objet.commit()


def get_stats():
    global total_number_of_visits
    global total_number_of_items
    session_objet = SessionManager().session
    stats: Statistic = session_objet.query(Statistic).first()
    total_number_of_items = stats.amount_of_item_in_stock
    total_number_of_visits = stats.visits


def visitors_check():
    session.permanent = True
    if 'created' not in session:
        # Nowa sesja
        session['created'] = datetime.datetime.now()
        stats_update()
        return "new session."
    else:
        get_stats()
        return "old session"


def results_to_json(results, return_format='long'):
    json_list = ''
    if return_format == 'long':
        json_list = json.dumps([
            {'id': item.id,
             'name': item.name,
             'picture': base64.b64encode(item.img).decode('utf-8'),
             'price': item.price,
             'amount': item.amount,
             'type': item.type,
             'variant': item.variant,
             'tags': item.tags,
             'feature': item.feature,
             'work_source': item.work_source,
             'renewable': item.renewable,
             'drop_data': item.drop_data.isoformat(),
             } for item in results])
    if return_format == 'short':
        json_list = json.dumps([
            {'id': item.id,
             'name': item.name,
             'picture': base64.b64encode(item.img).decode('utf-8'),
             'price': item.price,
             } for item in results])
    return json_list


def results_of_tags(tag_list):
    print("Otrzymano dane:", tag_list)
    global amount_of_item_on_page
    types = tag_list.get("type", [])
    tags = tag_list.get("item_tags", [])
    sources = tag_list.get("work_source", [])
    feature = tag_list.get("feature", [])
    variant = tag_list.get("variant", [])
    offset = tag_list.get('page')

    filters = {
        'type': types,
        'tags': tags,
        'work_source': sources,
        'feature': feature,
        'variant': variant,
    }

    # Mapujemy nazwy kluczy z filters na kolumny z modelu
    column_map = {
        'type': Assortment.type,
        'tags': Assortment.tags,
        'work_source': Assortment.work_source,
        'feature': Assortment.feature,
        'variant': Assortment.variant,
    }

    # Budujemy listę warunków tylko dla niepustych list
    conditions = [
        column_map[key].in_(values)
        for key, values in filters.items()
        if values
    ]

    # Tworzymy zapytanie z warunkami połączonymi logicznym AND
    stmt = (
        SessionManager()
        .session.query(Assortment)
        .where(and_(*conditions))
        .limit(10)
        .offset((offset * 10))
    )
    count = (
        SessionManager().session.query(Assortment).where(and_(*conditions)).count()
    )
    # Wykonanie zapytania
    results = stmt.all()
    amount_of_item_on_page = count
    return results_to_json(results)


def top_ten():
    session_object = SessionManager()
    items_list = session_object.session.query(Assortment).order_by(Assortment.drop_data.desc()).limit(10)
    return results_to_json(items_list)


def results_of_id(ids):
    results = SessionManager().session.query(Assortment).where(Assortment.id.in_(ids.get('ids'))).all()
    return results_to_json(results, 'short')


def distinct_tags():
    session_objet = SessionManager()
    # dist_type = session_objet.session.query(Assortment.type, Assortment.item_tags, Assortment.variant,
    #                                         Assortment.feature, Assortment.work_source).distinct().all()

    stmt = select(
        Assortment.type,
        Assortment.tags,
        Assortment.variant,
        Assortment.work_source,
        Assortment.feature,
    )
    results = session_objet.session.execute(stmt).all()
    result_dict = {
        "type": set(),
        "item_tags": set(),
        "variant": set(),
        "work_source": set(),
        "feature": set()
    }

    for row in results:
        result_dict["type"].add(row[0])
        result_dict["item_tags"].add(row[1])
        result_dict["variant"].add(row[2])
        result_dict["feature"].add(row[3])
        result_dict["work_source"].add(row[4])

    # Zamień sety na listy (bo set nie jest JSON-serializowalny)
    list_of_dist_type = tuple(result_dict["type"])
    list_of_dist_tags = tuple(result_dict["item_tags"])
    list_of_dist_variant = tuple(result_dict["variant"])
    list_of_dist_feature = tuple(result_dict["work_source"])
    list_of_dist_source = tuple(result_dict["feature"])
    data = {
        "type": list_of_dist_type,
        "tags": list_of_dist_tags,
        "variant": list_of_dist_variant,
        "feature": list_of_dist_feature,
        "source": list_of_dist_source
    }
    json_list = json.dumps(data)
    return json_list


def decoder(token):
    try:
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        print(decoded)
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


@app.route('/KikFronPage')
def fron_page():
    visitors_check()
    return render_template("fron_page.html",
                           items=top_ten(),
                           visitors=total_number_of_visits,
                           number_of_items=total_number_of_items
                           )


@app.route('/KikList')
def list_page():
    visitors_check()
    global total_number_of_visits
    global total_number_of_items

    return render_template("list_page.html", items=distinct_tags())


@app.route('/search', methods=['POST'])
def search_results():
    answer = results_of_tags(request.get_json())
    return jsonify({"status": "ok", "received": answer, "amount": amount_of_item_on_page}), 200


@app.route('/sessionCartItemInfo', methods=['POST'])
def cart_items():
    return jsonify({"status": "ok", "received": results_of_id(request.get_json())}), 200


@app.route('/orderSender', methods=['POST'])
def order_sender():
    data = request.get_json()
    new_order = Order()
    new_order.name = data.get('name')
    new_order.items = data.get('items')
    new_order.items_amount = data.get('items_amount')
    new_order.price = data.get('price')
    new_order.city = data.get('city')
    new_order.street = data.get('street')
    new_order.postal_code = data.get('postal_code')
    new_order.cuntry = data.get('cuntry')
    new_order.location = data.get('location')
    new_order.building_number = data.get('building_number')
    new_order.email = data.get('contact_address')
    new_order.status = 'new'
    new_order.order_data = datetime.datetime.now()
    object_db = SessionManager().session
    object_db.add(new_order)
    object_db.commit()

    statistic_frame = dict()
    statistic_frame['operation'] = 'new'
    statistic_frame['items_amount'] = sum(int(x) for x in new_order.items_amount.split(",") if x)
    statistic_frame['price'] = new_order.price

    update_statistic_order(order=statistic_frame)
    return jsonify({"status": "ok", "received": new_order.id}), 200


@app.route('/mobileAppLogin', methods=['POST'])
def mobile_app_login():
    login = request.json
    if login["username"] == "kiki@gmale.com" or login["username"] == "kiki" and login["password"] == "k3.A.W.L.W.A":
        token = jwt.encode({
            "user": login["username"],
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return jsonify({"token": token})
    return jsonify({"error": "login error"}), 401


def update_item():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if decoder(token):
        data = request.get_json()
        db_session = SessionManager().session
        db_item = db_session.query(Assortment).filter_by(id=data.get('id')).first()
        statistic = dict()
        statistic['operation'] = 'insert'
        if data.get('name'):
            db_item.name = data.get('name')
        if data.get('img'):
            db_item.img = data.get('img')
        if data.get('price'):
            db_item.price = data.get('price')
        if data.get('amount'):
            statistic['amount'] = data.get('amount')
            db_item.amount = db_item.amount + data.get('amount')
        if data.get('type'):
            db_item.type = data.get('type')
        if data.get('variant'):
            db_item.variant = data.get('variant')
        if data.get('item_tags'):
            db_item.item_tags = data.get('item_tags')
        if data.get('feature'):
            db_item.feature = data.get('feature')
        if data.get('work_source'):
            db_item.work_source = data.get('work_source')
        if data.get('renewable'):
            db_item.renewable = data.get('renewable')
        if data.get('material'):
            db_item.material = data.get('material')

        db_session.commit()

        update_statistic_item(statistic)


@app.route('/insertItemSecureAccess', methods=['POST'])
def insert_item():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if decoder(token):
        data = request.get_json()
        statistic = dict()
        db_session = SessionManager().session
        new_item = Assortment()
        new_item.name = data.get('name')
        new_item.img = data.get('img')
        new_item.price = data.get('price')
        statistic['amount'] = data.get('amount')
        new_item.amount = data.get('amount')
        new_item.type = data.get('type')
        new_item.variant = data.get('variant')
        new_item.item_tags = data.get('item_tags')
        new_item.feature = data.get('feature')
        new_item.work_source = data.get('work_source')
        new_item.renewable = data.get('renewable')
        new_item.material = data.get('material')
        db_session.commit()

        update_statistic_item(statistic)

        return jsonify({"success": "Item updated"})
    return jsonify({"error": "Token error"}), 401


@app.route('/updateOrderSecureAccess', methods=['POST'])
def update_order():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if decoder(token):
        data = request.get_json()
        db_session = SessionManager().session
        db_order = db_session.query(Order).filter_by(id=data.get('id')).first()
        if db_order:
            db_order.status = data.get('status')
        db_session.commit()
        statistic_frame = dict()
        statistic_frame['operation'] = data.get('status')
        statistic_frame['items_amount'] = sum(int(x) for x in db_order.items_amount.split(",") if x)
        statistic_frame['price'] = db_order.price

        update_statistic_order(statistic_frame)
        return jsonify({"success": "Order updated"})
    return jsonify({"error": "Token error"}), 401


def update_statistic_order(order):
    db_session = SessionManager().session
    db_statistic: Statistic = db_session.query(Statistic).filter(Statistic.id == 1).first()
    now = datetime.datetime.now()
    db_statistic_m: StatisticMonth = db_session.query(StatisticMonth).filter(
        extract('year', StatisticMonth.data) == now.year).filter(
        extract('month', StatisticMonth.data) == now.month).first()

    if order['operation'] == 'new':
        db_statistic.order_new += 1
        db_statistic.amount_of_item_in_new_order += order['items_amount']
        db_statistic.amount_of_money_in_new_order += order['price']
        db_statistic_m.order_new += 1
        db_statistic_m.amount_of_item_in_new_order += order['items_amount']
        db_statistic_m.amount_of_money_in_new_order += order['price']

    if order['operation'] == 'processed':
        db_statistic.order_processed += 1
        db_statistic.amount_of_item_in_processed_order += order['items_amount']
        db_statistic.amount_of_money_in_processed_order += order['price']
        db_statistic_m.order_processed += 1
        db_statistic_m.amount_of_item_in_processed_order += order['items_amount']
        db_statistic_m.amount_of_money_in_processed_order += order['price']

        db_statistic.order_new -= 1
        db_statistic.amount_of_item_in_new_order -= order['items_amount']
        db_statistic.amount_of_money_in_new_order -= order['price']
        db_statistic_m.order_new -= 1
        db_statistic_m.amount_of_item_in_new_order -= order['items_amount']
        db_statistic_m.amount_of_money_in_new_order -= order['price']

    if order['operation'] == 'finish':
        db_statistic.order_finish += 1
        db_statistic.amount_of_item_sent += order['items_amount']
        db_statistic.value_total += order['price']
        db_statistic_m.order_finish += 1
        db_statistic_m.amount_of_item_sent += order['items_amount']
        db_statistic_m.value_total += order['price']

        db_statistic.order_processed -= 1
        db_statistic.amount_of_item_in_processed_order -= order['items_amount']
        db_statistic.amount_of_money_in_processed_order -= order['price']
        db_statistic_m.order_processed -= 1
        db_statistic_m.amount_of_item_in_processed_order -= order['items_amount']
        db_statistic_m.amount_of_money_in_processed_order -= order['price']

    if order['operation'] == 'drop':
        if order['state'] == 'new':
            db_statistic.order_new -= 1
            db_statistic.amount_of_item_in_new_order -= order['items_amount']
            db_statistic.amount_of_money_in_new_order -= order['price']
            db_statistic_m.order_new -= 1
            db_statistic_m.amount_of_item_in_new_order -= order['items_amount']
            db_statistic_m.amount_of_money_in_new_order -= order['price']
        if order['state'] == 'processed':
            db_statistic.order_processed -= 1
            db_statistic.amount_of_item_in_processed_order -= order['items_amount']
            db_statistic.amount_of_money_in_processed_order -= order['price']
            db_statistic_m.order_processed -= 1
            db_statistic_m.amount_of_item_in_processed_order -= order['items_amount']
            db_statistic_m.amount_of_money_in_processed_order -= order['price']
        if order['state'] == 'finish':
            db_statistic.order_finish -= 1
            db_statistic.amount_of_item_sent -= order['items_amount']
            db_statistic.value_total -= order['price']
            db_statistic_m.order_finish -= 1
            db_statistic_m.amount_of_item_sent -= order['items_amount']
            db_statistic_m.value_total -= order['price']

    db_session.commit()


def update_statistic_item(item):
    db_session = SessionManager().session
    db_statistic: Statistic = db_session.query(Statistic).filter(Statistic.id == 1).first()
    if item['operation'] == 'insert':
        db_statistic.amount_of_item_in_stock += item['amount']
    if item['operation'] == 'update':
        db_statistic.amount_of_item_in_stock += item['amount']
    db_session.commit()


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "there is no option someone gonna know it, you get it please don't do a mess"
    app.secret_key = "super duper secret key, no one gonna know"
    app.permanent_session_lifetime = timedelta(days=1)
    app.run(host="0.0.0.0", port=5000, debug=True)
