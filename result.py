class Result:
    def __init__(self, message: str = '', code: int = 0):
        self._message = message
        self._code = code

    @property
    def message(self) -> str:
        return self._message

    @property
    def code(self) -> int:
        return self._code
