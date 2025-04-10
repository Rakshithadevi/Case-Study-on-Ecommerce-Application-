import configparser
import os


class PropertyUtil:
    @staticmethod
    def get_database_config():
        config = configparser.ConfigParser()

        # Absolute Path
        config_path = os.path.join(os.path.dirname(__file__), "../config.ini")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        config.read(config_path)

        return {
            "host": config.get("database", "host"),
            "user": config.get("database", "user"),
            "password": config.get("database", "password"),
            "database": config.get("database", "database")
        }
