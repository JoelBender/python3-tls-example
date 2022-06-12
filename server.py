import asyncio
import ssl


async def client_connected(reader, writer) -> None:
    # print(writer.get_extra_info("socket").getpeercert())
    print("peercert: " + str(writer.get_extra_info("peercert")))
    print("cipher: " + str(writer.get_extra_info("cipher")))

    writer.write(b"hai there ^_^\n")
    writer.close()


sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.load_cert_chain(certfile="server.crt", keyfile="server.key")
sslcontext.load_verify_locations("root.pem")

print(sslcontext.cert_store_stats())


async def main() -> None:
    server = await asyncio.start_server(
        client_connected, "127.0.0.1", 1234, ssl=sslcontext
    )

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
