from GameArt import *
import random
import sys
import time
import os
import json

class Duskers:

    def __init__(self):
        self.option = None
        self.save_content_json = None
        self.save_slots = ['empty', 'empty', 'empty']
        self.used_slots = None
        self.save_content = None
        self.name = None
        self.titanium = 0
        self.robot_count = 3
        self.file_name = None
        self.saved_dict = {}
        self.locations = locations
        self.difficulty = difficulty
        self.exiting = False

        # upgrades
        self.titanium_scan = False
        self.enemy_enc_scan = False

    def menu(self):
        print(ART_DISPLAY)
        user_input = input(
            "[New] Game\n[Load] game\n[High] Scores\n[Help]\n[Exit]\n\n"
            "Your command:")

        while user_input.lower() not in ['new', 'load', 'high', 'help', 'exit']:
            print("Invalid input")

            user_input = input("\nYour command:")

        if user_input.lower() == 'high':
            self.high_score()

        if user_input.lower() == 'load':
            self.game_load()

        if user_input.lower() == 'help':
            print(GAME_HELP, '\n')
            go_back = input('To go back into the menu, please type in "back": ')

            while go_back != 'back':
                print('only [back] is available')
                go_back = input()
            self.menu()

        if user_input.lower() == 'exit':
            self.exit()

        if user_input.lower() == 'new':
            self.play()

    def high_score(self):
        print("\n\t\tHIGH SCORES\n")
        if os.path.isfile('highscores.txt'):
            high_scores_list = []
            with open('highscores.txt', 'r') as file:
                for x in file.readlines():
                    y = x.split(' ')
                    y[1] = y[1].rstrip('\n')
                    y[1] = int(y[1])
                    high_scores_list.append(y)

            high_scores_list = sorted(high_scores_list, key=lambda z: z[1],
                                      reverse=True)

            for index, scoreboard in enumerate(high_scores_list[:10], start=1):
                print(f"({index})", scoreboard[0], scoreboard[1])

            print("\n\t[Back]")

            action = input('Your command:')
            while action != 'back':
                print("Invalid input, only [back] is available")
                action = input('Your command:')

            self.menu()

        else:
            print("There are no highscores.\n[Back]")
            action = input('Your command')

            while action.lower != 'back':
                print('Invalid input, only [back] is available')
                action = input('Your command')

            self.menu()

        self.menu()

    def play(self):
        self.name = input("\nEnter your name:\n")
        print(f"\nGreetings, commander {self.name}!\n"
              f"Are you ready to begin?\n[Yes] [No] "
              f"Return to Main[Menu]\n")
        while True:
            begin = input("Your command:")
            if begin.lower() == 'yes':
                lumps = 0
                self.exploration()
            elif begin.lower() == 'no':
                print("\nHow about now.\nAre you ready to begin?\n\t"
                      "[Yes] [No]\n")

            elif begin.lower() == 'menu':
                Duskers().menu()
            else:
                print("Invalid input")

    def game_save(self):
        found = False
        saves = [1, 2, 3]
        occupied_slots = []
        print('Select save slot: ')

        for x in saves:
            if os.path.isfile(f"save_file{x}.json"):
                occupied_slots.append(str(x).strip('[]'))
                if len(occupied_slots) > 0:
                    found = True

        for x in range(len(occupied_slots)):
            occupied_slots[x] = int(occupied_slots[x])

        if not found:
            for slot, save_name in enumerate(self.save_slots):
                print(f"[{slot + 1}] {save_name}")
                self.saved_dict[f"{slot + 1}"] = save_name

            action = input('Your command:')

            if action in self.saved_dict.keys():
                date_of_save = time.strftime("%Y-%m-%d %H:%M")
                self.save_content = {
                    "name": self.name,
                    "Titanium": self.titanium,
                    "Robots": self.robot_count,
                    "Last save": date_of_save,
                    "Titanium scan": self.titanium_scan,
                    "Enemy scanner": self.enemy_enc_scan
                }

                self.save_content_json = json.dumps(self.save_content)
                with open(f'save_file{action}.json', 'w') as file:
                    file.write(self.save_content_json)

                if self.option.lower() == 'save' and self.exiting:
                    print("Saved successfully!")
                    self.exit()

                print(GAME_SAVE)
                self.exploration()

        elif found:
            for x in occupied_slots:
                with open(f'save_file{x}.json', 'r') as file:
                    data = json.load(file)
                    player_name = data['name']
                    titanium = data['Titanium']
                    robots = data['Robots']
                    time_of_save = data['Last save']
                    titanium_scan = data['Titanium scan']
                    enemy_scanner = data['Enemy scanner']

                if titanium_scan and not enemy_scanner:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save}" \
                        f" Purchased upgrades: Titanium scan"
                elif enemy_scanner and not titanium_scan:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save}" \
                        f" Purchased upgrades: Enemy encounter scanner"
                elif enemy_scanner and titanium_scan:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save}" \
                        f" Purchased upgrades: Titanium scan," \
                        f" Enemy encounter scanner"
                else:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save} Purchased upgrades: None"

                self.save_slots[x - 1] = save_file_name

            while True:

                for slot, save_name in enumerate(self.save_slots):
                    print(f"[{slot + 1}] {save_name}")
                    self.saved_dict[f"{slot + 1}"] = save_name

                action = input('Your command:')

                if action in self.saved_dict.keys():

                    date_of_save = time.strftime("%Y-%m-%d %H:%M")
                    self.save_content = {
                        "name": self.name,
                        "Titanium": self.titanium,
                        "Robots": self.robot_count,
                        "Last save": date_of_save,
                        "Titanium scan": self.titanium_scan,
                        "Enemy scanner": self.enemy_enc_scan
                    }

                    self.save_content_json = json.dumps(self.save_content)
                    with open(f'save_file{action}.json', 'w') as file:
                        file.write(self.save_content_json)

                    if self.option.lower() == 'save' and self.exiting:
                        print("Saved successfully!")
                        self.exit()

                    print(GAME_SAVE)
                    self.exploration()

    def game_load(self):
        found = False
        saves = [1, 2, 3]
        occupied_slots = []
        print('Select save slot: ')

        for x in saves:
            if os.path.isfile(f"save_file{x}.json"):
                occupied_slots.append(str(x).strip('[]'))
                if len(occupied_slots) > 0:
                    found = True

        for x in range(len(occupied_slots)):
            occupied_slots[x] = int(occupied_slots[x])

        if not found:
            while True:
                for slot, save_name in enumerate(self.save_slots):
                    print(f"[{slot + 1}] {save_name}")
                    self.saved_dict[f"{slot + 1}"] = save_name

                action = input('Your command:')

                if action in self.saved_dict.keys():
                    if self.saved_dict[action] == 'empty':
                        print('Empty slot!')
                        continue
                    else:
                        with open(f'save_file{action}.json', 'r') as file:
                            data = json.load(file)
                            self.titanium = data['Titanium']
                            self.name = data['name']
                            self.robot_count = data['Robots']
                            self.titanium_scan = data['Titanium scan']
                            self.enemy_enc_scan = data['Enemy scanner']
                    print(GAME_LOAD.format(self.name))
                    self.exploration()
                elif action == 'back':
                    self.menu()

        if found:
            for x in occupied_slots:
                with open(f'save_file{x}.json', 'r') as file:
                    data = json.load(file)
                    player_name = data['name']
                    titanium = data['Titanium']
                    robots = data['Robots']
                    time_of_save = data['Last save']
                    titanium_scan = data['Titanium scan']
                    enemy_scanner = data['Enemy scanner']

                if titanium_scan and not enemy_scanner:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save}" \
                        f" Purchased upgrades: Titanium scan"
                elif enemy_scanner and not titanium_scan:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save}" \
                        f" Purchased upgrades: Enemy encounter scanner"
                elif enemy_scanner and titanium_scan:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save}" \
                        f" Purchased upgrades: Titanium scan," \
                        f" Enemy encounter scanner"
                else:
                    save_file_name = \
                        f"{player_name} Titanium: {titanium} Robots: {robots}" \
                        f" Last save: {time_of_save} Purchased upgrades: None"

                self.save_slots[x - 1] = save_file_name

            while True:
                for slot, save_name in enumerate(self.save_slots):
                    print(f"[{slot + 1}] {save_name}")
                    self.saved_dict[f"{slot + 1}"] = save_name

                action = input('Your command:')

                if action in self.saved_dict.keys():
                    if self.saved_dict[action] == 'empty':
                        print('Empty slot!')
                        continue
                    else:
                        with open(f'save_file{action}.json', 'r') as file:
                            data = json.load(file)
                            self.titanium = data['Titanium']
                            self.name = data['name']
                            self.robot_count = data['Robots']
                            self.titanium_scan = data['Titanium scan']
                            self.enemy_enc_scan = data['Enemy scanner']
                    print(GAME_LOAD.format(self.name))
                    self.exploration()

    def exploration(self):

        print(robotprint(self.robot_count).format(self.titanium))

        while True:
            self.option = input('Your command:')

            if self.option.lower() == 'save':
                self.game_save()

            elif self.option.lower() == 'ex':

                loc_am = random.randint(1, 9)
                loc_list = []
                answers = ["s", "back"]

                answer = True
                while answer:
                    if loc_am > 0:
                        if self.difficulty == 'easy':
                            loc_list.append([random.choice(locations),
                                             random.randint(10, 100),
                                             random.random() - 0.2])
                        elif self.difficulty == 'hard':
                            loc_list.append([random.choice(locations),
                                             random.randint(10, 100),
                                             random.random() + 0.2])
                        else:
                            loc_list.append([random.choice(locations),
                                             random.randint(10, 100),
                                             random.random()])

                        percent = round(loc_list[0][2] * 100)
                        percent = str(int(percent)) + "%"

                        search_animation()

                        if not self.titanium_scan and not self.enemy_enc_scan:
                            for index, visited in enumerate(loc_list):
                                print(f"[{index + 1}] {visited[0]}")
                        elif self.titanium_scan and not self.enemy_enc_scan:
                            for index, visited in enumerate(loc_list):
                                print(f"[{index + 1}] {visited[0]}: Titanium: "
                                      f"{visited[1]}")
                        elif self.enemy_enc_scan and not self.titanium_scan:
                            for index, visited in enumerate(loc_list):
                                print(f"[{index + 1}] {visited[0]} "
                                      f"Encounter rate: {percent}")
                        else:
                            for index, visited in enumerate(loc_list):
                                print(f"[{index + 1}] {visited[0]}: Titanium: "
                                      f"{visited[1]} Encounter rate: {percent}")

                        answers.append(str(index + 1))
                        loc_am = loc_am - 1
                        print("\n[S] to continue searching")

                        action = input('Your command:')

                    else:
                        print("Nothing more in sight.")
                        print("Please choose one of the found locations")
                        action = input('Your command:')

                    if action.lower() == 's':
                        answer = True

                    elif action == "back":
                        self.exploration()

                    elif action in answers:
                        encounter = False

                        location_name = loc_list[int(action) - 1][0]
                        titanium_found = loc_list[int(action) - 1][1]
                        enemy_encounter_rate1 = loc_list[int(action) - 1][2]

                        enemy_encounter_rate2 = random.random()

                        if enemy_encounter_rate2 < enemy_encounter_rate1:
                            encounter = True

                        if encounter and self.robot_count > 1:
                            print("Deploying robots")
                            print("Enemy encounter")
                            print(f"{location_name} explored successfully, 1 robot"
                                  f" lost...")
                            self.robot_count -= 1
                        elif encounter and self.robot_count == 1:

                            print("Enemy encounter!!!\nMission aborted, the last "
                                  "robot lost...")
                            print(GAME_OVER)

                            with open('highscores.txt', 'a') as file:
                                data = self.name + ' ' + str(self.titanium)
                                file.write(data + "\n")

                            self.titanium = 0
                            self.robot_count = 3
                            Duskers.menu(self)

                        else:
                            print(f"{location_name} explored successfully,"
                                  f" with no damage taken.")

                        self.titanium += titanium_found
                        print(f"Acquired {titanium_found} lumps of titanium")
                        self.exploration()
                    else:
                        print("Invalid input, still searching")

            elif self.option.lower() == 'm':
                print(GAME_MENU)
                self.option = input('Your command:')
                if self.option.lower() == 'back':
                    self.exploration()
                elif self.option.lower() == 'main':
                    self.menu()
                elif self.option.lower() == 'save':
                    self.exiting = True
                    self.game_save()
                elif self.option.lower() == 'exit':
                    self.exit()

            elif self.option.lower() == 'up':
                print(GAME_UPGRADES)

            elif self.option.lower() == 'back':
                choice = input('Go back to main menu?: ')
                while choice.lower() not in ['yes', 'no']:
                    print('Wrong input, only [yes] or [no] are available')
                    choice = input('Go back to main menu?: ')
                if choice.lower() == 'yes':
                    self.menu()
                else:
                    self.exploration()
            else:
                print('Invalid input')
                continue

            while True:
                action = input('Your command:')
                if action == '1':
                    if (self.titanium - 250) < 0:
                        print("Insufficient titanium!")
                        continue
                    else:
                        self.titanium -= 250
                        self.titanium_scan = True
                        print("Purchase successful. You can now see how much titanium "
                              "you can get from each found location.")
                        self.exploration()
                elif action == '2':
                    if (self.titanium - 500) < 0:
                        print("Insufficient titanium!")
                        continue
                    else:
                        self.titanium -= 500
                        self.enemy_enc_scan = True
                        print("Purchase successful. You will now see the percentage of "
                              "likeliness of encountering an enemy at each found location.")
                        self.exploration()

                elif action == '3':
                    if (self.titanium - 1000) < 0:
                        print("Insufficient titanium!")
                        continue
                    else:
                        self.titanium -= 1000
                        self.robot_count += 1
                        print("Purchase successful. You now have an additional robot")
                        self.exploration()
                elif action == 'back':
                    self.exploration()

                else:
                    print("Invalid input")
                    continue

    def exit(self):
        print("\nThanks for playing, bye!\n")
        return exit()


