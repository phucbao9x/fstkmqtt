class MissingDataException(Exception): pass

class ConnectException:
    class DontHaveAnyConnectionException(Exception): pass

class NotEnoughPrivilege(Exception): pass

class NullConnectionError(Exception): pass

class DangerousRequestException(Exception) : pass