import os

# third-party imports
from flask_script import Manager # controller class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand

# local imports
from app import create_app, db
from app import models

app = create_app(config_name=os.getenv("FLASK_CONFIG"))
migrate = Migrate(app, db)
manger = Manager(app)

manger.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manger.run()
