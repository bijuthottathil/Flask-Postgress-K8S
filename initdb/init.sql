CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO inventory (product_name, category, quantity, price) VALUES
('Laptop Pro X15', 'Electronics', 50, 1200.00);

INSERT INTO inventory (product_name, category, quantity, price) VALUES
('Wireless Mouse M300', 'Accessories', 200, 25.50);

INSERT INTO inventory (product_name, category, quantity, price) VALUES
('Ergonomic Office Chair', 'Furniture', 30, 189.99);

INSERT INTO inventory (product_name, category, quantity, price) VALUES
('4K LED Monitor 27-inch', 'Electronics', 75, 349.99);

INSERT INTO inventory (product_name, category, quantity, price) VALUES
('Stainless Steel Water Bottle', 'Kitchenware', 150, 15.00);

SELECT * FROM public.inventory
ORDER BY id ASC 