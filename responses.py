import requests
import os

import constants
import settings

logger = settings.logging.getLogger("bot")


def get_response(riot_id: str, tag_line: str, queue_type: str, server: str) -> str:
    region = constants.Region[server].value
    return get_league_rank(riot_id, tag_line, region, queue_type)


def get_posts(url):
    logger.info(f"Trying Request for {url}")
    response = requests.get(url)

    if (response.status_code == 200):
        logger.info(f"Successfully retrieved {url}")
        return response.json()
    else:
        logger.error(f"Request failed : Error Code {response.status_code}")
        return


def get_riot_response(url):
    new_url = "{0}?api_key={1}".format(url, os.getenv("riot-key"))
    return get_posts(new_url)


def get_riot_puuid(game_tag, tag_line):
    region = constants.AMERICAS
    endpoint = ("https://" + region + constants.RIOT_ACCOUNT_ENDPOINT
                + game_tag + '/' + tag_line)
    response = get_riot_response(endpoint)
    if not response:
        logger.error(f"Unable to find puuid for {game_tag}#{tag_line}")
        return

    return response["puuid"], response["gameName"], response["tagLine"]


def get_summoner_id(puuid, region):
    endpoint = "https://" + region + constants.RIOT_LOL_SUMMONER_ENDPOINT + puuid
    response = get_riot_response(endpoint)

    if not response:
        logger.error(f"Unable to find Summoner ID for {puuid}")
        return
    return response["id"]


def get_league_rank(game_tag, tag_line, region, queue_type):
    puuid, game_tag, tag_line = get_riot_puuid(game_tag, tag_line)
    if not puuid:
        return "{}#{} could not be found".format(game_tag, tag_line)

    summoner_id = get_summoner_id(puuid, region)
    if not summoner_id:
        return "{}#{} could not be found".format(game_tag, tag_line)

    endpoint = "https://" + region + constants.RIOT_LOL_LEAGUE_ENTRIES_ENDPOINT + summoner_id
    rank = parse_league_rank(get_riot_response(endpoint), queue_type)

    if not rank:
        return f"{game_tag}-{tag_line} is Unranked"
    wins = rank["wins"]
    losses = rank["losses"]

    response = (
        "{}#{}: {} : {} : {} {} LP ".format(game_tag, tag_line, constants.queue_types.get(queue_type).get("description"),
                                      rank["tier"], rank["rank"], rank["leaguePoints"]))
    response += "\nWins: {}, Losses {} W/L: {}%".format(wins, losses, str(round((wins / (wins + losses)) * 100)))
    return response


def parse_league_rank(response, queue_type):
    if not response:
        return
    rank = (list(filter(lambda rankData: rankData["queueType"] == constants.queue_types[queue_type]["id"], response)))
    if len(rank) == 0:
        return
    return rank[0]
