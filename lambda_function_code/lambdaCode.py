"""
The code template is obtained from coding Dojo and modified according to our requirement
"""

from __future__ import print_function
import random

dict = {"123":"Jennifer" , "456":"Rob" , "789": "Tiffany"}


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
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(session)
    elif intent_name == "getNumberFromUserIntent":
        return getNumberFromUser(intent_request,session)
    elif intent_name == "AMAZON.YesIntent":
        return yesFuncName(session)
    elif intent_name == "AMAZON.NoIntent":
        return noFuncName(session)
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

def get_welcome_response(session):
    print("SessionId: " + session['sessionId'])

    ## set the session attributes here right at the begining of the game
    card_title = "Welcome"


    speech_output = "Welcome to Collabrite test portal. It is our privlege to be of your service today! Please state your 3 digit pin to authenticate. Please state the numbers one after another followed by the prompt. Your first number: "

    session_attributes = {"currentNumber": "-1"}

    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getNumberFromUser(intent_request,session):
    card_title = "Enter 3 digit pin"
    speech_output = "Your next number"

    try:
        currentNumber = session['attributes']['currentNumber']
        pin = intent_request["intent"]["slots"]["num"]["value"]
            #pin = intent_request["intent"]["slots"]["num"]["value"]

        if(currentNumber == '-1'):
            currentNumber = str(pin)
        else:
            currentNumber = currentNumber + str(pin)

        if(len(currentNumber) < 3):
            speech_output = "The pin you entered is "+ str(pin) +" your next number:"
        elif(len(currentNumber) == 3):
            if currentNumber in dict.keys():
                speech_output = "Authentication successful for: "+dict[currentNumber]

            else:
                speech_output = "Authentication failure."

    except KeyError:
        currentNumber = "-1"
        speech_output = "Somethings seems strange, I am bidding good bye!"
        handle_session_end_request()
    except ValueError:
        speech_output = "Somethings seems strange, I am bidding good bye!"
        handle_session_end_request()

    reprompt_text = speech_output

    if(len(currentNumber) == 3):
        should_end_session = True
    else:
        should_end_session = False

    session_attributes = {"currentNumber": currentNumber}

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for visiting us. We constantly strive to redefine what is best for you!"
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