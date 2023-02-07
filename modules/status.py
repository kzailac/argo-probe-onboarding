class Status:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        self.status_code = self.OK
        self.status_msg = "OK"

    def ok(self, msg):
        self.status_code = self.OK
        self.status_msg = f"OK - {msg}"

    def warning(self, msg):
        self.status_code = self.WARNING
        self.status_msg = f"WARNING - {msg}"

    def critical(self, msg):
        self.status_code = self.CRITICAL
        self.status_msg = f"CRITICAL - {msg}"

    def unknown(self, msg):
        self.status_code = self.UNKNOWN
        self.status_msg = f"UNKNOWN - {msg}"

    def get_msg(self):
        return self.status_msg

    def get_status_code(self):
        return self.status_code
