USE CATALOG {{catalog}};
CREATE SCHEMA IF NOT EXISTS beta;
USE beta;

CREATE TABLE IF NOT EXISTS things (
    id BIGINT NOT NULL,
    content STRING NOT NULL,
    created TIMESTAMP
);