def search_animation():
    animation = [
        ".",
        "..",
        "...",
    ]
    i = 0
    while i != len(animation):
        print('\rSearching' + animation[i % len(animation)], end='')
        time.sleep(0.3)
        i += 1
    print('\n')


def main():
    """
    If using command line arguments for executing the program, use this syntax:

    ~python (file_name) (1st arg) (2nd arg)

    where:
    1st arg - difficulty (easy, medium, hard)
    2nd arg - locations separated by comma

    example: python main.py medium place1,place2,place3

    default difficulty is medium
    default locations are hard coded by myself

    difficulties:
    easy - all encounter chances are lowered by 20%
    medium - all encounter chances will be default
    hard - all encounter changes are raised by 20%

    """

    global locations, difficulty

    difficulty = "medium"

    locations = ["Sunrise Sierra", "Silk Valley", "Old Junkyard",
                 "Abandoned Mansion", "Snow grove", "Dry Lake",
                 "Gold Mountain", "Dark Forest"]

    args = sys.argv

    if len(args) >= 2:
        if args[1] not in ['easy', 'medium', 'hard']:
            locations.clear()
            for x in args[1].split(','):
                locations.append(x)
        else:
            difficulty = args[1]

    if len(args) == 3:
        locations.clear()
        for x in args[2].split(','):
            locations.append(x)

    elif len(args) > 3:
        print('too many arguments, please run the program again with either'
              ' 1 or 2 arguments')
        exit(1)

    Duskers().menu()


if __name__ == '__main__':
    main()