from flask import Flask, render_template_string, send_from_directory
import os

app = Flask(__name__)

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directory Listing</title>
</head>
<body>
    <h1>Directory Listing</h1>
    <ul>
        {% for item in items %}
            <li><a href="{{ url_for('serve_item', path=item['path']) }}">{{ item['name'] }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def directory_listing():
    directory_path = os.path.abspath('.')  # Current directory
    items = [{'name': item, 'path': item} for item in os.listdir(directory_path)]
    return render_template_string(html_template, items=items)

@app.route('/<path:path>')
def serve_item(path):
    full_path = os.path.join(os.path.abspath('.'), path)
    if os.path.isfile(full_path):
        return send_from_directory(os.path.abspath('.'), path)
    elif os.path.isdir(full_path):
        items = [{'name': item, 'path': os.path.join(path, item)} for item in os.listdir(full_path)]
        return render_template_string(html_template, items=items)
    else:
        return 'Not Found', 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)