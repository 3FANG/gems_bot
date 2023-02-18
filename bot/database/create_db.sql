CREATE TABLE IF NOT EXISTS Users(
    id BIGINT PRIMARY KEY,
    username VARCHAR(30),
    first_name TEXT,
    last_name TEXT,
    registed timestamptz DEFAULT now(),
    referral BIGINT REFERENCES Users(id),
    balance INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Games(
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS Goods(
    id SERIAL PRIMARY KEY,
    title TEXT,
    price INT,
    game_id INT REFERENCES Game(id),
    available BOOLEAN DEFAULT TRUE
);

-- Переделать
CREATE TABLE IF NOT EXISTS Orders(
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES Users(id),
    good_id INT REFERENCES Goods(id),
    payed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Promos(
    id SERIAL PRIMARY KEY,
    name TEXT,
    value INT,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Used_Promos(
    user_id BIGINT REFERENCES Users(id),
    promo_id INT REFERENCES Promos(id),
    PRIMARY KEY(user_id, promo_id)
);

CREATE TABLE IF NOT EXISTS Invoices(
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES Users(id),
    value INT,
    date_of_payment timestamptz DEFAULT now()
);
