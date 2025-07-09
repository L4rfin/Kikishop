CREATE
DATABASE kikshop;
USE
kikshop;
CREATE TABLE assortment
(
    id               BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name             VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    img              BLOB                                not NULL,
    price            FLOAT                               NOT NULL,
    amount           SMALLINT                            not NULL,
    type             VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    genre            VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    character_source VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    renewable        VARCHAR(255) COLLATE utf8_polish_ci NOT NULL,
    drop_data        DATE                                NOT NULL
);

CREATE
USER 'shopUser'@'localhost' IDENTIFIED VIA mysql_native_password USING '***';GRANT SELECT, UPDATE ON *.* TO
'shopUser'@'localhost' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;