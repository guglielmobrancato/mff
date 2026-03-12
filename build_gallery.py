import os

files = os.listdir('assets/locandine 2026')
files = [f for f in files if f.endswith(('.jpg', '.webp'))]

html = "<html><body style='background: #fff;'>"
html += "<h1>Locandine 2026 Gallery</h1>"
for f in files:
    html += f"<div style='display:inline-block; margin: 10px; border: 1px solid black; padding: 5px; text-align: center;'>"
    html += f"<img src='assets/locandine 2026/{f}' height='300'><br>"
    html += f"<b>{f}</b></div>\n"
html += "</body></html>"

with open('locandine_gallery.html', 'w', encoding='utf-8') as file:
    file.write(html)
print("Gallery created successfully.")
