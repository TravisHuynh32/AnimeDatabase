CREATE DATABASE anime; 

CREATE TABLE anime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    genres TEXT,
    rating DECIMAL(3, 2),
    synopsis TEXT,
    url VARCHAR(255)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    location VARCHAR(255)
);

INSERT INTO users (username, email, age, gender, location)
VALUES ('Travis Huynh', 'huynhtk51@gmail.com', 20, 'Male', 'Olympia, Washington');

CREATE TABLE ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    anime_id INT,
    rating FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (anime_id) REFERENCES anime(id)
);

INSERT INTO ratings (user_id, anime_id, rating) VALUES (1, 30, 9);


SELECT * FROM anime;
SELECT * FROM users; 
SELECT * FROM ratings; 
