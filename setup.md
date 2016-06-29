Setup Guide
-------------

##**Step 1. Setup and configure MySQL**

1. Use following commands to install MySQL on an ubuntu machine:
```
echo "deb http://repo.mysql.com/apt/ubuntu/ precise mysql-apt-config" | sudo tee /etc/apt/sources.list.d/mysql.list
echo "deb http://repo.mysql.com/apt/ubuntu/ precise mysql-5.7" | sudo tee /etc/apt/sources.list.d/mysql.list
curl -s http://ronaldbradford.com/mysql/mysql.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y mysql-server
```

2. Log into MySQL server using proper credentials
```
mysql -u root -p <password>
```
Please note that these credentials will also be required for HTTP Server.

3. Create database and the following tables:
```
CREATE DATABASE <db_name>;
```
```
CREATE TABLE auth_admin (
    id INT(11) AUTO_INCREMENT,
    username VARCHAR(63) NOT NULL,
    password VARCHAR(63) NOT NULL,
    user_id VARCHAR(32) NOT NULL,
    token VARCHAR(63) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY (user_id)
);
```
```
CREATE TABLE articles_title (
    id INT(11) AUTO_INCREMENT,
    title VARCHAR(254) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);
```
```
CREATE TABLE articles_content (
    id INT(11) AUTO_INCREMENT,
    article_id INT(11) NOT NULL,
    paragraph_number INT(11) NOT NULL,
    text longtext,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY (article_id, paragraph_number),
    FOREIGN KEY (article_id) REFERENCES articles_title (id)
);
```
```
CREATE TABLE articles_comment (
    id INT(11) AUTO_INCREMENT,
    paragraph_id INT(11) NOT NULL,
    text longtext,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    FOREIGN KEY (paragraph_id) REFERENCES articles_content (id)
);
```

##**Step 2. Download python modules**

1. Download python pip
```
sudo apt-get install python-pip
```
2. Download all required modules from "requirements.txt" in the given package
```
sudo pip install -r requirements.txt
```