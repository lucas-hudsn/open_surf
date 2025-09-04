import google.generativeai as genai
import json

model = genai.GenerativeModel("gemini-2.5-flash")

def generarte_description(_break, state):
    prompt = (
        "You are an expert surf guide and forecaster."
        f"Provide a detailed description of the {_break} surf break in {state}, Australia. "
        "Include the following information:\n"
        "- Which wind directions are best for surfing?\n"
        "- What swell size is ideal for optimal conditions?\n"
        "- What tide works best at this break?\n"
        "- What is the recommended experience level for surfers at Bells Beach?\n"
        "Format your answer in clear, short sentences."
        """Example format:Bells Beach is a world-renowned right-hand point break in Victoria, Australia. It is famous for its powerful, long-peeling waves that break over a reef and rock bottom. The main wave, "The Bowl," offers incredible sections.
        **Best Wind Directions:**
        North to Northwest winds are ideal for surfing Bells Beach. These winds are offshore and create clean, groomed wave faces. Light North-Northeast winds can also be favorable.
        **Ideal Swell Size:**
        Bells Beach requires a solid swell to perform optimally. Ideal conditions are typically found with a strong groundswell producing 4–8 feet (face height) waves. It can handle much larger surf, but this range provides the most rideable and powerful waves. It needs at least 3 feet of swell to truly come alive.
        **Best Tide:**
        Mid to high tide generally works best at Bells Beach. This tide range offers a fuller wave, making for longer and more consistent rides. High tide can also be excellent, providing powerful, unbroken walls. Low tide can make sections hollower but also more critical and sometimes sectiony.
        **Recommended Experience Level:**
        Bells Beach is recommended for experienced surfers only. Intermediate to advanced skill levels are required. Surfers need strong paddling power, confidence in powerful waves, and a good understanding of ocean conditions and surf etiquette. It is not suitable for beginners or novice surfers."""
    )
    return prompt

with open("data/australian_surf_breaks.json", "r") as f:
    surf_breaks = json.load(f)

for break_ in surf_breaks:
    name = break_["name"]
    state = break_["state_or_territory"]
    prompt = generarte_description(name, state)
    response = model.generate_content(prompt)
    description = response.text.strip()
    break_["description"] = description
    print(f"Generated description for {name}, {state}")

with open("data/australian_surf_breaks.json", "w") as f:
    json.dump(surf_breaks, f, indent=2)

