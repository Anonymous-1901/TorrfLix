import time
from tpblite import TPB
import subprocess as s
from pyfiglet import Figlet
import os
import speech_recognition as sr
import clipboard

path = "E:\\torrflix_downloads"
cache = "E:\\torrflix_cache"

def listen():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        print("Say Movie name . . .")
        data = r.listen(source, timeout=1, phrase_time_limit=4)
        try:
            speech = r.recognize_google(data)
            print(speech)
            return speech
        except Exception as e:
            print(e)


def stream_movies(*args):
    if not args:
        try:
            name = listen()
        except:
            print("Voice recognition cancelled")
            name = input("Enter a movie/game/show name : ")
    else:
        name=args[0]
    t = TPB()
    print("Searching :", name)
    while True:
        try:
            torrents = t.search(name)
            break
        except ConnectionError:
            print("Error connecting to the server , retrying . . . ")
            time.sleep(1)
            continue

    sr = 1
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(
        "|                                              Name                                           |   Seeders  |   Leechers  |      Size     |         Category        |")
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for torrent in torrents:
        split = str(torrent).split(',')
        movie_name = split[0]
        seeders = split[1].replace('S:', '')
        leechers = split[2].replace('L:', '')
        size = split[3]
        if sr <= 9:
            print("| " + str(sr) + "  > " + str(movie_name) + " " * (86 - len(movie_name)) + " | " + str(
                seeders) + " " * (11 - len(str(seeders))) + "|" + str(leechers) +
                  " " * (13 - len(str(leechers))) + "|" + str(size) + " " * (15 - len(str(size))) + "|" + str(
                torrent.category) + " " * (25 - len(str(torrent.category))) + "|")
        else:
            print(
                "| " + str(sr) + " > " + str(movie_name) + " " * (86 - len(movie_name)) + " | " + str(seeders) + " " * (
                        11 - len(str(seeders))) + "|" + str(leechers) +
                " " * (13 - len(str(leechers))) + "|" + str(size) + " " * (15 - len(str(size))) + "|" + str(
                    torrent.category) + " " * (25 - len(str(torrent.category))) + "|")
        sr += 1
    selection = int(input("\nEnter movie number  : "))
    selection -= 1
    print(torrents[selection].title)
    magnet = torrents[selection].magnetlink
    clipboard.copy(magnet)
    print("\nMagnet copied to clipboard !")
    stream = int(input("\nChoose a option  : \n1.Stream \n2.Download \n3.Select episode\n\n>"))
    if stream == 1:
        command = f"webtorrent download \"{magnet}\" --vlc -o E:\\torrflix_cache --not-on-top"
        s.run(command, shell=True)
        cont = input("Press ENTER to continue or q to exit . . .")


    elif stream == 2:
        # print(str(torrents[selection]) + "\n" + magnet)
        command = f"webtorrent download \"{magnet}\" -o {path}"
        s.run(command, shell=True)
        cont = input("Press ENTER to continue or q to exit . . .")

    elif stream == 3:
        while True:
            s.run("cls",shell=True)
            print("Getting file list . . .")
            outt = s.run(f"webtorrent \"{magnet}\" -s -q", shell=True, capture_output=True, text=True)
            episodes = outt.stdout
            episodes = episodes.replace("To select a specific file, re-run `webtorrent` with \"--select [index]\"", '')
            episodes = episodes.replace("Example: webtorrent download \"magnet:...\" --select 0", '')
            episodes = episodes.replace("webtorrent is exiting...", '')
            episodes = episodes.replace("download",'stream')
            print(episodes)
            episode_no = int(input("Choose an episode > "))
            command = f"webtorrent download \"{magnet}\" -s {episode_no} --vlc -o E:\\torrflix_cache --not-on-top"
            s.run(command, shell=True)
            while True:
                next_epi = input("Play next episode ?y/n : , \nb to go back : ")
                if next_epi == 'n':
                    cont = None
                    back = False
                    break
                    
                elif next_epi == 'b':
                    back = True
                    break
                else:
                    episode_no += 1
                    command = f"webtorrent download \"{magnet}\" -s {episode_no} --vlc -o E:\\torrflix_cache --not-on-top"
                    s.run(command, shell=True)
            if back:
                continue
            else:
                break
    return cont


def download_torrent():
    paste = clipboard.paste()
    if 'magnet:?xt=' in paste:
        print("Found a magnet that you copied !")
        download_this = paste
    else:
        download_this = input("Paste magnet :  ")
    s.run(f"webtorrent download \"{download_this}\" -o {path}", shell=True)
    cont = input("Press ENTER to continue or q to exit . . .")
    return cont


def clear_cache():
    clear = input(
        "WARNING:All of the downloaded files will be deleted , which means if you stream the same files again it will take more time and bandwidth ."
        "\n\nAre you sure you want to continue ?(y/n) : ")
    if clear.lower() == 'n':
        cont = input("Press ENTER to continue or q to exit . . .")
    else:
        s.run(f"pushd {cache} && rd /s /q . 2>nul", shell=True)
        if len(os.listdir(cache)) == 0:
            print("[+] Cache cleared successfully ")
            cont = input("Press ENTER to continue or q to exit . . .")
        else:
            print("Some Error occurred while clearing cache :(")
            cont = input("Press ENTER to continue or q to exit . . .")
    return cont


def wishlist():
    os.system('cls')
    print("1. View wishlist\n2.Add to wishlist\n3.Clear wishlist\n")
    wish = int(input("Choose an option : "))
    with open('wishlist.txt', 'r+') as file:
        if wish == 1:
            for line in file.readlines():
                print(line)
            cont = input("Press ENTER to continue or q to exit . . .")
        elif wish == 2:
            add_movie = input("Add this to wishlist : ")
            file.write("\n" + str(add_movie))
            print("Name added to watchlist")
            cont = input("Press ENTER to continue or q to exit . . .")
        else:
            print('that feature must be under devv. :(')
            cont = input("Press ENTER to continue or q to exit . . .")

    return cont


if __name__ == '__main__':
    f = Figlet()
    # listen()
    while True:
        s.run("cls", shell=True)
        print(f.renderText("TORRFLIX"))
        print("1.Stream/Download Movies \n2.Download Torrents \n3.Browse Downloads\n4.Wishlist\n5.Clear cache\n")
        option = input("Search a movie directly or Choose a option > ")
        try:
            option = int(option)
        except ValueError:
            cont = stream_movies(option)
            if cont == 'q':
                exit()

        if option == 1:
            cont = stream_movies()
            if cont == 'q':
                exit()
            else:
                continue
        elif option == 2:
            cont = download_torrent()
            if cont.lower() == 'q':
                exit()
            else:
                continue
        elif option == 3:
            s.run(f"explorer {path}", shell=True)
            cont = input("Press ENTER to continue or q to exit . . .")
            if cont.lower() == 'q':
                exit()
            else:
                continue
        elif option == 4:
            cont = wishlist()
            if cont.lower() == 'q':
                exit()
            else:
                continue
        elif option == 5:
            cont = clear_cache()
            if cont.lower() == 'q':
                exit()
            else:
                continue
        else:
            print("Wrong option chosen. ")
            continue
