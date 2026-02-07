-- USERS (15)
INSERT INTO users (name, email, phone, age, country, city) VALUES
('User One', 'user1@mail.com', '1111111111', 25, 'India', 'Delhi'),
('User Two', 'user2@mail.com', '2222222222', 28, 'India', 'Mumbai'),
('User Three', 'user3@mail.com', '3333333333', 22, 'India', 'Bangalore'),
('User Four', 'user4@mail.com', '4444444444', 35, 'USA', 'New York'),
('User Five', 'user5@mail.com', '5555555555', 30, 'USA', 'Chicago'),
('User Six', 'user6@mail.com', '6666666666', 27, 'UK', 'London'),
('User Seven', 'user7@mail.com', '7777777777', 40, 'Germany', 'Berlin'),
('User Eight', 'user8@mail.com', '8888888888', 29, 'France', 'Paris'),
('User Nine', 'user9@mail.com', '9999999999', 34, 'India', 'Pune'),
('User Ten', 'user10@mail.com', '1010101010', 26, 'India', 'Kolkata'),
('User Eleven', 'user11@mail.com', '1111111110', 31, 'Canada', 'Toronto'),
('User Twelve', 'user12@mail.com', '1212121212', 24, 'India', 'Chennai'),
('User Thirteen', 'user13@mail.com', '1313131313', 38, 'USA', 'Austin'),
('User Fourteen', 'user14@mail.com', '1414141414', 21, 'India', 'Jaipur'),
('User Fifteen', 'user15@mail.com', '1515151515', 33, 'Australia', 'Sydney');

-- DEPARTMENTS (5)
INSERT INTO departments (name, location) VALUES
('Engineering', 'Bangalore'),
('HR', 'Delhi'),
('Finance', 'Mumbai'),
('Sales', 'Pune'),
('Operations', 'Chennai');

-- EMPLOYEES (10)
INSERT INTO employees (name, email, department_id, manager_id, salary, hire_date) VALUES
('Alice', 'alice@company.com', 1, NULL, 90000, '2021-01-15'),
('Bob', 'bob@company.com', 1, 1, 75000, '2021-06-10'),
('Charlie', 'charlie@company.com', 2, NULL, 65000, '2020-03-20'),
('David', 'david@company.com', 3, NULL, 80000, '2019-11-01'),
('Eva', 'eva@company.com', 4, NULL, 70000, '2022-02-05'),
('Frank', 'frank@company.com', 1, 1, 72000, '2022-09-12'),
('Grace', 'grace@company.com', 5, NULL, 68000, '2020-07-18'),
('Henry', 'henry@company.com', 3, 4, 76000, '2021-08-22'),
('Ivy', 'ivy@company.com', 2, 3, 64000, '2023-01-10'),
('Jack', 'jack@company.com', 4, 5, 71000, '2022-04-14');

-- CATEGORIES (6)
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Books', 'Printed and digital books'),
('Clothing', 'Men and Women clothing'),
('Home', 'Home appliances and decor'),
('Sports', 'Sports equipment'),
('Beauty', 'Beauty and personal care');

-- SUPPLIERS (5)
INSERT INTO suppliers (name, country, contact_email) VALUES
('Supplier A', 'India', 'a@supplier.com'),
('Supplier B', 'USA', 'b@supplier.com'),
('Supplier C', 'China', 'c@supplier.com'),
('Supplier D', 'Germany', 'd@supplier.com'),
('Supplier E', 'UK', 'e@supplier.com');

-- PRODUCTS (20)
INSERT INTO products (name, description, category_id, supplier_id, price, stock) VALUES
('Laptop', '14 inch laptop', 1, 1, 75000, 20),
('Smartphone', 'Android phone', 1, 2, 30000, 50),
('Headphones', 'Noise cancelling', 1, 3, 5000, 100),
('Novel', 'Fiction book', 2, 4, 400, 200),
('Notebook', 'College notebook', 2, 5, 100, 500),
('T-Shirt', 'Cotton T-shirt', 3, 1, 800, 150),
('Jeans', 'Blue denim', 3, 2, 2000, 80),
('Sofa', '3-seater sofa', 4, 3, 35000, 10),
('Lamp', 'Table lamp', 4, 4, 1500, 60),
('Mixer', 'Kitchen mixer', 4, 5, 4500, 25),
('Football', 'Standard size', 5, 1, 1200, 40),
('Cricket Bat', 'English willow', 5, 2, 3500, 30),
('Yoga Mat', 'Anti-slip', 5, 3, 900, 70),
('Face Cream', 'Moisturizer', 6, 4, 600, 90),
('Perfume', 'Eau de parfum', 6, 5, 2500, 35),
('Tablet', '10 inch tablet', 1, 1, 28000, 22),
('E-reader', 'E-ink reader', 1, 2, 12000, 18),
('Jacket', 'Winter jacket', 3, 3, 4500, 40),
('Shoes', 'Running shoes', 5, 4, 3000, 55),
('Hair Dryer', '1200W dryer', 6, 5, 1800, 45);

-- ORDERS (25)
INSERT INTO orders (user_id, product_id, quantity, order_date, status) VALUES
(1, 1, 1, '2024-01-05', 'delivered'),
(2, 2, 2, '2024-01-10', 'shipped'),
(3, 3, 1, '2024-01-12', 'pending'),
(4, 4, 3, '2024-01-15', 'delivered'),
(5, 5, 5, '2024-01-18', 'shipped'),
(6, 6, 2, '2024-01-20', 'pending'),
(7, 7, 1, '2024-01-22', 'delivered'),
(8, 8, 1, '2024-01-25', 'pending'),
(9, 9, 2, '2024-01-27', 'shipped'),
(10, 10, 1, '2024-01-28', 'delivered'),
(11, 11, 3, '2024-02-01', 'pending'),
(12, 12, 1, '2024-02-03', 'shipped'),
(13, 13, 2, '2024-02-05', 'delivered'),
(14, 14, 1, '2024-02-07', 'pending'),
(15, 15, 1, '2024-02-10', 'shipped'),
(1, 16, 1, '2024-02-12', 'delivered'),
(2, 17, 2, '2024-02-14', 'pending'),
(3, 18, 1, '2024-02-16', 'shipped'),
(4, 19, 1, '2024-02-18', 'delivered'),
(5, 20, 2, '2024-02-20', 'pending'),
(6, 1, 1, '2024-02-22', 'shipped'),
(7, 2, 1, '2024-02-24', 'delivered'),
(8, 3, 2, '2024-02-26', 'pending'),
(9, 4, 1, '2024-02-28', 'shipped'),
(10, 5, 3, '2024-03-01', 'delivered');

-- REVIEWS (12)
INSERT INTO reviews (product_id, user_id, rating, comment, review_date) VALUES
(1, 1, 5, 'Excellent product', '2024-01-10'),
(2, 2, 4, 'Very good', '2024-01-12'),
(3, 3, 3, 'Average', '2024-01-14'),
(4, 4, 5, 'Loved it', '2024-01-16'),
(5, 5, 4, 'Worth the price', '2024-01-18'),
(6, 6, 2, 'Not great', '2024-01-20'),
(7, 7, 5, 'Perfect', '2024-01-22'),
(8, 8, 3, 'Okayish', '2024-01-24'),
(9, 9, 4, 'Nice quality', '2024-01-26'),
(10, 10, 5, 'Highly recommend', '2024-01-28'),
(11, 11, 4, 'Good value', '2024-02-01'),
(12, 12, 3, 'Decent', '2024-02-03');
