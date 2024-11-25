from app import create_app
import sys
import os

# Adds the parent directory to the path to access the 'app' module
# This allows importing the 'app' module even if this file is executed
# from another directory.
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'app')))

# Imports the 'create_app' function from the 'app' module
# This function is used to create an instance of the Flask application.

# Creates an instance of the Flask application by calling 'create_app'
app = create_app()

if __name__ == '__main__':
    """
    This block checks if the script is executed directly
    (not imported as a module).
    If so, it starts the Flask application with the 'debug' option enabled.

    The 'debug=True' option allows the application to restart automatically on
    code changes and provides debugging information in case of errors.
    """
    app.run(debug=True)
