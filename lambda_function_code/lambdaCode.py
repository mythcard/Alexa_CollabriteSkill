"""
The code template is obtained from coding Dojo and modified according to our requirement
"""

from __future__ import print_function
import random


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # Dispatch to your skill's launch
    return get_welcome_response(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "onlaunch":
        return get_welcome_response(session)
    #elif intent_name == "rules":
    #    return giveRuleDetails(session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(session)
    elif intent_name == "getNumberFromUserIntent":
        return getNumberFromUser(intent_request,session)
    elif intent_name == "AMAZON.YesIntent":
        return performNextStepAfterYes(session)
    elif intent_name == "AMAZON.NoIntent":
        return performNextStepAfterNo(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Functions that control the skill's behavior ------------------

def getBestChoice(finalCounter):
    return 11 - (finalCounter%11)

def getUserChoice():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return random.choice(lst)

def getBegNoFromInitialStrategy(playerCounter, randNo):
    ## 3 startegies I have thought for now
    ## one random number choice, 4 out of 10 times choose this startegy
    ## two mock the number choice user chooses, 3 out of 10 times choose this startegy
    ## three choose tables, some random random table, 3 out of ten times choose this strategy
    if(randNo > 0 and randNo < 5):
        return getUserChoice()
    elif(randNo > 4 and randNo < 8):
        return playerCounter
    else:
        return getUserChoice()    ## tables still need implementation details

## this is to infuse non deterministic component to the game
def selectUserNumber(finalCounter, playerCounter,inflectionPoint, userStrategyNo):
    ## 2 stages of the game

    if(finalCounter >= 0 and finalCounter <= inflectionPoint):
        currentChoice = getBegNoFromInitialStrategy(playerCounter, userStrategyNo)
        print("Current Choice emanating out of the normal flow: " + str(currentChoice))
    else:
        currentChoice = getBestChoice(finalCounter)
        print("Current Choice emanating out of the brain: " + str(currentChoice))

    if(currentChoice > 0 and currentChoice < 11):
        return currentChoice
    else:
        return getUserChoice()

def getConcernCommand():
    wiseSynonyms = ["wisely","carefully","warily","prudently","with caution","with all your wit","with all your combined acumen"]
    cmd =  ". It is your turn now, Choose a number between 1 to 10 and choose it "+random.choice(wiseSynonyms)+" to push me to 100. "
    return cmd

def getNormalCommand():
    lst = [1, 2, 3]
    argument =  random.choice(lst)
    switcher = {
        1: ". Your turn to push.",
        2: ". Your turn.",
        3: ". Your chance to play, go ahead and choose your number.",
    }
    return switcher.get(argument, "Your turn.")

def getIntrPlayerCommand(finalCounter, inflectionPoint):
    if(finalCounter < 19 or finalCounter > inflectionPoint):
        return getConcernCommand()
    else:
        return getNormalCommand()


def get_welcome_response(session):
    print("SessionId: " + session['sessionId'])

    ## first select the partition where first and second strategy work
    inflectionPoint = int(random.gauss(75, 10))
    while(inflectionPoint < 50 or inflectionPoint > 90):
        inflectionPoint = int(random.gauss(75, 10))
    userStrategyNo = getUserChoice()
    stepNo = 0

    if('userId' in session['user'].keys()):
        print("ENCODE USERID:"+session['user']['userId'])
    if('consentToken' in session['user'].keys()):
        print("ENCODE CONSENTTOKEN:" + session['user']['consentToken'])

    print("Inflection point in this game: " + str(inflectionPoint))
    print("ENCODE INFLECTION:"+ str(inflectionPoint))
    print("Strategy chosen: " + str(userStrategyNo))
    print("ENCODE STRATEGYCODE:" + str(userStrategyNo))

    ## set the session attributes here right at the begining of the game
    session_attributes = {"sessionGameState": 'begining', "finalCounter": 0, "playerCounter": 0, "userCounter": 0, "inflectionPoint": inflectionPoint, "userStrategyNo":userStrategyNo, "stepNo": stepNo}
    card_title = "Welcome"


    speech_output = "Welcome to the Push One to Hundred arena. This is an awesome place to test or sharpen your analytical skill. So let us get started. The rules of the game are simple. There is a counter which is at zero for now. At every turn each player gets to choose a number between one and ten. And the counter gets incremented by the number the player chooses. The objective of the player, is to push the opponent to tell 100. The player who forces the opponent to 100, wins. So let us start push one to hundred. Please say Yes to start, and no to forfeit"
    #speech_output = "Its testing you douche bag. Please say Yes to start, and no to forfeit"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with the same text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def performNextStepAfterNo(session):
    should_end_session = False

    # assign the necessary persistent varaibles from previous section of same session
    sessionGameState = session['attributes']['sessionGameState']
    finalCounter = session['attributes']['finalCounter']
    playerCounter = session['attributes']['playerCounter']
    userCounter = session['attributes']['userCounter']
    inflectionPoint =  session['attributes']['inflectionPoint']
    userStrategyNo = session['attributes']['userStrategyNo']
    stepNo = session['attributes']['stepNo']


    if (sessionGameState == 'begining'):
        return handle_session_end_request()
    elif (sessionGameState == 'AskUserWhetherNumYesNo'):
        speech_output = "The counter is currently at "+str(finalCounter)+". Choose a number between 1 to 10 to push me to 100."

    session_attributes = {"sessionGameState": sessionGameState, "finalCounter": finalCounter, "playerCounter": 0,
                          "userCounter": userCounter, "inflectionPoint": inflectionPoint, "userStrategyNo":userStrategyNo,"stepNo": stepNo}
    card_title = "In No"
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def performNextStepAfterYes(session):
    speech_output = "Oh My God. This is a dark side, where we should not enter. I am sorry I need to end the game, and notify the Force."
    should_end_session = True

    # assign the necessary persistent varaibles from previous section of same session
    sessionGameState = session['attributes']['sessionGameState']
    finalCounter = session['attributes']['finalCounter']
    playerCounter = session['attributes']['playerCounter']
    userCounter = session['attributes']['userCounter']
    inflectionPoint = session['attributes']['inflectionPoint']
    userStrategyNo = session['attributes']['userStrategyNo']
    stepNo = session['attributes']['stepNo']


    if (sessionGameState == 'begining' and finalCounter >= 0 and finalCounter < 100):
        should_end_session = False
        userCounter = getUserChoice()
        stepNo += 1
        print("User chose number: " + str(userCounter) + " at step: "+str(stepNo))
        print("ENCODE USERCHOSE:" + str(userCounter)+" STEP:"+str(stepNo))

        finalCounter += userCounter

        print("Final counter right now: " + str(finalCounter)+ " at step: "+str(stepNo))
        print("ENCODE FINCNT:" + str(finalCounter)+ " at step: "+str(stepNo))

        sessionGameState = "askUserForNumber"
        speech_output = "I played, " + str(userCounter) + ". The current counter now, is set to " + str(
            finalCounter) + ". It is your turn now, Choose a number between 1 to 10 and choose it wisely to push me to 100."

    elif(sessionGameState == 'AskUserWhetherNumYesNo'):
        should_end_session = False
        stepNo += 1
        print("Player chose number: " + str(playerCounter) + " at step: "+str(stepNo))
        print("ENCODE PLAYERCHOSE:" + str(playerCounter) + " STEP:"+str(stepNo))

        finalCounter += int(playerCounter)

        print("Final counter right now: " + str(finalCounter) + " at step: "+str(stepNo))
        print("ENCODE FINCNT:" + str(finalCounter) + " at step: "+str(stepNo))

        if(finalCounter >= 99):
            print("State before game ends: " + sessionGameState)
            speech_output = "The Game just ended. You are great at this. Challenge me another time and I shall show you, my prowess. Before I shut down, wishing you a Happy Halloween!"
            should_end_session = True
        else:
            sessionGameState = 'userTurn'


        if(finalCounter > 0 and finalCounter < 100 and sessionGameState == 'userTurn'):
            userCounter = selectUserNumber(finalCounter, playerCounter,inflectionPoint,userStrategyNo)

            stepNo += 1
            print("User chose number: " + str(userCounter) + " at step: " + str(stepNo))
            print("ENCODE USERCHOSE:" + str(userCounter) + " STEP:" + str(stepNo))

            finalCounter += userCounter

            print("Final counter right now: " + str(finalCounter) + " at step: " + str(stepNo))
            print("ENCODE FINCNT:" + str(finalCounter) + " at step: " + str(stepNo))

            if (finalCounter >= 100):
                speech_output = "The Game just ended. You are great at this. Challenge me another time and I shall show you, my prowess. Before I shut down, wishing you a Happy Halloween!"
                should_end_session = True
            elif(finalCounter == 99):
                speech_output = "I played, " + str(userCounter) + ". The current counter now, is set to " + str(
                    finalCounter)+". Since you have no other play, the Game just ended. I win. Practice well and come back another time to challenge me. Before I shut down, wishing you a Happy Halloween!"
                should_end_session = True
            else:
                sessionGameState = "askUserForNumber"
                speech_output = "I played, " + str(userCounter) + ". The current counter now, is set to " + str(
                    finalCounter)
                speech_output = speech_output + getIntrPlayerCommand(finalCounter, inflectionPoint)

    elif (sessionGameState == 'askUserForNumber'):
        should_end_session = False
        sessionGameState = "askUserForNumber"
        speech_output = "I played, " + str(userCounter) + ". The current counter now, is set to " + str(
            finalCounter)
        speech_output = speech_output + getIntrPlayerCommand(finalCounter, inflectionPoint)

    session_attributes = {"sessionGameState": sessionGameState, "finalCounter": finalCounter, "playerCounter": 0,
                          "userCounter": userCounter, "inflectionPoint": inflectionPoint, "userStrategyNo":userStrategyNo, "stepNo": stepNo}
    card_title = "In Yes"
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response(session):
    # assign the necessary persistent varaibles from previous section of same session
    sessionGameState = session['attributes']['sessionGameState']
    finalCounter = session['attributes']['finalCounter']
    playerCounter = session['attributes']['playerCounter']
    userCounter = session['attributes']['userCounter']
    inflectionPoint = session['attributes']['inflectionPoint']
    userStrategyNo = session['attributes']['userStrategyNo']
    stepNo = session['attributes']['stepNo']

    #session_attributes = {}

    session_attributes = {"sessionGameState": sessionGameState, "finalCounter": finalCounter, "playerCounter": playerCounter,
                          "userCounter": userCounter, "inflectionPoint": inflectionPoint,
                          "userStrategyNo": userStrategyNo, "stepNo": stepNo}
    card_title = "Help"
    speech_output = "This is Push One to Hundred arena. This is an awesome place to test or sharpen your analytical skill. The rules of the game are simple. This is a turn based game. There is a counter, which is set to a certain number, between 1 and 99, at all times. At each turn, each player gets to choose a number between one and ten. And the counter gets incremented by the number, the player chooses. The objective of the player, is to push the opponent to tell 100. The player who forces the opponent to 100, wins. Please say Yes to resume, or just say Help to hear back the details."

    reprompt_text = speech_output
    should_end_session = False
    #print("In here at help last step")
    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



def getNumberFromUser(intent_request,session):
    # assign the necessary persistent varaibles from previous section of same session
    sessionGameState = session['attributes']['sessionGameState']
    finalCounter = session['attributes']['finalCounter']
    playerCounter = session['attributes']['playerCounter']
    userCounter = session['attributes']['userCounter']
    inflectionPoint = session['attributes']['inflectionPoint']
    userStrategyNo = session['attributes']['userStrategyNo']
    stepNo = session['attributes']['stepNo']

    card_title = "Your turn to Push a number between 1 - 10."

    session_attributes = {"sessionGameState": sessionGameState, "finalCounter": finalCounter,
                          "playerCounter": playerCounter,
                          "userCounter": userCounter, "inflectionPoint": inflectionPoint,
                          "userStrategyNo": userStrategyNo, "stepNo": stepNo}

    try:
        playerCounter = intent_request["intent"]["slots"]["num"]["value"]


        sessionGameState = 'AskUserWhetherNumYesNo'


        if(int(playerCounter) > 10):
            speech_output = "The number that you have selected is: "+ str(playerCounter)+ " which is greater than 10. Please choose a number between 1 and 10"
        elif(int(playerCounter > 0 and int(playerCounter) < 11) and (finalCounter + int(playerCounter)) <= 99):
            speech_output = "The number that you have selected is: "+ str(playerCounter)+ ". If confirmed, the counter shall be set to "+ str(finalCounter+ int(playerCounter))+". Please say Yes to confirm, or No, to deny."
        elif (int(playerCounter > 0 and int(playerCounter) < 11 and  (finalCounter + int(playerCounter)) > 100)):
            speech_output = "The number that you have selected is: " + str(
                playerCounter) + ". If confirmed, the counter shall be set to " + str(
                finalCounter + int(playerCounter)) + ". I just want to be sure before continuing further. Please say Yes to confirm, or No, to deny."
        else:
            speech_output = "There seems to be some problem. I request you to ensure you give me only numbers between one to ten, because that is all, that I can digest."

    except KeyError:
        speech_output = "There seems to be some problem. I request you to ensure you give me only numbers between one to ten, because that is all, that I can digest."
    except ValueError:
        speech_output = "There seems to be some problem. I request you to ensure you give me only numbers between one to ten, because that is all, that I can digest."

    session_attributes = {"sessionGameState": sessionGameState, "finalCounter": finalCounter,
                          "playerCounter": playerCounter,
                          "userCounter": userCounter, "inflectionPoint": inflectionPoint,
                          "userStrategyNo": userStrategyNo, "stepNo": stepNo}

    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing Push One To Hundred. Hope it was both entertaining and educational."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':   output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
