from flask_script import Manager
from app import app, db, models
from app.models import Resource
import unittest
import coverage
import os
from sqlalchemy.exc import IntegrityError

# Initializing the manager
manager = Manager(app)

# Test coverage configuration
COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[]
)
COV.start()

# Add test command
@manager.command
def test():
    """
    Run tests without coverage
    :return:
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# Run the manager
if __name__ == '__main__':
    manager.run()
