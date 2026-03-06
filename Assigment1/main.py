from fastapi import FastAPI,Query
 
app = FastAPI()
 
# ── Temporary data ───────────────────────────────────────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price': 99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price': 49, 'category': 'Stationery',  'in_stock': True },

    #  Q1 : Add 3 Products 
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True}, 
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {
        'products': products,
        'total': len(products) 
        }

# ── Endpoint 2 — Return all products with filters ──────────────────────────
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}
    

# Q2 --------> Endpoint 3 — Return products by category wise ──────────────────
@app.get('/products/category/{category_name}')
def get_products_by_category(category_name: str):
    category_products = [p for p in products if p['category'].lower() == category_name.lower()]
    if not category_products: return {"error": "No products found in this category"}   
    return {'products': category_products, 'count': len(category_products)}
 
# Q3 :-------> Endpoint 4 — Return products available instock ────────────────── 
@app.get('/products/instock')
def get_in_stock_products():
    in_stock_products=[p for p in products if p['in_stock'] == True]
    return {'products': in_stock_products, 'count': len(in_stock_products)}

# Q4 :-------> Endpoint 5 — Return store summary like Name , Total Products , instock and others  ──────────────────
@app.get('/store/summary')
def store_summary():
    name= "My E-commerce Store"
    total_products = len(products)
    in_stock_products = len([p for p in products if p['in_stock']])
    out_of_stock_products = total_products - in_stock_products
    return {
        'store_name': name,
        'total_products': total_products,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'categories': list(set(p['category'] for p in products))
    }

# Q5 :-------> Endpoint 6 — Return products by searching  ──────────────────
@app.get('/products/search/{keyword}')
def search_products(keyword: str):
    keyword_lower = keyword.lower()
    matching_products = [p for p in products if keyword_lower in p['name'].lower()]
    if not matching_products:
        return {"message": "No products matched your search"}
    return {'products': matching_products, 'count': len(matching_products)  }

# Q6 :-------> Endpoint 7 — Return the Best deal to users ──────────────────
@app.get("/products/deals") 
def get_deals():
    cheapest = min(products, key=lambda p: p["price"]) 
    expensive = max(products, key=lambda p: p["price"]) 
    return { "best_deal": cheapest, "premium_pick": expensive, }

# ── Endpoint 8 — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}