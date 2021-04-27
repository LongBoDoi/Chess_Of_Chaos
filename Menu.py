from Constant import _font
from GamePlay import *


def main_menu():
    first_menu = True
    while first_menu:
        mouse_pos = Vector2(mouse.get_pos())

        for g_event in event.get():
            if g_event.type == QUIT:
                return
            if g_event.type == MOUSEBUTTONDOWN:
                if g_event.button == 1:
                    if play_button.contains_mouse(mouse_pos):
                        first_menu = False

        screen.blit(game_background, (0, 300, 603, 783))
        game_title.render()
        play_button.render(mouse_pos)
        exit_button.render(mouse_pos)

        display.flip()

    second_menu = True
    while second_menu:
        mouse_pos = Vector2(mouse.get_pos())

        for g_event in event.get():
            if g_event.type == QUIT:
                return
            if g_event.type == MOUSEBUTTONDOWN:
                if g_event.button == 1:
                    if host_button.contains_mouse(mouse_pos):
                        return host_menu()
                    if join_button.contains_mouse(mouse_pos):
                        return join_menu()

        screen.blit(game_background, (0, 300, 603, 783))
        game_title.render()
        host_button.render(mouse_pos)
        join_button.render(mouse_pos)

        display.flip()


def host_menu():
    host_net.start_connection(host_net.server)

    host_ip = _font.render("Server created. Your IP: " + host_net.get_ip(), True, white)
    r_id = str(random.randint(1000, 9999))
    room_id = _font.render("Room ID: " + r_id, True, white)

    room_id_sent = False

    while True:
        connected = host_net.is_connected()

        for g_event in event.get():
            if g_event.type == QUIT:
                return
            if connected:
                if g_event.type == MOUSEBUTTONDOWN:
                    if g_event.button == 1:
                        if start_button.contains_mouse(Vector2(mouse.get_pos())):
                            # send start game command to the client
                            host_net.send("Start_game")
                            # get random player side and send the other side to client
                            p_color = random.randint(0, 1)
                            print("My side:", p_color)
                            host_net.send(str(1 - p_color))
                            return GamePlay(bool(p_color), True)

        # drawing
        screen.fill(black)
        screen.blit(game_background, (0, 300, 603, 783))
        game_title.render()
        screen.blit(host_ip, dest=((603 - host_ip.get_rect().width) / 2, 200))
        screen.blit(room_id, dest=((603 - room_id.get_rect().width) / 2, 240))
        status = _font.render("Opponent found." if connected else "Waiting for opponent...", True, white)
        screen.blit(status, dest=((603 - status.get_rect().width) / 2, 280))

        if not connected:
            host_net.listen()
        else:
            start_button.render(Vector2(mouse.get_pos()))
            if not room_id_sent:
                host_net.send(r_id)
                room_id_sent = True

        display.flip()


def join_menu():
    ip_heading = _font.render("IP:", True, white)
    typing = False
    ip_field = ""

    first_menu = True
    while first_menu:
        mouse_pos = Vector2(mouse.get_pos())

        for g_event in event.get():
            if g_event.type == QUIT:
                return
            if g_event.type == MOUSEBUTTONDOWN:
                if g_event.button == 1:
                    typing = Rect(150, 200, 300, 50).contains((mouse_pos.x, mouse_pos.y, 0, 0))

                    if join_button.contains_mouse(mouse_pos):
                        join_server.connect(ip_field)
                        if join_server.is_connected():
                            first_menu = False
            if g_event.type == KEYDOWN:
                if not typing:
                    break
                if g_event.key == K_BACKSPACE:
                    ip_field = ip_field[:-1]
                else:
                    ip_field += g_event.unicode
                    if len(ip_field) > 15:
                        ip_field = ip_field[:-1]

        screen.fill(black)
        screen.blit(game_background, (0, 300, 603, 783))
        game_title.render()
        draw.rect(screen, white if typing else grey, Rect(150, 200, 300, 50))
        screen.blit(ip_heading, dest=(110, 210))
        ip_text = _font.render(ip_field, True, black)
        screen.blit(ip_text, dest=(160, 207))
        find_button.render(mouse_pos)

        display.flip()

    second_menu = True
    room_id = join_server.receive(4)
    room_id = _font.render("Room ID: " + room_id, True, white)
    status = _font.render("Waiting for the host to start game.", True, white)
    while second_menu:
        for g_event in event.get():
            if g_event.type == QUIT:
                return

        # wait for start game command from the host
        cmd = join_server.receive(10)
        if cmd == "Start_game":
            side = int(join_server.receive(1))
            return GamePlay(bool(side), False)

        screen.fill(black)
        screen.blit(game_background, (0, 300, 603, 783))
        game_title.render()
        screen.blit(room_id, dest=((603 - room_id.get_rect().w) / 2, 240))
        screen.blit(status, dest=((603 - status.get_rect().w) / 2, 280))

        display.flip()
