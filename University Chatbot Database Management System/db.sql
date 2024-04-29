-- Query for creating the table
-- DROP TABLE IF exists question_response;
CREATE TABLE question_response ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(255),
    question TEXT,
    response TEXT,
    training_text LONGTEXT,
    university TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 );
