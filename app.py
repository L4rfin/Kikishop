import base64
import datetime
import json
from datetime import timedelta

from flask import Flask, session, render_template, request, jsonify
from sqlalchemy import and_, select, or_

from database.database_session_manager import SessionManager
from database.models.assortment import Assortment
from database.models.order import Order
from database.models.staristic import Statistic

app = Flask(__name__)

total_number_of_visits = 0
total_number_of_items = 0


def stats_update():
    session_objet = SessionManager().session
    stats: Statistic = session_objet.get(Statistic, 0)
    stats.visits += 1
    global total_number_of_visits
    global total_number_of_items
    total_number_of_items = stats.amount_of_item
    total_number_of_visits = stats.visits
    session_objet.commit()


def get_stats():
    global total_number_of_visits
    global total_number_of_items
    session_objet = SessionManager().session
    stats: Statistic = session_objet.get(Statistic, 0)
    total_number_of_items = stats.amount_of_item
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
             'tags': item.item_tags,
             'feature': item.feature,
             'work_source': item.work_source,
             'renewable': item.renewable,
             'drop_data': item.drop_data.isoformat()
             } for item in results])
    if return_format == 'short':
        json_list = json.dumps([
            {'id': item.id,
             'name': item.name,
             'img': base64.b64encode(item.img).decode('utf-8'),
             'price': item.price,
             } for item in results])
    return json_list


def results_of_tags(tag_list):
    print("Otrzymano dane:", tag_list)
    types = tag_list.get("type", [])
    tags = tag_list.get("item_tags", [])
    sources = tag_list.get("work_source", [])
    feature = tag_list.get("feature", [])
    variant = tag_list.get("variant", [])

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
        'tags': Assortment.item_tags,
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
        .offset(0)
    )

    # Wykonanie zapytania
    results = stmt.all()
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
        Assortment.item_tags,
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
    return jsonify({"status": "ok", "received": results_of_tags(request.get_json())}), 200


@app.route('/sessionCartItemInfo', methods=['POST'])
def cart_items():
    return jsonify({"status": "ok", "received": results_of_id(request.get_json())}), 200


@app.route('/orderSender', methods=['POST'])
def order_sender():
    data = request.get_json()
    new_order = Order()
    new_order.name = data.get('name')
    new_order.items = data.get('items')
    new_order.price = data.get('price')
    new_order.city = data.get('city')
    new_order.street = data.get('street')
    new_order.postal_code = data.get('postal_code')
    new_order.cuntry = data.get('cuntry')
    new_order.location = data.get('location')
    new_order.building_number = data.get('building_number')
    new_order.email = data.get('contact_address')
    new_order.status = 'order resaved'
    new_order.order_data = datetime.datetime.now()
    object_db = SessionManager().session
    object_db.add(new_order)
    object_db.commit()
    return jsonify({"status": "ok", "received": new_order.id}), 200


if __name__ == '__main__':
    app.secret_key = "super duper secret key, no one gonna know"
    app.permanent_session_lifetime = timedelta(days=1)
    app.run(host="0.0.0.0", port=5000, debug=True)
