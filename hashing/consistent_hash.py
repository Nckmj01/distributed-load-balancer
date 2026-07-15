M = 512      # Number of slots in the hash ring
K = 9        # Number of virtual nodes per physical server


# Hash function for mapping client requests to the hash ring.
def H(request_id):
    return (131 * request_id + 17) % M


# Hash function for placing virtual servers on the hash ring.
def Phi(server_id, virtual_id):
    return (97 * server_id + 131 * virtual_id + 17) % M


class ConsistentHash:

    def __init__(self):
        # Initialize an empty hash ring and server list.
        self.ring = [None] * M
        self.servers = []

    def add_server(self, server_id):

        # Prevent duplicate server entries.
        if server_id in self.servers:
            return

        self.servers.append(server_id)

        # Place each virtual server on the hash ring.
        for j in range(K):

            idx = Phi(server_id, j)

            # Resolve collisions using linear probing.
            while self.ring[idx] is not None:
                idx = (idx + 1) % M

            self.ring[idx] = server_id

    def remove_server(self, server_id):

        # Ignore requests to remove non-existent servers.
        if server_id not in self.servers:
            return

        self.servers.remove(server_id)

        # Remove all virtual nodes belonging to the server.
        for i in range(M):

            if self.ring[i] == server_id:
                self.ring[i] = None

    def get_server(self, request_id):

        # Map the request to its assigned server.
        idx = H(request_id)

        # Search clockwise until a server is found.
        for i in range(M):

            pos = (idx + i) % M

            if self.ring[pos] is not None:
                return self.ring[pos]

        return None
