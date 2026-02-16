INSERT INTO users (name, email, phone, age, country, city) VALUES
('Alice Smith', 'alice.smith@example.com', '111-222-3333', 30, 'USA', 'New York'),
('Bob Johnson', 'bob.johnson@example.com', '444-555-6666', 24, 'Canada', 'Toronto'),
('Charlie Brown', 'charlie.brown@example.com', '777-888-9999', 35, 'UK', 'London');

INSERT INTO departments (name, location) VALUES
('Sales', 'Building A'),
('Marketing', 'Building B'),
('Engineering', 'Building C');

INSERT INTO employees (name, email, department_id, manager_id, salary, hire_date) VALUES
('John Doe', 'john.doe@example.com', 3, NULL, 75000.00, '2022-01-15'),
('Jane Smith', 'jane.smith@example.com', 3, 1, 80000.00, '2021-06-01'),
('Peter Jones', 'peter.jones@example.com', 1, NULL, 60000.00, '2023-03-10');

INSERT INTO categories (name, description) VALUES
('Electronics', 'Gadgets and electronic devices'),
('Books', 'Various genres of books'),
('Apparel', 'Clothing and accessories');

INSERT INTO suppliers (name, country, contact_email) VALUES
('Tech Supplies Inc.', 'USA', 'contact@techsupplies.com'),
('Bookworm Distributors', 'UK', 'info@bookworm.com'),
('Fashion Forward Ltd.', 'Canada', 'sales@fashionforward.ca');

INSERT INTO products (name, description, category_id, supplier_id, price, stock) VALUES
('Laptop Pro', 'High-performance laptop', 1, 1, 1200.00, 50),
('SQL for Dummies', 'Beginner guide to SQL', 2, 2, 25.00, 200),
('Winter Jacket', 'Warm winter coat', 3, 3, 150.00, 100);

INSERT INTO orders (user_id, product_id, quantity, order_date, status) VALUES
(1, 1, 1, '2024-01-20', 'delivered'),
(2, 2, 2, '2024-01-22', 'shipped'),
(1, 3, 1, '2024-01-25', 'pending');

INSERT INTO reviews (product_id, user_id, rating, comment, review_date) VALUES
(1, 1, 5, 'Excellent laptop, very fast!', '2024-01-28'),
(2, 2, 4, 'Good book for beginners.', '2024-01-30'),
(3, 1, 3, 'Jacket is okay, a bit thin.', '2024-02-01');
