from steam.steamid import SteamID

async def _get_steam_id(profile_url):
    try:
        return SteamID.from_url(profile_url)
    except Exception:
        return None

async def get_steam_id_64(profile_url):
    steam_id = await _get_steam_id(profile_url)
    return steam_id.as_64 if steam_id else None

async def get_account_id(profile_url):
    steam_id = await _get_steam_id(profile_url)
    return steam_id.as_32 if steam_id else None

async def get_steam_id_32_zero(profile_url):
    steam_id = await _get_steam_id(profile_url)
    return steam_id.as_steam2_zero if steam_id else None

async def is_valid_profile(profile_url):
    steam_id = await _get_steam_id(profile_url)
    return steam_id is not None
