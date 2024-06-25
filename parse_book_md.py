import json
import re


def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content by each section
    sections = re.split(r'##\s+\d+\.\s+', content)[1:]

    parsed_data = []

    for section in sections:
        title_match = re.search(r'(.+)', section)
        title = title_match.group(1).strip() if title_match else ''

        desc_match = re.search(
            r'\*\*释义\*\*\s*(.*?)\s*\*\*例句\*\*', section, re.DOTALL)
        desc = desc_match.group(1).strip() if desc_match else ''

        examples = []
        example_matches = re.findall(
            r'- <span lang="en">(.*?)</span>\s*<span lang="cn">(.*?)</span><audio controls><source src="(.*?)" type="audio/mpeg"></audio>',
            section,
            re.DOTALL
        )

        for en, cn, audio in example_matches:
            examples.append({
                # Remove any remaining HTML tags
                'en': re.sub(r'<.*?>', '', en).strip(),
                # Remove any remaining HTML tags
                'cn': re.sub(r'<.*?>', '', cn).strip(),
                'audio_link': audio.strip()
            })

        parsed_data.append({
            'name': title,
            'desc': desc,
            'examples': examples
        })

    return parsed_data


# Example usage
file_path = 'book.md'
parsed_data = parse_markdown(file_path)

# Convert the parsed data to JSON string
data_json = json.dumps(parsed_data, ensure_ascii=False, indent=2)

# Create the JavaScript file content
js_content = f"const books = {data_json};"

# Write the JavaScript file
js_file_path = 'book.js'
with open(js_file_path, 'w+', encoding='utf-8') as js_file:
    js_file.write(js_content)

print(f'JavaScript file created at {js_file_path}')
