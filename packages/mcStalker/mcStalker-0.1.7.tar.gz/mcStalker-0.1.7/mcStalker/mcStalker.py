import asyncio, aiohttp, json


class MCStalker:
    """The Parent Class, Do not import this."""

    def __init__(self, apiKey):
        self.key = apiKey

    class invalidApiKey(Exception):
        """The invalidApiKey error."""

        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Invalid API Key (Register at https://mcstalker.com/register)- {0} ".format(
                self.message
            )


class Stats(MCStalker):
    """The Stats class."""

    class _Stats:
        """The statistics of the API.
        updated: str = The last time the statistics were updated.
        players: int = The number of players currently in the database.
        servers: int = The number of servers currently in the database.
        raw: dict = The raw, cleaned data from the API.
        """

        updated: str = ""
        servers: int = None
        players: int = None
        raw: dict = None

    @staticmethod
    def returnCleanStatsDict(stats: dict):
        """Returns the statistics of the API.

        Args:
            stats (dict): The statistics of the API.

        Returns:
            dict: The statistics of the API.
        """
        _stats = {}
        _stats["lastUpdated"] = stats.get("updated")
        _stats["recentlySeenServers"] = stats.get("serversRecentlySeen")
        _stats["servers"] = stats.get("servers")
        _stats["players"] = stats.get("players")
        return _stats

    def returnStatsObject(self, statsDict: dict):
        """Returns the statistics of the API.

        Args:
            statsDict (dict): The statistics of the API.
        """
        stats = self._Stats()
        stats.updated = statsDict.get("lastUpdated")
        stats.servers = statsDict.get("servers")
        stats.players = statsDict.get("players")
        stats.recentlySeenServers = statsDict.get("recentlySeenServers")
        stats.raw = statsDict

    async def requestStats(self):
        """Requests the statistics of the API.

        Raises:
            MCStalker.invalidApiKey: If the API key is invalid.

        Returns:
            dict: The statistics of the API.
        """
        async with aiohttp.ClientSession() as session, session.get(
            "https://backend.mcstalker.com/api/stats",
            headers={"Authentication": f"Bearer {self.key}"},
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 403:
                raise MCStalker.invalidApiKey(await resp.json()["message"])

    async def returnStats(self):
        """Returns the statistics of the API.

        Returns:
            Stats._Stats: The statistics of the API.
        """
        return self.returnStatsObject(
            self.returnCleanStatsDict(await self.requestStats())
        )


def Help():
    """Returns the help message."""
    x = """
The MCStalker API Wrapper
---------------------------
Async-Friendly wrapper for the MCStalker API.

*MAINTAINED DOCS AT https://github.com/TheOnlyWayUp/mcStalkerApiWrapper/wiki*

Endpoints currently supported - 
- /stats
- /searchusername
- /searchserver
- /filterservers

YOU NEED AN API KEY TO USE THIS WRAPPER.
You can register for a key at https://mcstalker.com/register

Imports - 
- from mcStalker.mcStalker import Player
- from mcStalker.mcStalker import Server
- from mcStalker.mcStalker import Stats

Usage -

    Stats -
        from mcStalker.mcStalker import Stats
        stats = Stats(apiKey)
        asyncio.run(stats.returnStats() -> Stats._Stats Object)

    Player -
        from mcStalker.mcStalker import Player
        player = Player(apiKey)
        asyncio.run(player.returnPlayer(username) -> Player._Player Object)

    Server - 
        from mcStalker.mcStalker import Server
        server = Server(apiKey)
        asyncio.run(server.returnServer(ip) -> Server._Server Object)
        asyncio.run(server.returnTopServers() -> [Server._Server Object, Server._Server Object, ...])

Created by TheOnlyWayUp#1231 - https://github.com/TheOnlyWayUp/
MCStalker created by SSouper - https://github.com/SSouper
    """
    print(x)


class Server(MCStalker):
    """The Server class, which is used to generate information about a server."""

    class _ipInfo:
        """The _ipInfo object, which is used to generate information about an IP."""

        loc = None
        org = None
        city = None
        postal = None
        region = None
        country = None
        hostname = None
        timezone = None

    class _Server:
        """The Server Object.
        ip: str = The IP address of the server.
        hostname: str = The hostname of the server.
        favicon: base64 string = The favicon of the server.
        players: list[MCStalker.Player()] = A list of players on the server.
        slots: dict{'online':None, 'max':None} = Player slots of the server.
        motd: str = The MOTD of the server.
        added: Unix timestamp = The time the server was added to the database.
        lastPinged: Unix timestamp = The time the server was last updated.
        vanilla: bool = Whether the server is vanilla or not.
        modified: bool = Whether the server is modified or not.
        authStatus: str = The authentication status of the server.
        ipInfo: MCStalker._ipInfo = The IP information of the server.
        version: str = The human friendly version of the server.
        raw: dict = The raw Cleaned JSON response from the server.
        """

        ip = ""
        favicon = ""
        hostname = None
        players = []
        slots = {"online": None, "max": None}
        motd = ""
        added = "Unix Timestamp"
        lastPinged = "Unix Timestamp"
        vanilla = bool
        ipInfo = None
        version: str = None
        raw = ""
        modded = None
        authStatus = 0

    class _Player:
        """The _Player object, which is used to generate information about a player. Please read the docs for Player() instead."""

        name = ""
        uuid = ""
        addedAt = ""
        lastSeen = ""
        servers = []
        raw = ""

    class serverNotFound(Exception):
        """The requestError error."""

        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Server was not found - {0} ".format(self.message)

    def returnPlayerObject(self, player: dict):
        """Returns a player object.

        Args:
            player (dict): The dict containing player information.

        Returns:
            Player._Player: The player object.
        """
        _player = self._Player()
        _player.name = player["name"]
        _player.uuid = player["uuid"]
        _player.addedAt = player["addedAt"]
        _player.lastSeen = player["lastSeen"]
        try:
            _player.servers = [
                self.returnServerObject(self.returnCleanServerDict(p))
                for p in player["servers"]
            ]
        except TypeError:
            _player.servers = "To find a player's servers, please use the \"returnPlayer(username)\" method as the Server API doesn't return complete information."
        _player.raw = player
        return _player

    def returnCleanPlayerDict(self, player: dict):
        """Returns a cleaned player dict.

        Args:
            player (dict): The dict containing player information.

        Returns:
            dict: The cleaned player dict.
        """
        _player = {
            "name": player.get("username"),
            "uuid": player.get("uuid"),
            "addedAt": player.get("createdAt"),
            "lastSeen": player.get("updatedAt"),
            "servers": player.get("servers"),
        }
        return _player

    def convertAuthStatusToString(self, authStatus: int):
        aDict = {
            0: "Cracked",
            1: "OnlineMode",
            4: "Unknown",
            5: "Whitelisted_Cracked",
            6: "Whitelisted_Online",
            7: "Open_Cracked",
            8: "Open_OnlineMode",
            9: "Error",
        }
        return aDict[authStatus], authStatus

    def returnCleanMotd(self, motd) -> str:
        """DONT USE, ALTERNATIVE USED IN CODE!!!
        Returns a cleaned MOTD.

        Args:
            motd (any): The MOTD to clean.

        Returns:
            str: The cleaned MOTD.
        """
        if type(motd) is list:
            return "".join([letter["text"] for letter in motd])
        if type(motd) is str:
            return motd
        if type(motd) is dict:
            try:
                return motd["text"]
            except KeyError:
                return self.returnCleanMotd(motd["extra"])
        return None

    def returnCleanServerDict(self, server: dict) -> dict:
        """Returns a clean dict with only the things we need in all the correct places.

        Args:
            server (dict): The dict to clean.

        Returns:
            dict: The cleaned dict.
        """
        _server = {
            "ip": server.get("ip"),
            "favicon": server.get("favicon"),
            "hostname": server.get("ipInfo").get("hostname"),
            "players": server.get("players"),
            "version": server.get("versionName"),
            "slots": {"online": server.get("online"), "max": server.get("max")},
            "motd": server.get("searchMotd"),
            "authStatus": server.get("authStatus"),
            "alive": server.get("alive"),
            "vanilla": server.get("vanilla"),
            "addedAt": server.get("createdAt"),
            "lastPinged": server.get("updatedAt"),
            "modded": server.get("modded"),
            "authStatus": server.get("authStatus"),
            "ipInfo": server.get("ipInfo"),
        }
        return _server

    def returnServerObject(self, server: dict) -> _Server:
        """Converts a dictionary to a Server object.

        Args:
            server (dict): The dict containing server information.

        Returns:
            Converters._Server: The server object.
        """
        _server = self._Server()
        _server.ip = server.get("ip")
        _server.favicon = server.get("favicon")
        _server.hostname = server.get("hostname")
        _server.slots = server.get("slots")
        try:
            _server.players = [
                self.returnPlayerObject(self.returnCleanPlayerDict(player))
                for player in server["players"]
            ]
        except TypeError:
            _server.players = []

        _server.motd = server.get("motd")
        _server.added = server.get("addedAt")
        _server.version = server.get("version")
        _server.lastPinged = server.get("lastPinged")
        _server.vanilla = server.get("vanilla")
        _server.modded = server.get("modded")
        _server.authStatus = self.convertAuthStatusToString(server.get("authStatus"))
        _server.ipInfo = self.returnIpObject(server["ipInfo"])
        _server.raw = server
        return _server

    def returnIpObject(self, ipInfo: dict) -> _ipInfo:
        """Converts a dictionary to an IP_Info object.

        Args:
            ipInfo (dict): The dict containing IP information.

        Returns:
            Converters._ipInfo: The IP_Info object.
        """
        _ipInfo = self._ipInfo()
        _ipInfo.loc = ipInfo.get("loc")
        _ipInfo.org = ipInfo.get("org")
        _ipInfo.city = ipInfo.get("city")
        _ipInfo.postal = ipInfo.get("postal")
        _ipInfo.region = ipInfo.get("region")
        _ipInfo.country = ipInfo.get("country")
        _ipInfo.hostname = ipInfo.get("hostname")
        _ipInfo.timezone = ipInfo.get("timezone")
        return _ipInfo

    async def requestServer(self, ip: str):
        """Requests a server from the API.

        Args:
            name (str): The IP to request.

        Returns:
            dict: The JSON response.
        """
        async with aiohttp.ClientSession() as session, session.get(
            f"https://backend.mcstalker.com/api/searchserver/{ip}",
            headers={"Authorization": f"Bearer {self.key}"},
        ) as response:
            return await response.json(), response.status

    async def requestTopServers(self, data: dict) -> dict:
        """Requests a list of servers from the API.

        Args:
            data (dict): The data to send.

        Returns:
            dict: The JSON response.
        """
        url = "https://backend.mcstalker.com/api/filterservers"
        async with aiohttp.ClientSession() as session, session.post(
            url,
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {self.key}",
            },
            data=json.dumps(data),
        ) as resp:
            return await resp.json(content_type="application/json"), resp.status

    async def returnServer(self, ip: str) -> _Server:
        """Returns a Server object.

        Args:
            ip (str): The IP address of the server.

        Returns:
            Converters._Server: The server object.
        """
        response = await self.requestServer(ip)
        # response = await response.json()
        status = response[1]
        response = response[0]
        if status == 200:
            server = self.returnServerObject(self.returnCleanServerDict(response))
            return server
        if status == 403:
            raise self.invalidApiKey(response.get("error"))
        raise self.serverNotFound(response.get("error"))

    async def returnTopServers(
        self,
        version: int = 756,
        sort: str = "updated",
        ascending: bool = False,
        peopleOnline: bool = True,
        country: str = "all",
        vanilla: bool = True,
        modded: bool = False,
        authStatus: str = "all",
        whitelistStatus: str = "all",
        motd: str = "",
        page: int = 1,
    ) -> list:
        """Returns the top servers as per the parameters defined. You can run the function without passing any, it'll return servers as per the recommended options.
        Version: 1.17.1
        Sort: Most recently added.
        Ascending: False
        People Online: True
        Country: All
        Vanilla: False
        Modded: False
        Auth Status: All
        Whitelist Status: All
        Motd: ""
        Page: 1

        Args:
            version (int - Protocol Number, optional): The version a server needs to have to be returned. Defaults to 756 (1.17.1).
            sort (str - "updated/new/empty/top", optional): What kind of servers to find. Defaults to "updated".
            ascending (bool, optional): Whether the results should be in ascending or descending order. Defaults to False.
            peopleOnline (bool, optional): If people have to be online on the server for it to be returned. Defaults to True.
            country (str, optional): The country a server must be located in. Defaults to 'all'.
            vanilla (bool, optional): Whether the server must be vanilla to be returned. Defaults to False.
            modded (bool, optional): Whether the server must be modded to be returned. Defaults to False.
            authStatus (str, optional): The cracked/online status of the server. Defaults to "all".
            whitelistStatus (str, optional): The whitelist status of the server. Defaults to "all".
            motd (str, optional): The MOTD a server must have to be returned. Defaults to "".
            page (int, optional): The page number. Defaults to 1.

        Returns:
            list: A list of Server Objects.
        """
        options = {
            "sortMode": sort,
            "ascdesc": "DESC" if not ascending else "ASC",
            "version": version,
            "country": country,
            "mustHavePeople": peopleOnline,
            "vanillaOnly": vanilla,
            "searchText": motd,
            "page": page,
            "modded": modded,
            "authStatus": authStatus,
            "whitelistStatus": whitelistStatus,
        }

        response = await self.requestTopServers(options)
        status = response[1]
        response = dict(response[0])
        if status == 200:
            return [
                self.returnServerObject(self.returnCleanServerDict(server))
                for server in response["result"]
            ]
        if status == 403:
            raise self.invalidApiKey(response["error"])
        raise self.serverNotFound(response["error"])


