


CREATE TABLE urls (
             id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
             name VARCHAR(255),
             created_at DATE DEFAULT timestamp);


CREATE TABLE url_cheks (
             id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
             url_id bigint REFERENCES urls(id),
             status_code VARCHAR(255),
             h1 VARCHAR(255),
             title VARCHAR(255),
             description text,
             created_at DATE DEFAULT timestamp
             );