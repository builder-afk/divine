import os
import re

print("Reading index.html...")
with open("index.html", "r", errors="ignore") as f:
    content = f.read()

# Find all product handles from products-data.js or index.html
with open("products-data.js", "r", errors="ignore") as f_js:
    js_data = f_js.read()
import json
m = re.search(r'window\.DIVINE_PRODUCTS\s*=\s*(\[.*?\]);', js_data, re.DOTALL)
products = json.loads(m.group(1)) if m else []
handles = set(p["handle"] for p in products)
print(f"Found {len(handles)} unique handles.")

# Create directories and index.html files
for h in handles:
    # 1. /products/<handle>/index.html
    dir1 = os.path.join("products", h)
    os.makedirs(dir1, exist_ok=True)
    redirect1 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=../../product.html?id={h}">
  <title>Redirecting to {h}...</title>
  <script>window.location.replace("../../product.html?id={h}");</script>
</head>
<body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
  <p>Opening product details...</p>
  <p><a href="../../product.html?id={h}">Click here if not redirected automatically</a></p>
</body>
</html>
"""
    with open(os.path.join(dir1, "index.html"), "w", encoding="utf-8") as f1:
        f1.write(redirect1)

    # 2. /collections/divine-collection-by-pachchigar-jewellers/products/<handle>/index.html
    dir2 = os.path.join("collections", "divine-collection-by-pachchigar-jewellers", "products", h)
    os.makedirs(dir2, exist_ok=True)
    redirect2 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=../../../../product.html?id={h}">
  <title>Redirecting to {h}...</title>
  <script>window.location.replace("../../../../product.html?id={h}");</script>
</head>
<body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
  <p>Opening product details...</p>
  <p><a href="../../../../product.html?id={h}">Click here if not redirected automatically</a></p>
</body>
</html>
"""
    with open(os.path.join(dir2, "index.html"), "w", encoding="utf-8") as f2:
        f2.write(redirect2)

print("Created static route fallbacks for all handles.")

# Now update index.html so card links point directly to product.html?id=<handle>
# Notice the pattern: href="/collections/divine-collection-by-pachchigar-jewellers/products/XYZ"
old_pattern = r'href="/collections/divine-collection-by-pachchigar-jewellers/products/([a-zA-Z0-9_-]+)"'
matches_before = len(re.findall(old_pattern, content))
print(f"Occurrences to update in index.html: {matches_before}")

new_content = re.sub(old_pattern, r'href="product.html?id=\1"', content)

# Also ensure any card click anywhere on the product card opens the product detail page smoothly
navigation_script = """
<script>
// Smooth card navigation enhancement
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.hdt-card-product').forEach(function(card) {
    card.style.cursor = 'pointer';
    card.addEventListener('click', function(e) {
      // If clicking ATC button or form, don't navigate
      if (e.target.closest('button') || e.target.closest('form') || e.target.closest('input')) {
        return;
      }
      var link = card.querySelector('a[href*="product.html"], a[data-pr-url]');
      if (link && link.getAttribute('href')) {
        window.location.href = link.getAttribute('href');
      }
    });
  });
});
</script>
</body>
"""

if "</body>" in new_content and "Smooth card navigation enhancement" not in new_content:
    new_content = new_content.replace("</body>", navigation_script)

with open("index.html", "w", encoding="utf-8") as f_out:
    f_out.write(new_content)

print("Updated index.html successfully!")