whyDoIEvenDoThis = Server("key")


class Player(MCStalker):
    """A class to handle player related functions."""

    class _Player:
        """The _Player object, which is used to generate information about a player. Please read the docs for Player() instead."""

        name = ""
        uuid = ""
        addedAt = ""
        lastSeen = ""
        servers = []
        raw = ""

    class playerNotFound(Exception):
        """The requestError error."""

        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Player was not found - {0} ".format(self.message)

    async def requestPlayer(self, name: str) -> _Player:
        """Requests a player.

        Args:
            name ([str]): The name of the player.

        Returns:
            dict: The player information.
        """
        async with aiohttp.ClientSession() as session, session.get(
            f"https://backend.mcstalker.com/api/searchusername/{name}",
            headers={"Authorization": f"Bearer {self.key}"},
        ) as resp:
            return await resp.json(), resp.status

    async def requestSearchPlayer(self, name):
        """Searches for a player, will return an array of user objects.

        Args:
            name (str): The name of the player.

        Returns:
            dict: The player information.
        """
        async with aiohttp.ClientSession() as session, session.get(
            f"https://backend.mcstalker.com/api/query/username/{name}",
            headers={"Authorization": f"Bearer {self.key}"},
        ) as resp:
            return await resp.json(), resp.status

    def returnPlayerObject(self, player: dict):
        """Returns a player object.

        Args:
            player (dict): The dict containing player information.

        Returns:
            Player._Player: The player object.
        """
        _player = self._Player()
        _player.name = player["name"]
        _player.uuid = player["uuid"]
        _player.addedAt = player["addedAt"]
        _player.lastSeen = player["lastSeen"]
        try:
            _player.servers = [
                whyDoIEvenDoThis.returnServerObject(
                    whyDoIEvenDoThis.returnCleanServerDict(p)
                )
                for p in player["servers"]
            ]
        except TypeError:
            _player.servers = []
        _player.raw = player
        return _player

    def returnCleanPlayerDict(self, player: dict):
        """Returns a cleaned player dict.

        Args:
            player (dict): The dict containing player information.

        Returns:
            dict: The cleaned player dict.
        """
        _player = {
            "name": player.get("username"),
            "uuid": player.get("uuid"),
            "addedAt": player.get("createdAt"),
            "lastSeen": player.get("updatedAt"),
            "servers": player.get("servers"),
        }
        return _player

    async def returnPlayer(self, username):
        """Returns a player object.

        Args:
            username (str): The username of the player.

        Raises:
            self.invalidApiKey: If the API key is invalid.
            self.playerNotFound: If the player was not found.

        Returns:
            Player._Player: The player object.
        """
        player = await self.requestPlayer(username)
        status = player[1]
        player = player[0]
        if status == 200:
            player = self.returnCleanPlayerDict(player)
            obj = self.returnPlayerObject(player)
            return obj
        if status == 403:
            raise self.invalidApiKey(player["error"])
        raise self.playerNotFound(player["error"])

    async def returnSearchPlayer(self, username):
        """Returns an array of player objects.

        Args:
            username (str): The username of the player.

        Raises:
            self.invalidApiKey: If the API key is invalid.
            self.playerNotFound: If the player was not found.

        Returns:
            Player._Player: The player object.
        """
        player = await self.requestSearchPlayer(username)
        status = player[1]
        playerList = player[0]
        if status == 200:
            player = [self.returnCleanPlayerDict(plr) for plr in playerList]
            obj = [self.returnPlayerObject(plr) for plr in player]
            return obj
        if status == 403:
            raise self.invalidApiKey(player["error"])
        raise self.playerNotFound(player["error"])
