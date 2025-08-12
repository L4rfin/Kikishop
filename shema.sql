CREATE
DATABASE kikshop;
USE
kikshop;
CREATE TABLE assortment
(
    id               BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    --general info
    name             VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    img              BLOB                               not NULL,
    price            FLOAT                              NOT NULL,
    amount           SMALLINT                           not NULL,
    renewable        VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    drop_data        DATE                               NOT NULL,
    amount_sold      BIGINT                             NOT NULL,

    --item tags
    type             VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    variant          VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    tags             VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    feature          VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    work_source VARCHAR(40) COLLATE utf8_polish_ci NOT NULL,
    material         VARCHAR(40) COLLATE utf8_polish_ci NOT NULL
);

CREATE TABLE delete_assortment
(
    id                  BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    item_id             BIGINT                             NOT NULL,
    cause               VARCHAR(50) COLLATE utf8_polish_ci NOT NULL,
    description_of_item VARCHAR(50) COLLATE utf8_polish_ci NOT NULL

);

CREATE TABLE client_order
(
    id              BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    --general order info
    name            VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    items           VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    items_amount    VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    price           FLOAT                               NOT NULL,
    status          VARCHAR(40) COLLATE utf8_polish_ci  NOT NULL,
    order_data      DATE                                NOT NULL,

    -- customer address
    city            VARCHAR(30) COLLATE utf8_polish_ci  NOT NULL,
    street          VARCHAR(50) COLLATE utf8_polish_ci  NOT NULL,
    postal_code     VARCHAR(15) COLLATE utf8_polish_ci  NOT NULL,
    cuntry          VARCHAR(10) COLLATE utf8_polish_ci  NOT NULL,
    building_number VARCHAR(10) COLLATE utf8_polish_ci  NOT NULL,
    -- contact address
    email           VARCHAR(40) COLLATE utf8_polish_ci  NOT NULL

);
CREATE TABLE statistic
(
    id                                 BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    visits                             BIGINT NOT NULL,
    amount_of_item_in_stock            INT    NOT NULL,

    --new order
    order_new                          INT    NOT NULL,
    amount_of_item_in_new_order        INT    NOT NULL,
    amount_of_money_in_new_order       BIGINT NOT NULL,

    --processed order
    order_processed                    INT    NOT NULL,
    amount_of_item_in_processed_order  INT    NOT NULL,
    amount_of_money_in_processed_order BIGINT NOT NULL,


    --finish order
    order_finish                       BIGINT NOT NULL,
    amount_of_item_sent                BIGINT NOT NULL,
    value_total                        BIGINT NOT NULL,

    --drop order
    order_drop                         BIGINT,
    drop_new_order                     BIGINT,
    drop_processed_order               BIGINT,
    drop_finsh_order                   BIGINT

);
CREATE TABLE statistic_monthly
(
    id                                 BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    visits                             BIGINT NOT NULL,
    data                               DATE   NOT NULL,

    --new order
    order_new                          INT,
    amount_of_item_in_new_order        INT,
    amount_of_money_in_new_order       BIGINT,

    --processed order
    order_processed                    INT,
    amount_of_item_in_processed_order  INT,
    amount_of_money_in_processed_order BIGINT,

    --finsh order
    order_finish                       BIGINT,
    amount_of_item_sent                BIGINT,
    value_total                        BIGINT,

    --drop order
    order_drop                         BIGINT,
    drop_new_order                     BIGINT,
    drop_processed_order               BIGINT,
    drop_finsh_order                   BIGINT,

    amount_of_item_in_order            INT,
    value_in_order                     INT
);

INSERT INTO `statistic` (`id`, `visits`, `amount_of_item_in_stock`, `order_new`, `amount_of_item_in_new_order`,
                         `amount_of_money_in_new_order`, `order_processed`, `amount_of_item_in_processed_order`,
                         `amount_of_money_in_processed_order`, `order_finish`, `amount_of_item_sent`, `value_total`,
                         `order_drop`, `drop_new_order`, `drop_processed_order`, `drop_finsh_order`)
VALUES ('0', '0',
        '0', '0',
        '0', '0',
        '0', '0',
        '0', '0',
        '0', '0',
        '0', '0',
        '0', '0');

CREATE
USER 'shopUser'@'localhost' IDENTIFIED VIA mysql_native_password USING '***';GRANT SELECT, UPDATE ON *.* TO
'shopUser'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;