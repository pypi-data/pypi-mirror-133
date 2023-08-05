import requests
import json
import random

class Client:

	"""
	Определение клиента:
	
	client = Client(token, group_id)

	Парамет token является токеном от вашей страницы в ВК,
	получить его можно здесь: https://vkhost.github.io

	Параметр token может содержать в себе как один токен,
	так и список токенов

	Парамет group_id должен содержать в себе сообщество ВК,
	которое будет служить базой данных. Начинатся id сообщество,
	должно со знака -

	ТОКЕНЫ ОТ АККАУНТОВ КОТОРЫЕ ПЕРЕДАЮТСЯ В ПАРАМЕТРЕ token,
	ДОЛЖНЫ БЫТЬ АДМИНИСТРАТОРАМИ В СООБЩЕСТВЕ group_id
	"""

	def __init__(self, tokens: str or list, group_id: int):
		if not isinstance(tokens, list):
			tokens = [tokens]
		self.api = f"https://api.vk.com/method/%method%?access_token={random.choice(tokens)}&v=5.131"
		self.group_id = group_id
		self.max_posts = 50

		response = requests.get(self.api.replace("%method%", "groups.getById"), params={
			"group_ids": f"{self.group_id}".replace("-", "")
		}).json()

		if "error" in response:
			if response["error"]["error_msg"] == "User authorization failed: no access_token passed.":
				print(f"ERROR:teletypeBD: Не зарегистрированный токен в группе: {response['error']['request_params'][0]['value']}")
			print(f"INFO:teletypeBD: Соединение не установлено [https://vk.com/{response['response'][0]['screen_name']}]")
		else:
			print(f"INFO:teletypeBD: Соединение установлено [https://vk.com/{response['response'][0]['screen_name']}]")

	def insert(self, posts: dict or list):
		"""
		Публикует посты, использование:
		
		client.insert({
			"_id": 1,
			"name": "hizri"
		})

		client.insert([
			{"_id": 1, "name": "hizri"},
			{"_id": 2, "name": "ramazan"}
		])

		Параметр _id является обязательным
		"""
		if not isinstance(posts, list):
			posts = [posts]

		for post in posts:
			if self.find({"_id": post['_id']}) != 0:
				raise TypeError(f"id <{post['_id']}> уже записан в базе")

			requests.get(self.api.replace("%method%", "wall.post"), params={
				"owner_id": self.group_id,
				"message": str(post)
			})

	def find(self, posts: dict):
		"""
		Получает один или несколько постов по его _id(ПО _id
		КОТОРОЕ УКАЗАНО В САМОЙ ЗАПИСИ, НО НЕ ПО _id ЗАПИСИ
		НА СТЕНЕ СООБЩЕСТВА), использование:

		print(client.find({"_id": 1}))

		print(client.find({"_id": [1, 2]}))

		>>> Возвращает список полученных записей,
		в случае отсутвия записи, она не будет добавлена в список.

		>>> Если запрашивается одна запись, в случае ее отсутвия,
		вернется значение 0
		"""
		if not isinstance(posts["_id"], list):
			posts["_id"] = [posts["_id"]]

		response = requests.get(self.api.replace("%method%", "wall.get"), params={
			"owner_id": self.group_id
		})

		if len(response.json()["response"]["items"]) > self.max_posts:
			postDelete = random.choice(response.json()["response"]["items"])
			requests.get(self.api.replace("%method%", "wall.delete"), params={
				"owner_id": self.group_id,
				"post_id": postDelete["id"]
			})
			print(f"Запись: {postDelete['text']}\nБыла удалена. Причина: <={self.max_posts}")

		check = []

		for key in response.json()["response"]["items"]:
			keyPost = json.loads(key["text"].replace("'", "\""))

			for post in posts["_id"]:
				if keyPost["_id"] == post:
					check.append(keyPost)
					break

		return check if len(check) >= 1 else 0

	def update(self, posts: dict, update: dict):
		"""
		Обнолвяет одну или несколько постов, _id записи
		определяется по тому же принципу как в методе find

		Сам метод, содержет в себе 2 модификатора,
		$set - изменить значение на отправляемое
		$inc - добавить к имеющимуся числу отправляемое

		Использование:
		client.update({
			"_id": 1,
		}, {
			"$set": {"name": "test"},
			"$inc": {"age": "1"}
		})

		В данном случае если указать больше id в поле _id,
		то у них всех будут изменены поля name и age

		Метод $set также может создать поле в случае его отсутвия
		"""
		if not isinstance(posts["_id"], list):
			posts["_id"] = [posts["_id"]]

		response = requests.get(self.api.replace("%method%", "wall.get"), params={
			"owner_id": self.group_id
		})

		for key in response.json()["response"]["items"]:
			keyPost = json.loads(key["text"].replace("'", "\""))

			for post in posts["_id"]:
				if keyPost["_id"] == post:
					for modificator in update:
						if modificator in ["$set", "$inc"] and len(update[modificator]) == 1:
							for keyModificator in update[modificator]:
								if modificator == "$set":
									keyPost[keyModificator] = update[modificator][keyModificator]
								elif modificator == "$inc":
									keyPost[keyModificator] += update[modificator][keyModificator]
						else:
							raise TypeError(f"Неизвестный модификатор <{modificator}>")

					response = requests.get(self.api.replace("%method%", "wall.edit"), params={
						"owner_id": self.group_id,
						"post_id": key["id"],
						"message": str(keyPost)
					})

	def delete(self, posts: dict or list):
		"""
		Удаляет посты, определение _id по тоту же принципу,
		что в методах find и update. Использование:

		client.delete({"_id": 1})

		client.delete({"_id": [1, 2, 3, 4]})

		Если указать all в _id, то будут удалены все посты
		"""
		if not isinstance(posts["_id"], list):
			posts["_id"] = [posts["_id"]]

		response = requests.get(self.api.replace("%method%", "wall.get"), params={
			"owner_id": self.group_id
		})

		for key in response.json()["response"]["items"]:
			keyPost = json.loads(key["text"].replace("'", "\""))

			if posts["_id"] == ["all"]:
				requests.get(self.api.replace("%method%", "wall.delete"), params={
					"owner_id": self.group_id,
					"post_id": key["id"]
				})
			else:
				for post in posts["_id"]:
					if keyPost["_id"] == post:

						requests.get(self.api.replace("%method%", "wall.delete"), params={
							"owner_id": self.group_id,
							"post_id": key["id"]
						})

	def find_all(self):
		"""
		Получает все посты

		print(client.find_all)

		>>> Возврщает список записей. В случае
		отсутсвия записей, вернется значение 0
		"""

		response = requests.get(self.api.replace("%method%", "wall.get"), params={
			"owner_id": self.group_id
		})

		check = []

		for key in response.json()["response"]["items"]:
			check.append(json.loads(key["text"].replace("'", "\"")))

		check.reverse()

		return check if len(check) >= 1 else 0
