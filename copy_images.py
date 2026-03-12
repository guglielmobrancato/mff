import os
import glob
import shutil

os.makedirs('assets/merch', exist_ok=True)
brain_dir = r"C:\Users\gbran\.gemini\antigravity\brain\2e33e1fe-f559-44ba-a9b1-c004b0dafcb3"

images = glob.glob(os.path.join(brain_dir, "*.png"))
for img in images:
    filename = os.path.basename(img)
    if "tshirt" in filename or "poster" in filename or "totebag" in filename:
        clean_name = filename.rsplit("_", 1)[0] + ".png"
        shutil.copy(img, f"assets/merch/{clean_name}")
        print(f"Copied {filename} to {clean_name}")
