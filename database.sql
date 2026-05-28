CREATE DATABASE InventoryDB;
GO

USE InventoryDB;
GO

CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100),
    quantity INT,
    price FLOAT
);