CREATE TABLE itens (
    slug VARCHAR NOT NULL,
    name VARCHAR,
    price smallint,
    type varchar,
    amount smallint,
    PRIMARY KEY(slug)
);

CREATE TABLE set_parts(
    set_slug VARCHAR NOT NULL,
    part_slug VARCHAR NOT NULL,
    amount SMALLINT,
    PRIMARY KEY(set_slug,part_slug),
    CONSTRAINT chave_set
        FOREIGN KEY(set_slug)
            REFERENCES itens(slug)
        ON DELETE CASCADE,
    CONSTRAINT chave_part
        FOREIGN KEY(part_slug)
            REFERENCES itens(slug)
        ON DELETE CASCADE
)