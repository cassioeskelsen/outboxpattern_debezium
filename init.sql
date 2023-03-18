create table orders
(
    id            uuid not null
        constraint orders_pk
            primary key,
    customer_name varchar(50),
    order_total   float
);

create table outboxevent
(
    id            UUID PRIMARY KEY,
    aggregatetype character varying(100),
    aggregateid   character varying(50),
    payload       jsonb
);

ALTER USER postgres WITH REPLICATION;

CREATE PUBLICATION orders_publication FOR ALL TABLES;

SELECT PG_CREATE_LOGICAL_REPLICATION_SLOT('orders_publication_slot', 'pgoutput');
