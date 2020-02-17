from app import create_app,db
from flask_script import Manager
from app.models import User,Workspace,Car,Trip,Review,WorkspaceUser

app = create_app('development')

manager = Manager(app)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Workspace=Workspace, Car=Car, Trip=Trip, Review=Review,WorkspaceUser=WorkspaceUser)

if __name__ == "__main__":
    manager.run()