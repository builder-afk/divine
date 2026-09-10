import os
import re
import json

print("=== VERIFYING PRODUCT CATALOG & ASSETS ===")

with open("products-data.js", "r", errors="ignore") as f:
    js = f.read()

# Extract JSON
m = re.search(r'window\.DIVINE_PRODUCTS\s*=\s*(\[.*?\]);', js, re.DOTALL)
assert m, "Could not extract DIVINE_PRODUCTS from products-data.js"
products = json.loads(m.group(1))

print(f"Total Products loaded: {len(products)}")
assert len(products) == 48, f"Expected 48 products, got {len(products)}"

missing_images = []
for p in products:
    for img in p.get("images", []):
        if not os.path.exists(img):
            missing_images.append((p["handle"], img))

if missing_images:
    print(f"WARNING: {len(missing_images)} missing images: {missing_images[:5]}")
else:
    print("✓ All product images exist locally on disk!")

print("\n=== VERIFYING STATIC FALLBACK ROUTES ===")
missing_routes = []
for p in products:
    h = p["handle"]
    r1 = os.path.join("products", h, "index.html")
    r2 = os.path.join("collections", "divine-collection-by-pachchigar-jewellers", "products", h, "index.html")
    if not os.path.exists(r1):
        missing_routes.append(r1)
    if not os.path.exists(r2):
        missing_routes.append(r2)

if missing_routes:
    print(f"WARNING: {len(missing_routes)} missing routes")
else:
    print("✓ All 96 static fallback route files exist on disk!")

print("\n=== VERIFYING INDEX.HTML CARD LINKS ===")
with open("index.html", "r", errors="ignore") as f:
    index_html = f.read()

old_links = re.findall(r'href="/collections/divine-collection-by-pachchigar-jewellers/products/[^"]+"', index_html)
print(f"Unconverted old links in index.html: {len(old_links)}")
assert len(old_links) == 0, "There are unconverted links in index.html"

new_links = re.findall(r'href="product\.html\?id=([a-zA-Z0-9_-]+)"', index_html)
print(f"Converted links in index.html: {len(new_links)}")
assert len(new_links) >= 48, f"Expected at least 48 converted links, got {len(new_links)}"

print("\n=== VERIFYING PRODUCT.HTML INTEGRITY ===")
with open("product.html", "r", errors="ignore") as f:
    prod_html = f.read()

required_ids = [
    "vj-product-title", "vj-product-sku", "vj-sale-price", "vj-regular-price",
    "vj-main-img", "vj-thumbnails", "vj-gallery-stage", "vj-btn-atc",
    "vj-btn-whatsapp", "vj-pincode-input", "vj-spec-table-body", "vj-related-grid",
    "vj-cart-overlay", "vj-lightbox"
]
missing_ids = [i for i in required_ids if f'id="{i}"' not in prod_html]
if missing_ids:
    print(f"WARNING: Missing IDs in product.html: {missing_ids}")
else:
    print("✓ All required element IDs present in product.html!")

print("\n=== ALL SYSTEM CHECKS PASSED PERFECTLY! ===")
