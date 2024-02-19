from fastapi_tools.mongo import Document


class User(Document):
    email: str
    name: str
    auth0_id: str
