import re

# Read the extracted footer html
with open("scratch/homepage_footer.html", "r", encoding="utf-8") as f:
    footer_html = f.read()

print("Footer HTML lines:", len(footer_html.splitlines()))

# Read product.html
with open("product.html", "r", encoding="utf-8") as f:
    prod_html = f.read()

# In product.html, find where footer starts or should be placed
# We currently have <footer class="vj-footer"> ... </footer> or minimal tabs
# Let's inspect where the footer is in product.html
p_footer_start = prod_html.find('<footer')
p_footer_end = prod_html.find('</footer>')

print("product.html current footer found:", p_footer_start != -1)

# Extract CSS from styles.css
with open("styles.css", "r", errors="ignore") as f:
    styles_css = f.read()

# Extract from line 1275 to 1845 in styles.css
styles_lines = styles_css.splitlines()
footer_css_lines = styles_lines[1275:1845]
footer_css = "\n".join(footer_css_lines)
print("Extracted footer CSS lines:", len(footer_css_lines))

with open("scratch/footer_extracted.css", "w", encoding="utf-8") as f_out:
    f_out.write(footer_css)
print("Saved footer CSS to scratch/footer_extracted.css")
