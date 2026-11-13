import requests

url = "http://127.0.0.1:5000/notes"


def show(r):
    print("Код:", r.status_code)
    try:
        print("Ответ:", r.json())
    except ValueError:
        print("Ответ:", r.text)
    print("-" * 40)


print("СОЗДАНИЕ ЗАМЕТОК")

r1 = requests.post(url, json={
    "author": "Ivan",
    "text": "Привет!"
})
show(r1)
id1 = r1.json()["id"]

r2 = requests.post(url, json={
    "author": "Anna",
    "text": "Хороший день!"
})
show(r2)
id2 = r2.json()["id"]

r3 = requests.post(url, json={
    "author": "Ivan",
    "text": "Моя вторая заметка"
})
show(r3)
id3 = r3.json()["id"]

show(requests.post(url, json={"text": "Без автора"}))
show(requests.post(url, json={
    "author": "Ivan",
    "text": ""
}))
show(requests.post(url, data={"text": "Не JSON"}))

print("ВСЕ ЗАМЕТКИ")
show(requests.get(url))

print("ОДНА ЗАМЕТКА")
show(requests.get(f"{url}/{id1}"))
show(requests.get(f"{url}/99999"))

print("PUT")
show(requests.put(f"{url}/{id1}", json={
    "author": "Petr",
    "text": "Обновленная заметка"
}))

show(requests.put(f"{url}/{id1}", json={
    "text": "Нет автора"
}))

print("PATCH")
show(requests.patch(f"{url}/{id2}", json={
    "text": "Изменен только текст"
}))

show(requests.patch(f"{url}/{id2}", json={
    "text": ""
}))

print("ЛАЙКИ")
show(requests.post(f"{url}/{id1}/like"))
show(requests.post(f"{url}/{id1}/like"))
show(requests.post(f"{url}/{id2}/like"))

show(requests.post(f"{url}/99999/like"))

print("ФИЛЬТР ПО АВТОРУ")
show(requests.get(url, params={"author": "Ivan"}))

print("ПАГИНАЦИЯ")
show(requests.get(url, params={
    "limit": 2,
    "offset": 0
}))

show(requests.get(url, params={
    "limit": 2,
    "offset": 1
}))

show(requests.get(url, params={"limit": 200}))
show(requests.get(url, params={"offset": -1}))
show(requests.get(url, params={"limit": "abc"}))

print("СОРТИРОВКА")
show(requests.get(url, params={
    "sort": "id",
    "order": "desc"
}))

show(requests.get(url, params={
    "sort": "likes",
    "order": "desc"
}))

show(requests.get(url, params={"sort": "abc"}))
show(requests.get(url, params={"order": "abc"}))

print("СТАТИСТИКА АВТОРОВ")
show(requests.get("http://127.0.0.1:5000/authors"))

print("УДАЛЕНИЕ ОДНОЙ ЗАМЕТКИ")
show(requests.delete(f"{url}/{id3}"))

show(requests.delete(f"{url}/{id3}"))

print("МАССОВОЕ УДАЛЕНИЕ")
show(requests.delete(url, params={"author": "Ivan"}))

show(requests.delete(url, params={"author": "Unknown"}))

show(requests.delete(url))

print("ОСТАВШИЕСЯ ЗАМЕТКИ")
show(requests.get(url))

print("ИТОГОВАЯ СТАТИСТИКА")
show(requests.get("http://127.0.0.1:5000/authors"))
