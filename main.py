import socket
import sys
import re
from random import randint


class connect:

    @staticmethod
    def connectToServer(HOST="127.0.0.1"):
        try:
            PORT = 50007
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.sendall(b'getwords')
            data = s.recv(2048)
            s.close()
            var = re.sub(r"b*'", "", repr(data))
            print(var)
            return re.sub(r"Here are the words: ", "", var)
        except ConnectionResetError:
            print("Server is shutting down!")
        except ConnectionRefusedError:
            print("Server is not running!")
            user_input = input("Do you want to play with others?\nYes or No\n>")
            if user_input.lower() == "yes" or user_input.lower() == "y":
                game.mainGame(False)
            else:
                sys.exit(0)


class game:
    connectToServer = False

    hm_words = []

    def __init__(self):
        if self.connectToServer:
            conn = connect.connectToServer
            words = conn()
            self.hm_words = words.split(", ")
        else:
            import hmgetwords
            self.hm_words = hmgetwords.getwords().split(", ")
            print(self.hm_words)
        print("Do you want to play by" + "\u0332".join(" y") + "ourself" " or with" + "\u0332".join(" o") + "thers?")
        while True:
            user_input = input("> ")
            if user_input == "y":
                self.mainGame()
            elif user_input == "o":
                self.mainGame(False)
                break
            else:
                print("\u0332Y or \u0332O")
                continue

    def mainGame(self, single=True):
        if single:
            allowedkeys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                           "u", "v", "w", "x", "y", "z"]
            usedalphabet = []
            alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                        "u", "v", "w", "x", "y", "z"]
            hangman = ""
            hangmannum = 0
            unknownWord = ""
            gameWon = False
            rannum = randint(0, len(self.hm_words) - 1)
            wordToGuess = self.hm_words[rannum]
            print(wordToGuess)
            wordToGuessList = list(wordToGuess)
            for x in wordToGuess:
                if unknownWord == "":
                    unknownWord = "_"
                else:
                    unknownWord = unknownWord + "_"
            while not gameWon:
                print(unknownWord)
                if not hangman == "":
                    print(hangman)
                user_input = input(">")
                usedUsedLetter = False
                for x in allowedkeys:
                    if user_input == x:
                        if not usedalphabet == []:
                            for y in usedalphabet:
                                if user_input == y:
                                    usedUsedLetter = True
                                    print(y + " was already used!")
                                    if hangmannum + 1 == 7:
                                        print("Game is over!")
                                        print("The word was ", wordToGuess)
                                        gameWon = True
                                        print("Do you want to play by" + "\u0332".join(
                                            " y") + "ourself" " or with" + "\u0332".join(" o") + "thers?")
                                    hangmannum = hangmannum + 1
                                    hangman = hangmanword(hangmannum)
                                    break
                                else:
                                    continue
                            if not usedUsedLetter:
                                try:
                                    wordToGuess.index(user_input)
                                except ValueError:
                                    usedalphabet.append(user_input)
                                    print(user_input + " is incorrect")
                                    if hangmannum + 1 == 7:
                                        print("Game is over!")
                                        print("The word was ", wordToGuess)
                                        gameWon = True
                                        print("Do you want to play by" + "\u0332".join(
                                            " y") + "ourself" " or with" + "\u0332".join(" o") + "thers?")
                                    hangmannum = hangmannum + 1
                                    hangman = hangmanword(hangmannum)
                                    continue
                                usedalphabet.append(user_input.lower())
                                print(usedalphabet)
                                unknownWordList = list(unknownWord)
                                wtgl = [pos for pos, char in enumerate(wordToGuess) if char == user_input]
                                i = 0
                                for k in wordToGuessList:
                                    if user_input == k:
                                        if len(wtgl) > 1:
                                            while i < len(wtgl):
                                                unknownWordList[wtgl[i]] = k
                                                i = i + 1
                                        else:
                                            unknownWordList[wtgl[0]] = k
                                unknownWord = "".join(unknownWordList)
                                if unknownWord == wordToGuess:
                                    gameWon = True
                                    print("You won!")
                                    user_input = input("Do you want to play again?\n>").lower()
                                    if user_input == "yes" or user_input == "y":
                                        print("Do you want to play by" + "\u0332".join(
                                            " y") + "ourself" " or with" + "\u0332".join(" o") + "thers?")
                                        break
                                    else:
                                        sys.exit(0)

                        else:
                            try:
                                wordToGuess.index(user_input)
                            except ValueError:
                                usedalphabet.append(user_input)
                                print(user_input + " is incorrect")
                                if hangmannum + 1 == 7:
                                    print("Game is over!")
                                    print("The word was ", wordToGuess)
                                    gameWon = True
                                    print("Do you want to play by" + "\u0332".join(
                                        " y") + "ourself" " or with" + "\u0332".join(" o") + "thers?")
                                hangmannum = hangmannum + 1
                                hangman = hangmanword(hangmannum)
                                continue
                            usedalphabet.append(user_input.lower())
                            print(usedalphabet)
                            unknownWordList = list(unknownWord)
                            wtgl = [pos for pos, char in enumerate(wordToGuess) if char == user_input]
                            i = 0
                            for k in wordToGuessList:
                                if user_input == k:
                                    if len(wtgl) > 1:
                                        while i < len(wtgl):
                                            unknownWordList[wtgl[i]] = k
                                            i = i + 1
                                    else:
                                        unknownWordList[wtgl[0]] = k
                            unknownWord = "".join(unknownWordList)
                            if unknownWord == wordToGuess:
                                gameWon = True
                                print("You won!")
                                user_input = input("Do you want to play again?\n>").lower()
                                if user_input == "yes" or user_input == "y":
                                    print("Do you want to play by" + "\u0332".join(
                                        " y") + "ourself" " or with" + "\u0332".join(" o") + "thers?")
                                    break
                                else:
                                    sys.exit(0)

        else:
            pass


def hangmanword(num):
    hangmandict = {
        1: "h",
        2: "ha",
        3: "han",
        4: "hang",
        5: "hangm",
        6: "hangma",
        7: "hangman"
    }
    if num == 0 or num < 0:
        pass
    elif num > 7:
        pass
    else:
        return hangmandict[num]


game = game()
game
