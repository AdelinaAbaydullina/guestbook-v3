import json
import os
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

notes = []
FILE = "notes.json"

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        notes = json.load(f)

def save_notes():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

def find_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return note
    return None


@app.get("/")
def index():
    return "<h1>Гостевая книга</h1>"


@app.get("/notes")
def list_notes():
    result = notes.copy()

    author = request.args.get("author")
    if author is not None:
        result = [n for n in result if n["author"] == author]

    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")

    if sort not in ["id", "likes"]:
        return jsonify(error="Неверная сортировка"), 400

    if order not in ["asc", "desc"]:
        return jsonify(error="Неверный порядок"), 400

    result.sort(key=lambda n: n[sort], reverse=(order == "desc"))

    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify(error="limit и offset должны быть числами"), 400

    if limit < 1 or limit > 100:
        return jsonify(error="limit должен быть от 1 до 100"), 400

    if offset < 0:
        return jsonify(error="offset не может быть отрицательным"), 400

    result = result[offset:offset + limit]

    return jsonify(result)


@app.post("/notes")
def create_note():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Нужен JSON"), 400

    author = data.get("author")
    text = data.get("text")

    if not isinstance(author, str) or not author.strip():
        return jsonify(error="Нужен автор"), 400

    if not isinstance(text, str) or not text.strip():
        return jsonify(error="Нужен текст"), 400

    if notes:
        new_id = max(n["id"] for n in notes) + 1
    else:
        new_id = 1

    note = {
        "id": new_id,
        "author": author.strip(),
        "text": text.strip(),
        "likes": 0
    }

    notes.append(note)
    save_notes()

    return jsonify(note), 201


@app.get("/notes/<int:note_id>")
def get_note(note_id):
    note = find_note(note_id)

    if note is None:
        abort(404)

    return jsonify(note)


@app.put("/notes/<int:note_id>")
def update_note(note_id):
    note = find_note(note_id)

    if note is None:
        abort(404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Нужен JSON"), 400

    author = data.get("author")
    text = data.get("text")

    if not isinstance(author, str) or not author.strip():
        return jsonify(error="Нужен автор"), 400

    if not isinstance(text, str) or not text.strip():
        return jsonify(error="Нужен текст"), 400

    note["author"] = author.strip()
    note["text"] = text.strip()

    save_notes()

    return jsonify(note), 200


@app.patch("/notes/<int:note_id>")
def patch_note(note_id):
    note = find_note(note_id)

    if note is None:
        abort(404)

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Нужен JSON"), 400

    if "text" not in data:
        return jsonify(error="Нужен текст"), 400

    if not isinstance(data["text"], str) or not data["text"].strip():
        return jsonify(error="Текст не должен быть пустым"), 400

    note["text"] = data["text"].strip()

    save_notes()

    return jsonify(note), 200


@app.delete("/notes/<int:note_id>")
def delete_note(note_id):
    note = find_note(note_id)

    if note is None:
        abort(404)

    notes.remove(note)
    save_notes()

    return "", 204

@app.post("/notes/<int:note_id>/like")
def like_note(note_id):
    note = find_note(note_id)

    if note is None:
        abort(404)

    note["likes"] += 1
    save_notes()

    return jsonify(note), 200

@app.get("/authors")
def authors():
    result = {}

    for note in notes:
        author = note["author"]

        if author not in result:
            result[author] = {
                "author": author,
                "notes": 0,
                "likes": 0
            }

        result[author]["notes"] += 1
        result[author]["likes"] += note["likes"]

    answer = list(result.values())
    answer.sort(key=lambda n: n["author"])

    return jsonify(answer)

@app.delete("/notes")
def delete_author_notes():
    author = request.args.get("author")

    if author is None or not author.strip():
        return jsonify(error="Укажите автора"), 400

    global notes

    old_count = len(notes)

    notes = [n for n in notes if n["author"] != author.strip()]

    deleted = old_count - len(notes)

    save_notes()

    return jsonify(deleted=deleted), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Заметка не найдена"), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(error="Метод не разрешен"), 405


if __name__ == "__main__":
    app.run(debug=True)
