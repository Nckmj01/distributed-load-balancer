M = 512      # Total slots in the hash ring
K = 9        # Virtual servers per physical server


def H(request_id):
    return (request_id**2 + 2*request_id + 17) % M


def Phi(server_id, virtual_id):
    return (server_id**2 + virtual_id**2 + 2*virtual_id + 25) % M


class ConsistentHash:

    def __init__(self):
        self.ring = [None] * M
        self.servers = []

    def add_server(self, server_id):

        if server_id in self.servers:
            return

        self.servers.append(server_id)

        for j in range(K):

            idx = Phi(server_id, j)

            while self.ring[idx] is not None:
                idx = (idx + 1) % M

            self.ring[idx] = server_id

    def remove_server(self, server_id):

        if server_id not in self.servers:
            return

        self.servers.remove(server_id)

        for i in range(M):

            if self.ring[i] == server_id:
                self.ring[i] = None

    def get_server(self, request_id):

        idx = H(request_id)

        for i in range(M):

            pos = (idx + i) % M

            if self.ring[pos] is not None:
                return self.ring[pos]

        return None
