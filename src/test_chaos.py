from  classes.game import Game
from test_setup import p,create, start_game,unames,vote
from fastapi.testclient import TestClient
from test_main import test_app
from api.routers.hub_endpoints import get_rooms

client = TestClient(test_app)

owner = p[0]
p1 = p[1]
p2 = p[2]
p3 = p[3]
p4 = p[4]

response_start = start_game(owner,"test-game")

def test_wrong_phase ():
    response = client.put(
        "test-game/chaos",
        headers=owner
    )
    assert response.status_code == 405


 
def deny_formula (alive_lads):
     #Let all vote nox
    for i in range(0, 5):
        if unames[i] in alive_lads:
            response = vote(header=p[i], vote="Nox", room_name="test-game")

def approve_formula (alive_lads):
    #Let all players vote Lumos
    for i in range(0, 5):
        if unames[i] in alive_lads:
            response = vote(header=p[i], vote="Lumos", room_name="test-game")


def get_chaos ():
    return client.get(
        "test-game/get-chaos",
        headers=owner
    )


def test_increase_chaos ():
    response_get_pregame1 = client.get(
        "/test-game/game_state",
        headers=p[0]
    )
    assert response_get_pregame1.status_code == 200
    print(response_get_pregame1.json())

    response_start = start_game(p[0], "test-game")
    print(response_start.json())
    # assert response_start.status_code == 201

    #Find who voldemort is 
    voldemort_uname = ""
    for k in range(0, 5):
        response_get_game = client.get(
            "/test-game/game_state",
            headers=p[k]
        )
        assert response_get_game.status_code == 200
        rta: dict = response_get_game.json()

        if rta['my_role'] == "Voldemort":
            voldemort_uname = unames[k]
        else:
            pass
    # print(f"Voldemort is: {voldemort_uname}")

    round_count = 0
    game_is_over = False
    de_score = 0
    fo_score = 0
    divination_casted = False
    avadas_avaliables = 2

    while not game_is_over and round_count < 30:
        round_count += 1
        response_get_ingame = client.get(
            "/test-game/game_state",
            headers=p[0]
        )
        assert response_get_ingame.status_code == 200

        rta: dict = response_get_ingame.json()
        # print(f"\nStart of round {round_count}")
        # print(rta)
        minister_uname: str = rta["minister"]
        minister_index = unames.index(minister_uname)
        director_index = (minister_index + 1) % 5
        director_uname: str = unames[director_index]
        alive_lads = rta["player_list"]

        respone_propose = client.put(
            "/test-game/director",
            json={"director_email": director_uname},
            headers=p[minister_index]
        )
        assert respone_propose.status_code == 201

        deny_formula(alive_lads)

        response_get_ingame2 = client.get(
            "/test-game/game_state",
            headers=p[0]
        )
        assert response_get_ingame2.status_code == 200


        print(get_chaos().json())
        print("\nAfter the voting")
        if get_chaos() == 3:
            chaos = client.put(
                "test-game/chaos",
                headers=owner
            )
            print(chaos.json())
        

        response_get_ingame2 = client.get(
            "/test-game/game_state",
            headers=p[0]
        )
        assert response_get_ingame2.status_code == 200
        print(response_get_ingame2.json())

        if de_score > 2 and voldemort_uname == director_uname:
            # print("Death eaters won, voldi runs hogwarts")
            game_is_over = True
            break

        if de_score == 6:
            print("Death eaters won")
            game_is_over = True
            break
        elif fo_score == 5:
            print("Phoenix order won")
            break
        else:
            pass

        if (de_score == 4 or de_score == 5) and avadas_avaliables >= 1:
            print("ENTERING THE IF")
            victim_index = (minister_index - 1) % 5
            victim_uname = unames[victim_index]
            response_cast_avada = client.put(
                "/test-game/cast/avada-kedavra",
                headers=p[minister_index],
                json={"target_email": victim_uname}
            )
            print("Is " + victim_uname + " Really dead?")
            # print(response_cast_avada.json())
            assert response_cast_avada.status_code == 200
            avadas_avaliables -= 1
            if victim_uname == voldemort_uname:
                print("Voldemort died, F")
                game_is_over = True


    
test_increase_chaos()