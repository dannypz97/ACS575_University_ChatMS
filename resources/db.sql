DROP TABLE IF exists chatbots;
DROP TABLE IF exists session_chats;
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
    1, # verify if ID for PFW in universities table is indeed 1
    'Daniyal Parveez',
    'parvd01@pfw.edu',
    '$2b$12$DP.kLTAef1DtPQOWQmwSf.WRfpmfNvx0xCwD4LiERHKfR7xlP2wsW',
    TRUE
),
(
    1, # verify if ID for PFW in universities table is indeed 1
    'Neel Singh',
    'singn03@pfw.edu',
    '$2b$12$RUFNSHIE0l1zc6lvZpXeJe.ETJTKqpePxyycVZmz50YtwiYE.stGS',
    TRUE
),
(
    1, # verify if ID for PFW in universities table is indeed 1
    'PFW Student1',
    'stud1@pfw.edu',
    '$2b$12$0l4OpVJBD1Z6jIYtNF9Sa.IyjCbWk19qBAImyWe2KhvzIhSUh6OVO',
    TRUE
);

CREATE TABLE chatbots (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    university_id INT NOT NULL,
    name VARCHAR(30),
    training_text LONGTEXT NOT NULL,
    is_trained BOOLEAN NOT NULL DEFAULT FALSE,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES universities(id),
    UNIQUE KEY chatbots_unique_university (university_id)
);

CREATE TABLE session_chats (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    bot_id INT,
    conversation JSON DEFAULT ('{}'),
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);