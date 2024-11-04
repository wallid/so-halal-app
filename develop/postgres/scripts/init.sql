-- Create the 'products' table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    barcode VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255),
    brands VARCHAR(255),
    status TEXT CHECK (status IN ('halal', 'not_halal', 'halal_given_ingredients', 'not_enough_information', 'unknown')),
    reasons TEXT[],  -- Array of reasons explaining the halal status
    haram_items_found TEXT[],  -- Array to store any haram items found
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the product_name column
CREATE INDEX IF NOT EXISTS idx_products_product_name ON products (product_name);

-- Create or replace the function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW() AT TIME ZONE 'UTC';
   RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS update_updated_at ON products;

-- Create the trigger to update the updated_at column before each row update
CREATE TRIGGER update_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();