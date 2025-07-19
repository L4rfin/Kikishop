import base64
import json

from flask import Flask, session, render_template, request, jsonify
from sqlalchemy import select, and_
from database.models.assortment import Assortment
from database.database_session_manager import SessionManager

app = Flask(__name__)


@app.route('/KikFronPage')
def fron_page():
    session_object = SessionManager()
    items_list = session_object.session.query(Assortment).order_by(Assortment.drop_data.desc()).all()
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
         } for item in items_list])
    return render_template("fron_page.html",
                           items=json_list
                           )


@app.route('/KikList')
def list_page():
    session_objet = SessionManager()
    dist_type = session_objet.session.query(Assortment.type).order_by(Assortment.type.desc()).distinct().all()
    dist_tags = session_objet.session.query(Assortment.item_tags).order_by(Assortment.item_tags.desc()).distinct().all()
    dist_variant = session_objet.session.query(Assortment.variant).order_by(Assortment.variant.desc()).distinct().all()
    dist_feature = session_objet.session.query(Assortment.feature).order_by(Assortment.feature.desc()).distinct().all()
    dist_source = session_objet.session.query(Assortment.work_source).order_by(Assortment.type.desc()).distinct().all()
    list_of_dist_type = tuple(x.type for x in dist_type)
    list_of_dist_tags = tuple(x.item_tags for x in dist_tags)
    list_of_dist_variant = tuple(x.variant for x in dist_variant)
    list_of_dist_feature = tuple(x.feature for x in dist_feature)
    list_of_dist_source = tuple(x.work_source for x in dist_source)
    data = {
        "type": list_of_dist_type,
        "tags": list_of_dist_tags,
        "variant": list_of_dist_variant,
        "feature": list_of_dist_feature,
        "source": list_of_dist_source
    }
    json_list = json.dumps(data)

    return render_template("list_page.html",
                           items=json_list)


@app.route('/search', methods=['POST'])
def search_results():
    data = request.get_json()  # Odbiera JSON z żądania
    print("Otrzymano dane:", data)
    types = data.get("type", [])
    tags = data.get("tags", [])
    sources = data.get("source", [])
    feature = data.get("feature", [])
    variant = data.get("variant", [])

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
    print(json_list)
    return jsonify({"status": "ok", "received": json_list}), 200

@app.route('/sessionCartItemInfo', methods=['POST'])
def cart_items():
    data = request.get_json()  # Odbiera JSON z żądania
    print(data)


    results = SessionManager().session.query(Assortment).where(Assortment.id.in_(data.get('ids'))).all()

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
    print(json_list)
    return jsonify({"status": "ok", "received": json_list}), 200
if __name__ == '__main__':
    app.run()


def session_setting():
    app.secret_key = "super duper secret key, no one gonna know"
    session.clear()
