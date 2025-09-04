import google.generativeai as genai
import json
import re
import json
import folium

prompt = (
    "List the 100 most popular surf breaks in Australia. "
    "For each surf break, provide the following details in a JSON array: "
    "1. name, 2. state_or_territory, 3. nearest_town_or_city, 4. type_of_break (e.g., beach, point, reef), "
    "5. coordinates (latitude and longitude as decimal numbers). "
    "Return only valid JSON, no extra text or formatting."
)

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)

def extract_json(text):
    # Remove markdown code block markers if present
    cleaned = re.sub(r"^```json|^```|```$", "", text.strip(), flags=re.MULTILINE)
    # Try to find the first JSON array in the text
    match = re.search(r"(\[\s*{.*}\s*\])", cleaned, re.DOTALL)
    if match:
        return match.group(1)
    return cleaned

def save_json_to_file(json_str, filename):
    try:
        data = json.loads(json_str)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} surf breaks to {filename}")
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        print("Raw response was:\n", json_str[:500])

json_str = extract_json(response.text)
save_json_to_file(json_str, "data/australian_surf_breaks.json")

# Load surf breaks data
with open("data/australian_surf_breaks.json", "r") as f:
    surf_breaks = json.load(f)

# Center map on Australia
australia_center = [-25.0, 134.0]
m = folium.Map(location=australia_center, zoom_start=4)

# Add markers for each surf break
for break_ in surf_breaks:
    coords = break_["coordinates"]
    name = break_["name"]
    state = break_["state_or_territory"]
    nearest = break_["nearest_town_or_city"]
    type_ = break_["type_of_break"]
    popup = f"<b>{name}</b><br>{type_.title()}<br>{nearest}, {state}"
    folium.Marker(
        location=[coords["latitude"], coords["longitude"]],
        popup=popup,
        icon=folium.Icon(color="blue", icon="cloud")
    ).add_to(m)

# Save map to HTML file
m.save("data/australian_surf_breaks_map.html")
print("Map saved as australian_surf_breaks_map.html")