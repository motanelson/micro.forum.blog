from flask import Flask, request, redirect
import os

app = Flask(__name__)

# Lista de categorias
lista1 = [
    "off_topic",
    "operation_system",
    "cosmos_os",
    "assembly",
    "programming",
    "hardware"
]


def sanitize(text):
    return text.replace("<", "").replace(">", "")


def get_filename(category):
    return f"{category}.txt"


def load_posts(category):
    posts = []
    filename = get_filename(category)

    if not os.path.exists(filename):
        open(filename, "w").close()

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|||")
            if len(parts) == 2:
                posts.append((parts[0], parts[1]))

    return posts


def save_post(category, url, message):
    filename = get_filename(category)
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{url}|||{message}\n")


# 🏠 Página principal
@app.route("/")
def home():
    html = """
    <html>
    <head>
        <title>Blog Categorias</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial;
                margin: 20px;
            }
            a {
                color: #00ffff;
                text-decoration: none;
                display: block;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <h1>Categorias</h1>
    """

    for cat in lista1:
        html += f'<a href="/{cat}">{cat}</a>'

    html += "</body></html>"
    return html


# 📄 Página de cada categoria
@app.route("/<category>", methods=["GET", "POST"])
def category_page(category):
    if category not in lista1:
        return "Categoria inválida", 404

    if request.method == "POST":
        url = sanitize(request.form.get("url", ""))
        message = sanitize(request.form.get("message", ""))

        if url and message:
            save_post(category, url, message)

        return redirect(f"/{category}")

    posts = load_posts(category)

    html = f"""
    <html>
    <head>
        <title>{category}</title>
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: Arial;
                margin: 20px;
            }}
            textarea, input {{
                width: 100%;
                background: #111;
                color: white;
                border: 1px solid #555;
                padding: 10px;
                margin-top: 5px;
            }}
            button {{
                margin-top: 10px;
                padding: 10px;
                background: #333;
                color: white;
                border: none;
                cursor: pointer;
            }}
            hr {{
                border: 1px solid #444;
            }}
            a {{
                color: #00ffff;
            }}
        </style>
    </head>
    <body>

        <a href="/">⬅ Voltar à página principal</a>

        <h2>{category}</h2>

        <form method="POST">
            <label>Endereço (URL):</label>
            <input type="text" name="url" required>

            <label>Mensagem:</label>
            <textarea name="message" rows="4" required></textarea>

            <button type="submit">Submit</button>
        </form>

        <hr>

        <h2>Mensagens</h2>
    """

    for url, msg in reversed(posts):
        html += f"""
        <div>
            <b>{url}</b><br>
            <p>{msg}</p>
        </div>
        <hr>
        """

    html += "</body></html>"
    return html


if __name__ == "__main__":
    app.run(debug=True)
