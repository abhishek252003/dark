
DROP TABLE IF EXISTS products;

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  price REAL NOT NULL,
  category TEXT NOT NULL
);

INSERT INTO products (name, description, price, category) VALUES
  ('Flux Capacitor', 'Enables time travel. Requires 1.21 gigawatts.', 1985000.55, 'electronics'),
  ('Self-Lacing Shoes', 'The future of footwear. Power laces for a perfect fit.', 2015.00, 'electronics'),
  ('The Hitchhiker''s Guide', 'An indispensable guide for interstellar travelers.', 42.00, 'books'),
  ('Necronomicon', 'Ancient tome of forbidden knowledge. May summon elder gods.', 999.99, 'books');
