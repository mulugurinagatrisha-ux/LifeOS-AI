import re


def parse_ai_response(text):

    sections = {
        "Estimated Days": "",
        "Daily Tasks": "",
        "Weekly Target": "",
        "Diet Plan": "",
        "Water Intake": "",
        "Workout Plan": "",
        "Motivation": "",
        "Success Tips": "",
        "Goal Completion Message": ""
    }

    if not text:
        return sections

    current = None

    # Recognize section headings even if they contain ":" or Markdown.
    heading_map = {
        "estimated days": "Estimated Days",
        "daily tasks": "Daily Tasks",
        "weekly target": "Weekly Target",
        "diet plan": "Diet Plan",
        "water intake": "Water Intake",
        "workout plan": "Workout Plan",
        "motivation": "Motivation",
        "success tips": "Success Tips",
        "goal completion message": "Goal Completion Message"
    }

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        cleaned = re.sub(r"^[#*\s]+", "", line)
        cleaned = re.sub(r"[*#\s]+$", "", cleaned)

        heading = re.sub(r":\s*$", "", cleaned).strip().lower()

        if heading in heading_map:
            current = heading_map[heading]
            continue

        if current:
            sections[current] += line + "\n"

    # Extract the number of estimated days from the AI response.
    estimated_text = sections["Estimated Days"]

    match = re.search(r"\b(\d+)\s*(?:days?|weeks?|months?)\b",
                      estimated_text, re.IGNORECASE)

    if match:
        number = int(match.group(1))
        unit = match.group(0).lower()

        if unit.startswith("week"):
            number *= 7
        elif unit.startswith("month"):
            number *= 30

        sections["Estimated Days"] = str(number)

    return {
        key: value.strip()
        for key, value in sections.items()
    }