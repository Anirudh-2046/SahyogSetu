"""
Language Service Domain Exceptions
"""

class LanguageServiceException(Exception):
    """Base exception for all language services."""
    def __init__(self, message: str, error_code: str = "language_service_error"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

class ProviderUnavailableException(LanguageServiceException):
    """Raised when an external speech or translation provider cannot be reached or is unconfigured."""
    def __init__(self, provider_name: str, reason: str):
        super().__init__(f"Provider '{provider_name}' unavailable: {reason}", "provider_unavailable")
        self.provider_name = provider_name
        self.reason = reason

class LanguageNotSupportedException(LanguageServiceException):
    """Raised when a task is requested for an unsupported language or dialect."""
    def __init__(self, language: str, task: str):
        super().__init__(f"Language '{language}' is not supported for task '{task}'.", "language_not_supported")
        self.language = language
        self.task = task

class AudioValidationException(LanguageServiceException):
    """Raised when uploaded audio fails format, size, or duration validation."""
    def __init__(self, reason: str):
        super().__init__(f"Audio validation failed: {reason}", "audio_validation_failed")
        self.reason = reason

class TranslationException(LanguageServiceException):
    """Raised when machine translation fails."""
    def __init__(self, message: str):
        super().__init__(message, "translation_failed")
