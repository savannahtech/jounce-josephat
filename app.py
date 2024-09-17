import os


from src import create_app
from src.infrastructure.config.settings import LocalConfig, TestConfig, UATConfig


env = os.environ.get("JOUNCE_ENV").lower()
if env == 'local':
    app = create_app(LocalConfig)
elif env == 'uat':
    app = create_app(UATConfig)
else:
    app = create_app(TestConfig)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
