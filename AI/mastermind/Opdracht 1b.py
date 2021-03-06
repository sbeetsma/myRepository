""" Opdracht 1b """

### (kleine) veranderingen ###

# output van console veranderd in code van 'getal' naar 'letter' bij guess = input(...)
# ongebruikte import weg (sorry als je die nog nodig had)

### feedback ###

# Werking van de code
#   shapiroAI en worstcaseAI werken goed een suggestie om ook de feedback van z/w pinnen te tonen in de console.
#   human werkt bijna goed, wanneer ik de geheime code goed invoer krijg ik wel de juiste feedback (4 zwart) maar de wincondition werkt nog niet goed dus het spel blijft doorgaan
#   ook exit de code zonder lose berichtje.
#   Ik kan een foutieve code invullen getallen of meerdere letters. Een oplossing hiervoor zou een valideerfunctie maken die de input controleert en eventueel reject.
#   In het begin was me onduidelijk hoe ik de poging voor de geheime code moest inputten, zou dit handiger zijn in 1 input?

# Efficientie/Indeling functies
#   een suggestie zou zijn om de gameloop (textterminal) zo te coderen dat je de variablen als player, human, number_of_colors etc.
#       kan meegeven als parameters en deze variablen te bepalen in een aparte functie of een standaard parameter waarde zoals je
#           op die manier kan je een nieuw algoritme implementeren/ spel starten met andere spelregels zonder iets aan de gameloop te veranderen.
#   sommige functies werken goed maar hebben ongebruikte parameters.


# Commentaar
# Docstrings zien er goed uit, het andere commentaar zou ik de """""" veranderen in # maar ik weet niet zeker wat daar de normen daar van zijn in python.
# Ookal kan ik ( nu nog ) de code goed volgen staat er nog weinig commentaar in de functies zelf, bijv een korte uitleg bij een while/for loop of if statement zou handig zijn.


from random import randrange
import string
import time


def textterminal():
    """ Deze functie zorgt ervoor dat de gebruiker text kan zien dat een spelbord moet voorstellen. Je kunt ook het
    totaal aantal kleuren bepalen en hoeveel kleuren je moet gokken. """

    player = input("Voer in de speler 'human' of 'shapiroAI' of 'worstcaseAI': ")
    if player != 'human' and player != "shapiroAI" and player != "worstcaseAI":
        print("Verkeerde naam, standaard 'human' ingevoerd")
        player = "human"
    # player = "onestepaheadAI"
    number_of_colors = 6
    length_of_guess = 4
    number_of_tries = 8

    secret_code = generaterandomcode(number_of_colors, length_of_guess)
    print("(dit hoort de speler niet te zien) De geheime code is: " + str(secret_code))
    time.sleep(1
               )

    answerguessed = False

    """ Dit deel is gemaakt voor de speler. Dit stuk zorgt ervoor dat de speler het spel kan spelen"""
    while answerguessed == False and number_of_tries > 0 and player == "human":
        try:
            all_guesses = []
            for i in range(length_of_guess):
                guess = input("Voer gok getal " + str(i + 1) + " in: ")
                all_guesses.append(guess)
        except ValueError:
            print("ValueError")
        feedback = checkAnswer(all_guesses, secret_code)
        if feedback == True:
            answerguessed = True
            print("Correct! Je hebt gewonnen")
        else:
            number_of_tries -= 1
            print("Je hebt nog " + str(number_of_tries) + " pogingen.")
            print(feedback)

    """ Dit deel is gemaakt voor de shapiroAI. Het zorgt ervoor dat de functies die nodig zijn worden aangeroepen """
    if player == "shapiroAI":
        shapiroAI(number_of_colors, length_of_guess, number_of_tries, secret_code)

    if player == "worstcaseAI":
        worstcaseAI(number_of_colors, length_of_guess, number_of_tries, secret_code)


def generaterandomcode(number_of_colors=6, length_of_guess=4):
    """ Genereer een lijst met input number_of_colors en de functie "generatecombinationslist".
    Returnt een random nummer in de gemaakte lijst"""
    number_of_colors = generatecombinationslist(number_of_colors)
    return number_of_colors[randrange(0, len(number_of_colors))]


def generatecombinationslist(number_of_colors=6):
    """ Genereer alle mogelijke combinaties. Returnt een lijst met alle combinaties. Het aantal kleuren kan veranderen
    maar de code kan alleen 4 characters lang zijn"""
    characters = []
    for i in range(number_of_colors):
        characters.append(string.ascii_lowercase[i])
    all_combinations = []
    for i in range(number_of_colors):
        first = characters[i]
        for i in range(number_of_colors):
            second = characters[i]
            for i in range(number_of_colors):
                third = characters[i]
                for i in range(number_of_colors):
                    fourth = characters[i]
                    all_combinations.append([first, second, third, fourth])
    return all_combinations


def generatepossiblecombinationslist(lst=None, guess=None, feedback=None):
    """ Bekijkt of dezelfde feedback uit een mogelijke antwoord en een gok komt. Als de feedback hetzelfde is wordt hij
    toegevoegd aan een lijst. Returnt een lijst met mogelijke antwoorden. """
    list_copy = []
    for possibleanswer in lst:
        if str(checkAnswer(guess, possibleanswer)) == str(feedback):
            list_copy.append(possibleanswer)
    return list_copy


