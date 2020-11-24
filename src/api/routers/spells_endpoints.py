from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi_utils.tasks import repeat_every
from datetime import datetime, timedelta

from api.models.room_models import TargetedSpellRequest
from api.handlers.authentication import valid_credentials, get_username_from_token
from api.handlers.game_checks import check_game_preconditions
from api.utils.room_utils import check_email_status, votes_to_json

from classes.room import Room, RoomStatus
from classes.room_hub import RoomHub
from classes.role_enum import Role
from classes.game_status_enum import GamePhase
from classes.game import Vote, Game

from api.routers.room_endpoints import hub
router = APIRouter()

#hub = RoomHub()


@ router.get("/{room_name}/cast/divination", tags=["Spells"], status_code=status.HTTP_200_OK)
async def cast_divination(room_name: str = Path(..., min_length=6, max_length=20),
                          username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()
    if (phase == GamePhase.CAST_DIVINATION and username == minister):
        return {"cards": game.divination()}
    else:
        raise HTTPException(
            detail="You're not allowed to do this", status_code=405)


@ router.put("/{room_name}/cast/confirm_divination", tags=["Spells"], status_code=status.HTTP_200_OK)
async def confirm_divination(room_name: str = Path(..., min_length=6, max_length=20),
                             username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()

    if (phase == GamePhase.CAST_DIVINATION and username == minister):
        game.restart_turn()
        return {"message": "Divination confirmed, moving on"}
    else:
        raise HTTPException(
            detail="You're not allowed to do this", status_code=405)


@ router.put("/{room_name}/cast/avada-kedavra", tags=["Spells"], status_code=status.HTTP_200_OK)
async def cast_avada_kedavra(body: TargetedSpellRequest,
                             room_name: str = Path(...,
                                                   min_length=6, max_length=20),
                             username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()
    if (phase == GamePhase.CAST_AVADA_KEDAVRA and username == minister):
        if body.target_uname not in game.get_current_players():
            raise HTTPException(detail="Player not found", status_code=404)
        elif body.target_uname not in game.get_alive_players():
            raise HTTPException(
                detail="Player is already dead", status_code=409)
        else:
            game.avada_kedavra(body.target_uname)
            return {"message": "Successfully casted Avada Kedavra"}
    else:
        raise HTTPException(
            detail="You're not allowed to do this", status_code=405)


@ router.put("/{room_name}/cast/crucio", tags=["Spells"], status_code=status.HTTP_200_OK)
async def cast_crucio(body: TargetedSpellRequest,
                      room_name: str = Path(...,
                                            min_length=6, max_length=20),
                      username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()

    return {"message": "Successfully casted Crucio"}


@ router.put("/{room_name}/cast/confirm_crucio", tags=["Spells"], status_code=status.HTTP_200_OK)
async def confirm_crucio(room_name: str = Path(..., min_length=6, max_length=20),
                         username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()

    return {"message": "Successfully casted cCrucio"}


@ router.put("/{room_name}/cast/imperius", tags=["Spells"], status_code=status.HTTP_200_OK)
async def cast_imperius(body: TargetedSpellRequest,
                        room_name: str = Path(...,
                                              min_length=6, max_length=20),
                        username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()
    if (phase == GamePhase.CAST_IMPERIUS and username == minister):
        if body.target_uname not in game.get_current_players():
            raise HTTPException(detail="Player not found", status_code=404)
        elif body.target_uname == minister:
            raise HTTPException(
                detail="You cant choose yourself", status_code=409)
        else:
            game.imperius(casted_by=minister, target=body.target_uname)
            return {"message": "Successfully casted Imperius"}
    else:
        raise HTTPException(
            detail="You're not allowed to do this", status_code=405)


@ router.put("/{room_name}/cast/expelliarmus", tags=["Spells"], status_code=status.HTTP_200_OK)
async def cast_expelliarmus(room_name: str = Path(
                            ..., min_length=6, max_length=20),
                            username: str = Depends(get_username_from_token)):
    global hub
    room = check_game_preconditions(username, room_name, hub)

    game = room.get_game()
    phase = game.get_phase()
    minister = game.get_minister_user()

    return {"message": "Successfully casted Expelliarmus"}