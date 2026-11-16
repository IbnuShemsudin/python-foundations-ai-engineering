
class StudentNotFoundError(Exception):
    """Raised when a student cannot be found."""
    pass


class DuplicateStudentError(Exception):
    """Raised when a student ID already exists."""
    pass


class StorageError(Exception):
    """Raised when student data cannot be loaded or saved."""
    pass
