import json

class dbJson:
    def __init__(self):
        self.filename = "db.json"
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def add_data(self, body, title,date):
        new_entry = {
            "id": len(self.data) + 1,
            "title": title,
            "body": body,
            "date":date
        }
        self.data.append(new_entry)
        self.save_data()

    def data_for_id(self, id):
        return next((item for item in self.data if item["id"] == id), None)

    def update_data(self, id, body=None, title=None):
        article = self.data_for_id(id)
        if article:
            if body:
                article["body"] = body
            if title:
                article["title"] = title
            self.save_data()

    def delete(self, id):
        self.data = [item for item in self.data if item["id"] != id]
        self.save_data()

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)
