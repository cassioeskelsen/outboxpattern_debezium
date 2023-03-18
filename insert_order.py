import json
import uuid
from random import choice, uniform

import psycopg2
import psycopg2.extras

psycopg2.extras.register_uuid()  # see https://stackoverflow.com/a/59268003

DATABASE = "postgres"
USER = "postgres"
PASSWORD = "debezium"
HOST = "localhost"
PORT = "5432"

EVENT_TYPE = "order"


def insert_order(database, user, password, host, port):
    order_json = generate_order()
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO orders (id, customer_name, order_total) "
                "VALUES (%s, %s, %s)",
                (order_json['order_number'], order_json['customer_name'], order_json['order_total']))
            cur.execute(
                "INSERT INTO outboxevent (id, aggregatetype,aggregateid, payload) "
                "VALUES (%s, %s, %s, %s)",
                (uuid.uuid4(), EVENT_TYPE, str(uuid.uuid4()), json.dumps(order_json)))
            conn.commit()


def generate_order():
    order_number = str(uuid.uuid4())
    customer_name = choice(
        ["Alice", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gustavo", "Helena", "Isabela", "João", "Karina", "Luiz",
         "Maria", "Nathan", "Olivia", "Pedro", "Quezia", "Rafael", "Sara", "Thiago", "Ulisses", "Valentina", "Zeca"])
    order_total = round(uniform(500.0, 10000.0), 2)
    return {"order_number": order_number, "customer_name": customer_name, "order_total": order_total}


if __name__ == "__main__":
    insert_order(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
