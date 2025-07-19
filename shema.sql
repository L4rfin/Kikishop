CREATE
DATABASE kikshop;
USE
kikshop;
CREATE TABLE assortment
(
    id               BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name             VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    img              BLOB                                not NULL,
    price            FLOAT                               NOT NULL,
    amount           SMALLINT                            not NULL,
    type             VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    variant          VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    tags             VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    feature          VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    character_source VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    renewable        VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    drop_data        DATE                                NOT NULL
);

CREATE TABLE client_order
(
    id              BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    items           VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    price           FLOAT                               NOT NULL,
    city            VARCHAR(30) COLLATE utf8_polish_ci NOT NULL,
    street          VARCHAR(50) COLLATE utf8_polish_ci NOT NULL,
    postal_code     VARCHAR(15) COLLATE utf8_polish_ci NOT NULL,
    building_number VARCHAR(10) COLLATE utf8_polish_ci NOT NULL,
    local_number    VARCHAR(10) COLLATE utf8_polish_ci NOT NULL,
    status          VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    order_data      DATE                                NOT NULL

);

CREATE
USER 'shopUser'@'localhost' IDENTIFIED VIA mysql_native_password USING '***';GRANT SELECT, UPDATE ON *.* TO
'shopUser'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;