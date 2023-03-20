import asyncio
import asyncpg


class ProxyDatabase:
    def __init__(self, uri):
        self.uri = uri
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.uri)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def fetchrow_dict(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args, record_class=dict)

    async def fetch_dict(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args, record_class=dict)

    async def add_proxy(self, ip_address, port, username=None, password=None, is_alive=True):
        await self.execute(
            'INSERT INTO proxies (ip_address, port, username, password, is_alive) VALUES ($1, $2, $3, $4, $5);',
            ip_address, port, username, password, is_alive)

    async def get_all_proxies(self):
        return await self.fetch_dict('SELECT * FROM proxies;')

    async def get_alive_proxies(self):
        return await self.fetch_dict('SELECT * FROM proxies WHERE is_alive = true;')

    async def set_proxy_status(self, ip_address, port, is_alive):
        await self.execute('UPDATE proxies SET is_alive = $1 WHERE ip_address = $2 AND port = $3;',
                            is_alive, ip_address, port)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()
