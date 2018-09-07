class VerificationException(Exception):
    pass


class NoArgumentsError(VerificationException):
    pass


class IpfsDataAttributeError(VerificationException):
    pass


class GrantedToUserDoesNotExist(VerificationException):
    pass


class VerifierUserDoesNotExist(VerificationException):
    pass


class VerifierUserValidationError(VerificationException):
    pass


class VerificationDoesNotExist(VerificationException):
    pass


class VerificationValidationError(VerificationException):
    pass


class CertificateDoesNotExist(VerificationException):
    pass


class CertificateValidationError(VerificationException):
    pass
