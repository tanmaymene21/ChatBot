-- First, clear existing data (if needed)
TRUNCATE TABLE products
, suppliers RESTART IDENTITY CASCADE;

-- Insert Suppliers
INSERT INTO suppliers
    (name, email, phone, address, categories_offered)
VALUES
    (
        'TechPro Supplies',
        'contact@techpro.com',
        '555-0101',
        '123 Tech Boulevard, Silicon Valley, CA 94025',
        '["Electronics", "Computers", "Accessories"]'
),
    (
        'Office Solutions Inc',
        'sales@officesolutions.com',
        '555-0102',
        '456 Business Park, Chicago, IL 60601',
        '["Office Supplies", "Furniture", "Electronics"]'
),
    (
        'Global Electronics',
        'info@globalelec.com',
        '555-0103',
        '789 Digital Drive, Austin, TX 78701',
        '["Electronics", "Smart Home", "Gaming"]'
),
    (
        'Eco Gadgets',
        'support@ecogadgets.com',
        '555-0104',
        '321 Green Street, Portland, OR 97201',
        '["Sustainable Tech", "Electronics", "Solar Products"]'
),
    (
        'Smart Home Solutions',
        'hello@smarthome.com',
        '555-0105',
        '654 Innovation Ave, Seattle, WA 98101',
        '["Smart Home", "Security", "Automation"]'
);

-- Insert Products
INSERT INTO products
    (name, brand, price, category, description, supplier_id)
VALUES
    -- TechPro Supplies Products
    (
        'Pro Laptop X1',
        'TechMaster',
        1299.99,
        'Electronics',
        'Professional laptop with 16GB RAM, 512GB SSD, and 4K display',
        1
),
    (
        'Wireless Mouse Pro',
        'TechMaster',
        49.99,
        'Accessories',
        'Ergonomic wireless mouse with 6-month battery life',
        1
),
    (
        'Mechanical Keyboard',
        'TechMaster',
        129.99,
        'Accessories',
        'RGB mechanical keyboard with custom switches',
        1
),

    -- Office Solutions Inc Products
    (
        'Executive Desk',
        'OfficePro',
        599.99,
        'Furniture',
        'Large executive desk with built-in wireless charging',
        2
),
    (
        'LED Desk Lamp',
        'LightMaster',
        79.99,
        'Office Supplies',
        'Adjustable LED desk lamp with color temperature control',
        2
),
    (
        'Ergonomic Chair',
        'ComfortPlus',
        299.99,
        'Furniture',
        'Fully adjustable ergonomic office chair',
        2
),

    -- Global Electronics Products
    (
        'Gaming Monitor',
        'ViewPro',
        449.99,
        'Gaming',
        '27-inch 144Hz gaming monitor with 1ms response time',
        3
),
    (
        'Smart TV',
        'ViewPro',
        899.99,
        'Electronics',
        '55-inch 4K Smart TV with HDR',
        3
),
    (
        'Gaming Console Pro',
        'GameMaster',
        499.99,
        'Gaming',
        'Next-gen gaming console with 1TB storage',
        3
),

    -- Eco Gadgets Products
    (
        'Solar Power Bank',
        'EcoPower',
        79.99,
        'Sustainable Tech',
        '20000mAh solar-powered power bank',
        4
),
    (
        'Smart LED Bulbs',
        'EcoLight',
        29.99,
        'Smart Home',
        'Energy-efficient smart LED bulbs with app control',
        4
),
    (
        'Recycled Laptop Stand',
        'EcoWork',
        49.99,
        'Sustainable Tech',
        'Laptop stand made from recycled materials',
        4
),

    -- Smart Home Solutions Products
    (
        'Smart Security Camera',
        'SecureHome',
        199.99,
        'Security',
        'HD wireless security camera with night vision',
        5
),
    (
        'Smart Thermostat',
        'ClimateControl',
        159.99,
        'Smart Home',
        'AI-powered smart thermostat with energy saving features',
        5
),
    (
        'Smart Door Lock',
        'SecureHome',
        249.99,
        'Security',
        'Fingerprint and PIN enabled smart door lock',
        5
);

-- Add some budget-friendly options
INSERT INTO products
    (name, brand, price, category, description, supplier_id)
VALUES
    (
        'Basic Mouse',
        'TechMaster',
        19.99,
        'Accessories',
        'Simple and reliable USB mouse',
        1
),
    (
        'Desktop Speakers',
        'AudioPro',
        39.99,
        'Electronics',
        'Compact USB powered desktop speakers',
        3
),
    (
        'USB Hub',
        'TechMaster',
        24.99,
        'Accessories',
        '4-port USB 3.0 hub',
        1
); 