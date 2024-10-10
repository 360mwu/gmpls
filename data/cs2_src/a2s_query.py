import a2s

async def get_server_info(ip, port):
    address = (ip, port)
    try:
        info = a2s.info(address)
        players = a2s.players(address)
        
        server_info = {
            'server_name': info.server_name,
            'map': info.map_name,
            'version': info.version,
            'player_count': info.player_count,
            'max_players': info.max_players,
            'players': [{'name': player.name, 'score': player.score, 'duration': player.duration} for player in players]
        }

        return server_info
    except:
        return None