def checkAnswer(guessedanswer, correctanswer):
    """ Returnt een dictionary. De dictionary bevat feedback over hoeveel witte en zwarte pinnen er zijn. """
    my_dict = {"zwart":0,"wit":0}
    correctanswer_copy = list(correctanswer).copy()
    for i in range(len(guessedanswer)):
        if guessedanswer[i] == correctanswer[i]:
            my_dict["zwart"] += 1
            correctanswer_copy.remove(guessedanswer[i])
    for i in range(len(guessedanswer)):
        for index in range(len(correctanswer_copy)):
            if index >= len(correctanswer_copy):
                break
            if guessedanswer[i] in correctanswer_copy:
                my_dict["wit"] += 1
                correctanswer_copy.remove(guessedanswer[i])
                break
    return my_dict


def shapiroAI(number_of_colors, length_of_guess, number_of_tries, secret_code):
    """ Maakt keuzes gebaseerd op de strategie van shapiro. Er wordt een lijst gemaakt met mogelijk antwoorden. Daaruit
    wordt er een willekeurig gekozen. Daarna worden keuzes weggehaald gebaseerd op de feedback met
    generatepossiblecombinationslist """
    possiblelist = generatecombinationslist(number_of_colors)
    answerguessed = False
    while answerguessed == False and number_of_tries > 0:
        guess = possiblelist[randrange(0, len(possiblelist))]
        print("De computer gokt: " + str(guess))
        feedback = checkAnswer(guess, secret_code)
        if guess == secret_code:
            answerguessed = True
            print("Correct! Computer heeft gewonnen")
        else:
            possiblelist = generatepossiblecombinationslist(possiblelist, guess, feedback)
            number_of_tries -= 1
        if number_of_tries == 0:
            print("Computer heeft verloren!")


def worstcaseAI(number_of_colors, length_of_guess, number_of_tries, secret_code):
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op een stap vooruit kijken. """
    possiblefeedback = []
    zwartindex = 0
    witindex = 0

    # Genereert een lijst met mogelijke feedback voor 4 mogelijke antwoorden
    while True:
        possiblefeedback.append({"zwart":zwartindex,"wit":witindex})
        witindex += 1
        if witindex + zwartindex > 4:
            zwartindex += 1
            witindex = 0
        if zwartindex == 3:
            possiblefeedback.append({"zwart":3,"wit":0})
            possiblefeedback.append({"zwart":4,"wit":0})
            break

    possiblelist = generatecombinationslist(number_of_colors)
    answerguessed = False
    firstguess = True
    while answerguessed == False and number_of_tries > 0:
        index = 0
        my_dict = {}
        previousworstcaseoutcome = []
        firsttime = True

        if firstguess == False:
            for possibleanswer in possiblelist:
                index += 1

                currentworstcaseoutcome = []
                for feedback in possiblefeedback:

                    outcome = generatepossiblecombinationslist(possiblelist, possibleanswer, feedback)
                    if len(outcome) > len(currentworstcaseoutcome):
                        currentworstcaseoutcome = outcome
                        if firsttime == True:
                            previousworstcaseoutcome = currentworstcaseoutcome
                            guess = possibleanswer
                            firsttime = False
                        my_dict[str(possibleanswer)] = len(currentworstcaseoutcome)
                        # print(str(possibleanswer))
                        # print(len(currentworstcaseoutcome))
                if len(currentworstcaseoutcome) < len(previousworstcaseoutcome):
                    previousworstcaseoutcome = currentworstcaseoutcome
                    guess = possibleanswer
            print("Computer deed: " + str(index) + " loops")

            # print(len(currentworstcaseoutcome))
            # print(possibleanswer)
            # print(my_dict)
            # time.sleep(1)

            minimum = min(my_dict.values())
            best_guesses = []

            for answer, worstcase in my_dict.items():
                if worstcase == minimum:
                    best_guesses.append(answer)

        if firstguess == True:
            guess = ['a', 'a', 'b', 'b']
            print("Computer gokt: " + str(guess))
            firstguess = False
        else:
            print("Computer gokt: " + str(best_guesses[randrange(0, len(best_guesses))]))
        if guess == secret_code:
            answerguessed = True
            print("Correct! Computer heeft gewonnen")
        else:
            feedback = checkAnswer(guess, secret_code)
            possiblelist = generatepossiblecombinationslist(possiblelist, guess, feedback)
            number_of_tries -= 1
        if number_of_tries == 0:
            print("Computer heeft verloren!")

        # if guess == secret_code:
        #     answerguessed = True
        #     print("Correct! Computer heeft gewonnen")
        # elif number_of_tries == 0:
        #     print("Computer heeft verloren!")




def eenkleurAI():
    """ Deze functie zorgt ervoor dat er een tegenstander is waar de gebruiker tegen kan spelen. De manier waarop
    de AI keuzes maakt, is gebaseerd op een kleur kiezen. Daarna gebaseerd op de feedback worden andere keuzes gemaakt
    """
    pass


textterminal()
# print(generatecombinationslist(5, 6))
# print(generaterandomcode(6, 7))
