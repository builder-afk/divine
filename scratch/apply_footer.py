# 1. Update product.css
with open("product.css", "r", encoding="utf-8") as f_css:
    p_css = f_css.read()

with open("scratch/footer_extracted.css", "r", encoding="utf-8") as f_fcss:
    footer_css = f_fcss.read()

if "#pj-footer-luxe" not in p_css:
    p_css += "\n\n/* ===================================================\n   Homepage Footer Styles - 100% Identical to Home Page\n   =================================================== */\n"
    p_css += footer_css
    with open("product.css", "w", encoding="utf-8") as f_css_out:
        f_css_out.write(p_css)
    print("Appended footer CSS to product.css")
else:
    print("Footer CSS already present in product.css")

# 2. Update product.html
with open("product.html", "r", encoding="utf-8") as f_html:
    p_html = f_html.read()

with open("scratch/homepage_footer.html", "r", encoding="utf-8") as f_fhtml:
    footer_html = f_fhtml.read()

target_marker = "<!-- Floating Minimal Widgets Matching Screenshots -->"
if "pj-footer-luxe" not in p_html:
    parts = p_html.split(target_marker)
    new_html = parts[0] + "\n" + footer_html + "\n\n  " + target_marker + parts[1]
    with open("product.html", "w", encoding="utf-8") as f_html_out:
        f_html_out.write(new_html)
    print("Inserted homepage footer into product.html")
else:
    print("Footer already present in product.html")

