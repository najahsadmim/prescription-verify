class MedicalAppException(Exception):
  pass

class InvalidImageError(MedicalAppException):
  pass

class MedicalValidationError(MedicalAppException):
  pass
