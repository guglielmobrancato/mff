import json
import re

with open('temp_excel.json', 'r', encoding='utf-8') as f:
    films = json.load(f)

with open('mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Normalize string for fuzzy matching
def normalize(s):
    if not isinstance(s, str):
        return ""
    # lower case, remove punctuation except spaces, strip
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)
    return s.strip()

# Build inverse mapping: normalized title -> filename
inv_map = {normalize(title): filename for filename, title in mapping.items()}

# Special cases or mismatches handled by close match
# For example ALQUIMIA -> Bones, Alquemy and Ether! or IL SETTICIDA -> INSETTICIDA
for filename, title in mapping.items():
    norm_t = normalize(title)
    if norm_t == "il setticida":
        inv_map[normalize("INSETTICIDA")] = filename
    elif norm_t == "alquimia":
        inv_map[normalize("Bones, Alquemy and Ether!")] = filename
    elif norm_t == "cento":
        inv_map[normalize("Cento - Assalto al moro")] = filename

# Hardcode the two re-uploaded posters
inv_map[normalize("A Seperation")] = "a separeation.jpg"
inv_map[normalize("Il Vollo della Falena")] = "il volo della falena.jpg"

html = """<!doctype html>
<html lang="it">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Film in Concorso - Marte Film Festival</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@400;700;900&display=swap"
    rel="stylesheet">
  <link rel="stylesheet" href="./style.css">
  <style>
    .film-hero {
      height: 50vh;
      background-image: url('assets/banner%20sito%20statue.png');
      background-size: cover;
      background-position: center;
      position: relative;
    }

    .film-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 2.5rem;
      margin-top: 3rem;
    }

    .film-card {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      overflow: hidden;
      transition: all 0.3s;
      display: flex;
      flex-direction: column;
    }

    .film-card:hover {
      border-color: var(--accent-color);
      transform: translateY(-5px);
      box-shadow: 0 10px 30px rgba(192, 83, 44, 0.2);
    }

    .film-poster {
      width: 100%;
      aspect-ratio: 2/3;
      background-color: #111;
      background-size: cover;
      background-position: center;
      position: relative;
    }
    
    .film-category-badge {
      position: absolute;
      top: 15px;
      right: 15px;
      background: var(--accent-color);
      color: #fff;
      padding: 0.3rem 0.8rem;
      border-radius: 20px;
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .film-info {
      padding: 1.5rem;
      flex-grow: 1;
      display: flex;
      flex-direction: column;
    }

    .film-title {
      font-family: var(--font-heading);
      font-size: 1.5rem;
      color: #fff;
      margin-bottom: 0.5rem;
    }

    .film-director {
      color: var(--accent-color);
      font-size: 0.9rem;
      margin-bottom: 1rem;
      font-weight: 600;
      text-transform: uppercase;
    }

    .film-logline {
      color: var(--text-secondary);
      font-size: 0.85rem;
      line-height: 1.6;
      margin-bottom: 1.5rem;
      flex-grow: 1;
    }

    .film-meta {
      display: flex;
      justify-content: space-between;
      border-top: 1px solid rgba(255,255,255,0.05);
      padding-top: 1rem;
      font-size: 0.8rem;
      color: rgba(255,255,255,0.5);
    }
  </style>
</head>

<body>
  <nav class="navbar">
    <div class="logo-container">
      <span style="font-family: 'Outfit'; font-weight: 900; color: var(--accent-color); font-size: 1.5rem;">MFF</span>
    </div>
    <ul class="nav-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="next.html">Next</a></li>
      <li><a href="legends.html">Last Editions</a></li>
      <li><a href="partner.html">Partner</a></li>
      <li><a href="chi-siamo.html">Who We Are</a></li>
    </ul>
    <div class="burger">
      <div class="line1"></div>
      <div class="line2"></div>
      <div class="line3"></div>
    </div>
  </nav>

  <section class="film-hero">
    <div class="hero-overlay"></div>
    <div class="hero-content">
      <h1>Film In Concorso</h1>
      <p>La selezione ufficiale della II Edizione.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="film-grid">
"""

def generate_card(film):
    title = film.get('TITOLO', '')
    norm_t = normalize(title)
    poster_filename = inv_map.get(norm_t)
    
    # Fallback partial matching if exact match not found
    if not poster_filename:
        for mapped_title_norm, fn in inv_map.items():
            if norm_t in mapped_title_norm or mapped_title_norm in norm_t:
                poster_filename = fn
                break
                
    poster_style = f"background-image: url('assets/locandine%202026/{poster_filename}');" if poster_filename else "background-image: url('assets/logo%20mff%20arancione.png'); background-size: contain; background-repeat: no-repeat;"
    
    director = film.get('AUTORE', '')
    category = film.get('CATEGORIA', 'IN CONCORSO')
    logline = film.get('LOGLINE', '')
    if logline == '?????':
        logline = ''
    durata = film.get('DURATA ', '')
    
    meta_html = f'''
            <div class="film-meta">
              <span>{durata}</span>
            </div>''' if durata else ""

    return f"""
        <div class="film-card">
          <div class="film-poster" style="{poster_style}">
             <div class="film-category-badge">{category}</div>
          </div>
          <div class="film-info">
            <h3 class="film-title">{title}</h3>
            <div class="film-director">{director}</div>
            <p class="film-logline">{logline}</p>{meta_html}
          </div>
        </div>
"""

for film in films:
    html += generate_card(film)

html += """
      </div>
    </div>
  </section>

  <footer>
    <div class="container">
      <p>&copy; 2026 Marte Studios. All Systems Nominal.</p>
    </div>
  </footer>

  <script type="module" src="./main.js"></script>
</body>
</html>
"""

with open('film-in-concorso.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("film-in-concorso.html created successfully.")
