import re
from .base_model import BaseModel


class User(BaseModel):
    """
    User class representing a user in the system.

    Inherits from BaseModel to gain basic functionalities such as ID and
    object management methods in the storage system.

    Attributes:
        first_name (str): The user's first name, limited to 50 characters.
        last_name (str): The user's last name, limited to 50 characters.
        email (str): The user's email address, must be a valid format.
        is_admin (bool): A boolean indicating if the user is an administrator
        (default is False).

    Methods:
        validate_name(name, field_name): Validates that the name/first name is
        not empty and has a maximum of 50 characters.
        validate_email(email): Validates that the email is in the correct
        format and is required.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initializes a new user with the specified attributes.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.
            is_admin (bool, optional): Indicates if the user is an
            administrator (default is False).

        Raises:
            ValueError: If any of the 'first_name', 'last_name', or 'email'
            fields are invalid.
        """
        # Call to BaseModel constructor to initialize ID and other attributes
        super().__init__()
        # Validate and assign the first name
        self.first_name = self.validate_name(first_name, 'First name')
        # Validate and assign the last name
        self.last_name = self.validate_name(last_name, 'Last name')
        # Validate and assign the email
        self.email = self.validate_email(email)
        # Assign the admin status (default is False)
        self.is_admin = is_admin

    def validate_name(self, name, field_name):
        """
        Validates that the first or last name is not empty and has a maximum
        of 50 characters.

        Args:
            name (str): The name or first name to validate.
            field_name (str): The name of the field
            (for customizing the error message).

        Returns:
            str: The validated name.

        Raises:
            ValueError: If the name is empty or exceeds 50 characters.
        """
        # Check if the name is empty or too long
        if not name or len(name) > 50:
            raise ValueError(
                f"{field_name} is required and must be 50 characters or fewer."
            )
        return name  # Return the validated name

    def validate_email(self, email):
        """
        Validates that the email is in a valid format.

        Args:
            email (str): The email address to validate.

        Returns:
            str: The validated email.

        Raises:
            ValueError: If the email is invalid.
        """
        # Regular expression to validate the email format
        email_regex = r'^\S+@\S+\.\S+$'
        # Check if the email is empty or not in the correct format
        if not email or not re.match(email_regex, email):
            raise ValueError("A valid email address is required.")
        # you could add a check for email uniqueness in the storage system
        return email  # Return the validated email
