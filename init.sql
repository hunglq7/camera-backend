-- Create database if not exists
CREATE DATABASE IF NOT EXISTS camera_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE camera_management;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Create cameras table
CREATE TABLE IF NOT EXISTS cameras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    location VARCHAR(200),
    is_online BOOLEAN DEFAULT FALSE,
    last_check DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create tong_hop_camera table
CREATE TABLE IF NOT EXISTS tong_hop_camera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camera_id INT NOT NULL,
    total_scans INT DEFAULT 0,
    summary VARCHAR(255),
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (camera_id) REFERENCES cameras(id)
);