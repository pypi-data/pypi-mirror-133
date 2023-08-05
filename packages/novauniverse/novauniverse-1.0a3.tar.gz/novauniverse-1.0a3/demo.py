import novauniverse as nova

player = nova.Player(player_name="THEGOLDENPRO")

session = nova.Session(session_id="95")
print(session.game.code_name)

#print(player.last_join)