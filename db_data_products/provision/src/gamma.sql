USE CATALOG {{catalog}};
CREATE SCHEMA IF NOT EXISTS gamma;
USE gamma;

CREATE TABLE IF NOT EXISTS things (
    id BIGINT NOT NULL,
    alpha_id BIGINT NOT NULL,
    gamma_id BIGINT NOT NULL,
    content STRING NOT NULL,
    created TIMESTAMP,
);