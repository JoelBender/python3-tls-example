import asyncio
import ssl


async def connect() -> None:
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    sslcontext.check_hostname = False
    sslcontext.load_verify_locations("root.pem")
    sslcontext.load_cert_chain(certfile="client.crt", keyfile="client.key")

    reader, writer = await asyncio.open_connection("127.0.0.1", 1234, ssl=sslcontext)
    data = await reader.read()
    print(data)
    return


loop = asyncio.get_event_loop()

loop.run_until_complete(connect())
