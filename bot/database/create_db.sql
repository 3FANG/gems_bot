CREATE TABLE IF NOT EXISTS Users(
    id BIGINT PRIMARY KEY,
    username VARCHAR(30),
    first_name TEXT,
    last_name TEXT,
    registed timestamptz DEFAULT now(),
    referral BIGINT REFERENCES Users(id),
    ref_link VARCHAR(30),
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
    game_id INT REFERENCES Games(id),
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Orders(
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES Users(id),
    good_id INT REFERENCES Goods(id),
    mail TEXT,
    registed timestamptz DEFAULT now(),
    status TEXT DEFAULT 'wait',
    code INT
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

CREATE TABLE IF NOT EXISTS Photos(
    id SERIAL PRIMARY KEY,
    photo_unique_id TEXT,
    photo_id TEXT,
    file_path TEXT,
    game_id INT REFERENCES Games(id)
);
