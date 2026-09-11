import os
import re
import json
import base64

def main():
    print("=== DECOUPLING BASE64 ASSETS FROM INDEX.HTML ===")
    os.makedirs("images/ui", exist_ok=True)
    os.makedirs("images/products", exist_ok=True)

    # 1. Load product map
    with open("products-data.js", "r", errors="ignore") as f:
        js = f.read()

    m = re.search(r'window\.DIVINE_PRODUCTS\s*=\s*(\[.*?\]);', js, re.DOTALL)
    if not m:
        raise ValueError("Could not parse products-data.js")
    products = json.loads(m.group(1))
    product_map = {p["handle"]: p["images"] for p in products}
    print(f"Loaded {len(product_map)} products from catalog.")

    # 2. Read index.html
    with open("index.html", "r", errors="ignore") as f:
        html = f.read()

    initial_size = len(html)
    print(f"Initial index.html size: {initial_size:,} bytes ({initial_size / (1024*1024):.2f} MB)")

    # 3. Replace card images
    card_pattern = re.compile(r'(<hdt-card-product\b.*?</hdt-card-product>)', re.DOTALL)
    card_chunks = []
    last_end = 0
    cards_processed = 0

    for match in card_pattern.finditer(html):
        card_chunks.append(html[last_end:match.start()])
        card_html = match.group(1)
        last_end = match.end()

        # Find handle
        m_handle = re.search(r'product\.html\?id=([a-zA-Z0-9_-]+)', card_html)
        if not m_handle:
            m_handle = re.search(r'/products/([a-zA-Z0-9_-]+)', card_html)
        
        handle = m_handle.group(1) if m_handle else None
        if handle and handle in product_map:
            imgs = product_map[handle]
            # Replace base64 in card_html
            b64_matches = list(re.finditer(r'src="(data:image/[^;]+;base64,[^"]+)"', card_html))
            new_card = card_html
            # Replace from right to left to preserve offsets
            for i in reversed(range(len(b64_matches))):
                b_match = b64_matches[i]
                replacement_img = imgs[i] if i < len(imgs) else imgs[0]
                new_card = new_card[:b_match.start()] + f'src="{replacement_img}"' + new_card[b_match.end():]
            card_chunks.append(new_card)
            cards_processed += 1
        else:
            print(f"Warning: Could not match product handle in card: {handle}")
            card_chunks.append(card_html)

    card_chunks.append(html[last_end:])
    step1_html = "".join(card_chunks)
    print(f"Processed {cards_processed} product cards.")
    print(f"Intermediate size after cards: {len(step1_html):,} bytes ({len(step1_html)/(1024*1024):.2f} MB)")

    # 4. Replace remaining UI base64 images
    promo_counter = 0
    thumb_counter = 0
    asset_counter = 0

    def replace_ui_b64(m):
        nonlocal promo_counter, thumb_counter, asset_counter
        data_url = m.group(1)
        mime_ext = m.group(2).lower()
        b64_str = m.group(3)
        ext = "jpg" if "jp" in mime_ext else "png"

        # Determine context by looking backward in step1_html
        start_pos = m.start()
        context = step1_html[max(0, start_pos - 120):start_pos]

        if "desk-img" in context:
            filename = "images/ui/banner-desktop.png"
        elif "mobile-img" in context:
            filename = "images/ui/banner-mobile.png"
        elif "hdt-media-wrapper" in context:
            filename = "images/ui/category-banner.png"
        elif "login-img" in context:
            filename = "images/ui/login-banner.png"
        elif "pcj-promo-img" in context:
            promo_counter += 1
            filename = f"images/ui/promo-{promo_counter}.{ext}"
        elif "pcj-thumb" in context:
            thumb_counter += 1
            filename = f"images/ui/thumb-{thumb_counter}.{ext}"
        else:
            asset_counter += 1
            filename = f"images/ui/asset-{asset_counter}.{ext}"

        # Decode and write to disk
        if not os.path.exists(filename):
            try:
                data = base64.b64decode(b64_str)
                with open(filename, "wb") as img_out:
                    img_out.write(data)
                print(f"  Saved UI image: {filename} ({len(data):,} bytes)")
            except Exception as e:
                print(f"  Error decoding {filename}: {e}")

        return f'src="{filename}"'

    final_html = re.sub(r'src="(data:image/([^;]+);base64,([^"]+))"', replace_ui_b64, step1_html)

    # Check remaining base64
    remaining = re.findall(r'data:image/[^;]+;base64,', final_html)
    print(f"Remaining base64 strings in index.html: {len(remaining)}")

    # 5. Save a backup of original index.html just in case
    if not os.path.exists("scratch/index.html.original"):
        os.makedirs("scratch", exist_ok=True)
        print("Backing up original index.html to scratch/index.html.original...")
        with open("scratch/index.html.original", "w", errors="ignore") as f:
            f.write(html)

    # 6. Write final optimized index.html
    with open("index.html", "w", errors="ignore") as f:
        f.write(final_html)

    final_size = len(final_html)
    print(f"\nFinal index.html size: {final_size:,} bytes ({final_size / 1024:.2f} KB)")
    print(f"Reduced size by: {(initial_size - final_size) / (1024*1024):.2f} MB ({((initial_size - final_size) / initial_size) * 100:.1f}%)")
    print("✓ index.html successfully decoupled and optimized!")

if __name__ == "__main__":
    main()
