import re

with open("index.html", "r", errors="ignore") as f:
    text = f.read()

start_marker = "<!-- BEGIN sections: footer-group -->"
end_marker = "<!-- END sections: footer-group -->"

p1 = text.find(start_marker)
p2 = text.find(end_marker)

if p1 != -1 and p2 != -1:
    footer_html = text[p1:p2 + len(end_marker)]
    print(f"Found footer html! Length: {len(footer_html)}")
    with open("scratch/homepage_footer.html", "w", encoding="utf-8") as f_out:
        f_out.write(footer_html)
    print("Saved to scratch/homepage_footer.html")
else:
    print("Could not locate markers:", p1, p2)
