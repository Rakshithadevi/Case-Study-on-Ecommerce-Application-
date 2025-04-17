from typing import Optional

class Admin:
    def __init__(self, admin_id: Optional[int] = None, name: str = None, password: str = None):
        self.admin_id = admin_id
        self.name = name
        self.password = password


    # Getters and Setters
    def get_admin_id(self):
        return self.admin_id

    def set_admin_id(self, admin_id: int):
        self.admin_id = admin_id

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_password(self):
        return self.password

    def set_password(self, password: str):
        self.password = password

    # Override __repr__ for better string representation
    def __repr__(self):
        return f"Admin(admin_id={self.admin_id}, name={self.name})"
