from dataclasses import dataclass


@dataclass(frozen=True)
class Details:
    exception_error: str = 'We have already started to fix this error'
    success_status: str = 'Request successfully processed'
