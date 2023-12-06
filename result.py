class Result:
    def __init__(self, action_name: str, message: str = '', code: int = 0):
        self._action_name = action_name
        self._message = message
        self._code = code

    @property
    def action_name(self) -> str:
        return self._action_name

    @property
    def message(self) -> str:
        return self._message

    @property
    def code(self) -> int:
        return self._code
