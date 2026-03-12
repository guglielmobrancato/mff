import os
import urllib.parse

html = """
    <!-- FILM INDUSTRY PARTNERS SECTION -->
    <section class="section dark-bg">
      <div class="container">
        <h2 style="margin-bottom: 2rem;">Film Industry Partners</h2>
        <p style="color: var(--text-secondary); max-width: 800px; margin-bottom: 3rem; font-size: 1.1rem; line-height: 1.6;">
          Realtà di produzione e distribuzione che presenzieranno alla Pitch Session e potranno liberamente opzionare una o più storie in gara.
        </p>

        <div class="partner-grid" style="margin-bottom: 4rem;">
"""

folder = r"assets\partner\producers & distributors"
if os.path.exists(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg'))]
    for f in files:
        encoded_f = urllib.parse.quote(f)
        html += f"""
          <div class="partner-logo" style="background: #fff; display: flex; align-items: center; justify-content: center; height: 150px; padding: 1rem;">
            <img src="assets/partner/producers%20%26%20distributors/{encoded_f}" alt="{f}" style="max-height: 100px; max-width: 90%; filter: none; transition: transform 0.3s; transform: scale(1);">
          </div>
"""

html += """
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
          <a href="film-industry-closed.html" class="cta-button">Partecipa alla Film Industry</a>
        </div>
      </div>
    </section>
"""

with open('partner_block.html', 'w', encoding='utf-8') as file:
    file.write(html)

print("Generated partner_block.html successfully.")
