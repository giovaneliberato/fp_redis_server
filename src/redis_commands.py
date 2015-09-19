import copy


def info(conn, hashmap):
    return hashmap, "+Functional Python Redis Server running on %s port %d \r\n" % conn.getsockname()


def quit(*args):
    raise Exception("Bye!")


def _command_not_found(command):
    def inner(hashmap, *args):
        return hashmap, "-ERR unknown command '%s'\r\n" % command
    return inner


def set(_, hashmap, key, value):
    hashmap = copy.deepcopy(hashmap)
    hashmap[key] = value
    return hashmap, "+OK\r\n"


def get(_, hashmap, key):
    value = hashmap.get(key)
    return hashmap, "$%d\r\n%s\r\n" % (len(value), value)


def find(command):
    return globals().get(command, _command_not_found(command))


def _remove_quotes(string):
    return string.replace("\"", "").replace("'", "")


def discard_protocol_labels(params):
    return [param for param in params if param and param[0] not in ("*", "$", ":")]


def parse(data):
    params = discard_protocol_labels(data.split("\r\n"))
    return params[0].lower(), tuple([_remove_quotes(param) for param in params[1:]])
