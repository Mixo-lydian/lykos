from src.decorators import event_listener
from src.containers import UserDict
from src.functions import get_players
from src.messages import messages

__all__ = ["add_absent", "get_absent"]

ABSENT = UserDict() # type: UserDict[users.User, str]

def add_absent(var, target, reason):
    if target not in get_players():
        return

    ABSENT[target] = reason

    for votee, voters in list(var.VOTES.items()):
        if target in voters:
            voters.remove(target)
            if not voters:
                del var.VOTES[votee]
            break

def get_absent(var):
    return set(ABSENT.keys())

@event_listener("del_player")
def on_del_player(evt, var, player, allroles, death_triggers):
    del ABSENT[:player:]

@event_listener("lynch")
@event_listener("abstain")
def on_lynch_and_abstain(evt, var, user):
    if user in ABSENT:
        user.send(messages[ABSENT[user] + "_absent"])
        evt.prevent_default = True

@event_listener("revealroles")
def on_revealroles(evt, var, wrapper):
    if ABSENT:
        evt.data["output"].append("\u0002absent\u0002: {0}".format(", ".join(p.nick for p in ABSENT)))

@event_listener("transition_night_begin")
def on_transition_night_begin(evt, var):
    ABSENT.clear()

@event_listener("reset")
def on_reset(evt, var):
    ABSENT.clear()
