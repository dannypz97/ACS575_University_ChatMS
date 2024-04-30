DROP TABLE IF exists chatbots;
DROP TABLE IF exists user_chats;
DROP TABLE IF exists users;
DROP TABLE IF exists universities;

CREATE TABLE universities (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    address TEXT,
    phone VARCHAR(20) NOT NULL,
    email_domain VARCHAR(15) NOT NULL,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO universities(name, address, phone, email_domain) VALUES (
    'Purdue Fort Wayne',
    '2101 E Coliseum Blvd, Fort Wayne, IN 46805',
    '(260) 481-6100',
    '@pfw.edu'
),
(
    'Purdue University',
    '610 Purdue Mall, West Lafayette, IN 47907',
    '(765) 494-4600',
    '@purdue.edu'
);

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    university_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(35) NOT NULL,
    password BINARY(60) NOT NULL,
    phone VARCHAR(20),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES universities(id),
    UNIQUE KEY users_unique_email (email)
);

INSERT INTO users(university_id, name, email, password, is_admin) VALUES (
    1, #verify if ID for PFW in universities table is indeed 1
    'Daniyal Parveez',
    'parvd01@pfw.edu',
    '$2b$12$DP.kLTAef1DtPQOWQmwSf.WRfpmfNvx0xCwD4LiERHKfR7xlP2wsW', #Password: root
    TRUE
),
(
    1, #verify if ID for PFW in universities table is indeed 1
    'Neel Singh',
    'singn03@pfw.edu',
    '$2b$12$RUFNSHIE0l1zc6lvZpXeJe.ETJTKqpePxyycVZmz50YtwiYE.stGS', #Password: root
    TRUE
),
(
    1, #verify if ID for PFW in universities table is indeed 1
    'PFW Student1',
    'stud1@pfw.edu',
    '$2b$12$OtqXoyvl5RX6xivsrBC.LeTdxSGAukPnVJQXfK9YspaMzuKdpCIHu', #Password: root123
    FALSE
),
(
    1, #verify if ID for PFW in universities table is indeed 1
    'PFW Student2',
    'stud2@pfw.edu',
    '$2b$12$C97Cv2tYyEhH8pVxgX8k7eciB3oUMwot/COnkOCe5CNAtWMsrqV7y', #Password: root123
    FALSE
),
(
    2, #verify if ID for Purdue in universities table is indeed 2
    'Purdue Admin1',
    'admin1@purdue.edu',
    '$2b$12$IeD327.9yus32ygJTuij3.ECGNsv10WezOuY9PicOmQrncMfY3EUG', #Password: proot
    TRUE
),
(
    2, #verify if ID for Purdue in universities table is indeed 2
    'Purdue Admin2',
    'admin2@purdue.edu',
    '$2b$12$WjMb31NlOTAzZWuGUoBkCegiAtZvTXpSYZF80lHxY9h5LXQAhcaPO', #Password: proot
    TRUE
),
(
    2, #verify if ID for Purdue in universities table is indeed 2
    'Purdue Student1',
    'stud1@purdue.edu',
    '$2b$12$3SepamsciX6PUbScXuOjF.O/3YhZGmhi3AG3m9FAZmapDcDg3GOky', #Password: proot123
    FALSE
),
(
    2, #verify if ID for Purdue in universities table is indeed 2
    'Purdue Student2',
    'stud2@purdue.edu',
    '$2b$12$cSIKhDZDsRgPGyWUQbbzYe1nWiNos0B8peXiQE5YTwbqJ65WjmLNi', #Password: proot123
    FALSE
),
;

CREATE TABLE chatbots (
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(30),
    training_text LONGTEXT NOT NULL,
    is_trained BOOLEAN NOT NULL DEFAULT FALSE,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES universities(id)
);

CREATE TABLE user_chats (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    source varchar(15) NOT NULL,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);