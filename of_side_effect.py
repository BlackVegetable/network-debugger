
class OFSideEffect:
    def __init__(self, command, src_ip=None, dst_ip=None, src_port=None, dst_port=None):
        if (not command == "add") and (not command == "remove"):
            raise Exception("command must be 'add' or 'remove'")
        if (not src_ip) and (not dst_ip) and (not src_port) and (not dst_port):
            raise Exception("At least one of src_ip, dst_ip, src_port, or dst_port" +
                            "must be set")
        self.source_ip = src_ip
        self.destination_ip = dst_ip
        self.source_port = src_port
        self.destination_port = dst_port
        self.command = command

    def is_opposite(self, other):
        return (self.source_ip == other.source_ip and
                self.destination_ip == other.destination_ip and
                self.source_port == other.source_port and
                self.destination_port == other.destination_port and
                ((self.command == "add" and other.command == "remove") or
                 (self.command == "remove" and other.command == "add")))

    def opposite(self):
        if self.command == "add":
            return OFSideEffect("remove", self.src_ip, self.dst_ip,
                                self.src_port, self.dst_port)
        return OFSideEffect("add", self.src_ip, self.dst_ip,
                            self.src_port, self.dst_port)

    def __str__(self):
        s = self.command + ":"
        if self.source_ip:
            s += " source ip = " + str(self.source_ip)
        if self.destination_ip:
            s += " destination ip = " + str(self.destination_ip)
        if self.source_port:
            s += " source port = " + str(self.source_port)
        if self.destination_port:
            s += " destination port = " + str(self.destination_port)
        return s
