from enum import Enum

AMERICAS = "AMERICAS"
ASIA = "ASIA"
ESPORTS = "ESPORTS"
EUROPE = "EUROPE"

queue_types = {
    "ranked_solo": {
        "id": "RANKED_SOLO_5x5",
        "description": "Ranked Solo"
    },
    "ranked_flex": {
        "id": "RANKED_FLEX_SR",
        "description": "Ranked Flex"
    }
}


class Region(Enum):
    BR = "BR1"
    EUNE = "EUN1"
    EUW = "EUW1"
    JP = "JP1"
    KR = "KR"
    LA1 = "LA1"
    LA2 = "LA2"
    NA = "NA1"
    OCE = "OC1"
    PH = "PH2"
    RU = "RU"
    SG = "SG2"
    TH = "TH2"
    TR = "TR1"
    TW = "TW2"
    VN = "VN2"


def process_region(region):
    try:
        region = Region(region)
    except ValueError:
        raise ValueError(f"{region} is not a valid color")
    print(f"Processing {region.name.lower()} region")


#ENDPOINTS
RIOT_ACCOUNT_ENDPOINT = ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
RIOT_LOL_SUMMONER_ENDPOINT = ".api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
RIOT_LOL_LEAGUE_ENTRIES_ENDPOINT = ".api.riotgames.com/lol/league/v4/entries/by-summoner/"
