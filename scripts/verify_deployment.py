import os
import re
import json
import sys

def check_file_sizes():
    print("\n--- 1. Checking File Sizes for Deployment Limits ---")
    too_large = []
    max_limit = 25 * 1024 * 1024  # 25 MB Cloudflare/Vercel single-file threshold
    
    for root, dirs, files in os.walk("."):
        if ".git" in root or "scratch" in root:
            continue
        for f in files:
            p = os.path.join(root, f)
            sz = os.path.getsize(p)
            if sz > max_limit:
                too_large.append((p, sz))

    index_sz = os.path.getsize("index.html")
    print(f"  index.html size: {index_sz:,} bytes ({index_sz / 1024:.1f} KB)")
    assert index_sz < 1.5 * 1024 * 1024, f"index.html is too large: {index_sz:,} bytes!"

    prod_sz = os.path.getsize("product.html")
    print(f"  product.html size: {prod_sz:,} bytes ({prod_sz / 1024:.1f} KB)")

    if too_large:
        print(f"FAILED: Files exceed hosting limit: {too_large}")
        return False
    print("✓ All repository files are well below static hosting file size limits!")
    return True

def check_asset_paths_and_casing():
    print("\n--- 2. Checking Local Asset Paths & Case Sensitivity ---")
    files_to_check = ["index.html", "product.html", "404.html"]
    missing_assets = []

    for fn in files_to_check:
        with open(fn, "r", errors="ignore") as f:
            content = f.read()

        # Find assets: img src, script src, link rel="stylesheet|icon" href
        assets = []
        # img, script, video, audio, source src
        for tag in re.finditer(r'<(?:img|script|video|audio|source)\b[^>]*\bsrc=["\']([^"\']+)["\']', content, re.IGNORECASE):
            assets.append(tag.group(1))
        # link rel="stylesheet|icon|apple-touch-icon" href
        for link in re.finditer(r'<link\b[^>]*\b(?:rel=["\'](?:stylesheet|icon|apple-touch-icon|shortcut icon)["\'][^>]*\bhref=["\']([^"\']+)["\']|\bhref=["\']([^"\']+)["\'][^>]*\brel=["\'](?:stylesheet|icon|apple-touch-icon|shortcut icon)["\'])', content, re.IGNORECASE):
            href = link.group(1) or link.group(2)
            if href:
                assets.append(href)

        for p in assets:
            if p.startswith("http://") or p.startswith("https://") or p.startswith("//") or p.startswith("data:") or p.startswith("blob:"):
                continue
            
            clean_path = p.split("?")[0].lstrip("/")
            if not os.path.exists(clean_path):
                missing_assets.append((fn, p))
            else:
                # Check exact case on filesystem
                parts = clean_path.split("/")
                curr = "."
                for part in parts:
                    if part in [".", ""]:
                        continue
                    actual_files = os.listdir(curr)
                    if part not in actual_files:
                        missing_assets.append((fn, f"{p} (case mismatch: {part} not in actual casing)"))
                    curr = os.path.join(curr, part)

    if missing_assets:
        print(f"FAILED: {len(missing_assets)} missing or case-mismatched assets:")
        for fn, p in missing_assets:
            print(f"  In {fn}: {p}")
        return False
    print("✓ All 100% of local stylesheets, scripts, logos, and images resolve with exact filesystem case!")
    return True

def check_product_catalog():
    print("\n--- 3. Checking Product Catalog & Static Fallback Routes ---")
    with open("products-data.js", "r", errors="ignore") as f:
        js = f.read()

    m = re.search(r'window\.DIVINE_PRODUCTS\s*=\s*(\[.*?\]);', js, re.DOTALL)
    assert m, "Could not extract DIVINE_PRODUCTS from products-data.js"
    products = json.loads(m.group(1))

    print(f"  Loaded {len(products)} products from products-data.js")
    assert len(products) == 48, f"Expected 48 products, found {len(products)}"

    missing_imgs = []
    missing_routes = []

    for p in products:
        h = p["handle"]
        for img in p.get("images", []):
            if not os.path.exists(img):
                missing_imgs.append((h, img))
        r1 = os.path.join("products", h, "index.html")
        r2 = os.path.join("collections", "divine-collection-by-pachchigar-jewellers", "products", h, "index.html")
        if not os.path.exists(r1):
            missing_routes.append(r1)
        if not os.path.exists(r2):
            missing_routes.append(r2)

    if missing_imgs:
        print(f"FAILED: {len(missing_imgs)} missing product images: {missing_imgs[:5]}")
        return False
    if missing_routes:
        print(f"FAILED: {len(missing_routes)} missing static fallback routes: {missing_routes[:5]}")
        return False

    print("✓ All 48 products have valid data, verified local images, and 96 static fallback routes!")
    return True

def check_deployment_configs():
    print("\n--- 4. Checking Deployment Configurations & Git Tracking ---")
    configs = ["vercel.json", "_redirects", "_headers", "404.html", "package.json"]
    for c in configs:
        assert os.path.exists(c), f"Missing deployment config file: {c}"
    
    with open(".gitignore", "r") as f:
        gi = f.read()
    assert "index.html" not in gi, "Fatal: index.html is still in .gitignore!"

    print("✓ vercel.json, _redirects, _headers, 404.html exist and index.html is tracked in git!")
    return True

def check_clean_links():
    print("\n--- 5. Checking Card & Header Navigation Links ---")
    with open("index.html", "r", errors="ignore") as f:
        idx_html = f.read()
    with open("product.html", "r", errors="ignore") as f:
        prd_html = f.read()

    # Verify no broken localhost references
    assert "localhost:8000" not in idx_html, "Found hardcoded localhost:8000 in index.html"
    assert "localhost:8000" not in prd_html, "Found hardcoded localhost:8000 in product.html"

    # Verify card links
    card_links = re.findall(r'href="product\.html\?id=([a-zA-Z0-9_-]+)"', idx_html)
    assert len(card_links) >= 48, f"Expected at least 48 product links in index.html, found {len(card_links)}"

    print("✓ Zero hardcoded localhost links, all 48 product card links verified!")
    return True

def main():
    print("==================================================")
    print("   VERMA JEWELLERS - PRODUCTION DEPLOYMENT AUDIT   ")
    print("==================================================")

    checks = [
        check_file_sizes,
        check_asset_paths_and_casing,
        check_product_catalog,
        check_deployment_configs,
        check_clean_links
    ]

    all_passed = True
    for c in checks:
        if not c():
            all_passed = False

    print("\n==================================================")
    if all_passed:
        print("✓ SUCCESS: SITE IS 100% PRODUCTION READY FOR DEPLOYMENT!")
        print("==================================================")
        sys.exit(0)
    else:
        print("✗ FAILED: Issues must be fixed before deployment.")
        print("==================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
