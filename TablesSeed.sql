-- Insert test data into Users table
INSERT INTO Users (username, password, role) VALUES
('john_doe', 'hashed_password1', 'member'),
('jane_smith', 'hashed_password2', 'librarian'),
('alice_wonder', 'hashed_password3', 'member'),
('bob_builder', 'hashed_password4', 'member');

-- Insert test data into Books table
INSERT INTO Books (title, author, available) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', TRUE),
('To Kill a Mockingbird', 'Harper Lee', TRUE),
('1984', 'George Orwell', FALSE),
('Moby Dick', 'Herman Melville', TRUE),
('War and Peace', 'Leo Tolstoy', FALSE);

-- Insert test data into Loans table
INSERT INTO Loans (user_id, book_id, loan_date, return_date) VALUES
(1, 3, '2024-12-28', '2025-01-10'),  -- John borrowed 1984
(3, 5, '2024-12-29', '2025-01-12'),  -- Alice borrowed War and Peace
(4, 2, '2024-12-30', '2025-01-15');  -- Bob borrowed To Kill a Mockingbird
