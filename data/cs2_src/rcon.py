from rcon.source import rcon


async def send_rcon_command(ip, port, password, command):
    try:
        response = await rcon(
            command, 
            host=ip, 
            port=port, 
            passwd=password
        )
        return response
    except Exception as e:
        return str(e)
    
    
async def check_rcon_connect(ip, port, password) -> bool:
    try:
        response = await rcon(
            'status', 
            host=ip, 
            port=port, 
            passwd=password
        )

        return 'status' in response.lower()
    except Exception:
        return False