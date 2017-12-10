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

    print("Let us see from begining = "+ event['request']['type'])

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
    print("Let us see what is the intent name = " + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "onlaunch":
        return get_welcome_response(session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response(session)
    elif intent_name == "getNumberFromUserIntent":
        return getNumberFromUser(intent_request,session)
    elif intent_name == "planIntent":
        return getPlanResponse(intent_request,session)
    elif intent_name == "planIntentJustMe":
        print("In the right place " + intent_name)
        return getPlanJustMeResponse(session)
    elif intent_name == "AMAZON.YesIntent":
        return yesFuncName(session)
    elif intent_name == "AMAZON.NoIntent":
        return noFuncName(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        print("In the wrong place = " + intent_name)
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


    speech_output = "Welcome to Blue Cross Blue Shield of Illinois Health Care Coverage portal. It is our privlege to be of your service today! Please state your 3 digit pin to authenticate. Please state the numbers one after another followed by the prompt. Your first number: "

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
        print("currentNumber=" + currentNumber)
        pin = intent_request["intent"]["slots"]["num"]["value"]
        print("pin=" + pin)
            #pin = intent_request["intent"]["slots"]["num"]["value"]

        if(currentNumber == '-1'):
            currentNumber = str(pin)
        else:
            currentNumber = currentNumber + str(pin)

        if(len(currentNumber) < 3):
            speech_output = "The pin you entered is "+ str(pin) +" your next number:"
        elif(len(currentNumber) == 3):
            if currentNumber in dict.keys():
                speech_output = "Hi "+dict[currentNumber]
                speech_output = speech_output+". Understanding your health care coverage can be confusing. This is why I would like to explain how a plan works. And when we are done, you will be able to get a personalized video summary of your Blue Cross Blue Shield of Illinois Health Care Plan. Please state, who is currently covered by your plan?"

            else:
                speech_output = "Authentication failure."

    except KeyError:
        currentNumber = "-1"
        speech_output = "Somethings seems strange in KeyError, I am bidding good bye!"
        handle_session_end_request()
    except ValueError:
        speech_output = "Somethings seems strange in ValueError, I am bidding good bye!"
        handle_session_end_request()

    reprompt_text = speech_output

    should_end_session = False

    session_attributes = {"currentNumber": currentNumber}

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def getPlanResponse(intent_request,session):

    speech_output = "You and your family, got it. Let us break down your plan name. Your plan is known as a health maintenance organization, or HMO. And by Health Maintenance Organization, I just mean a team of doctors and hospitals that help keep your family healthy. Do you know what a Network is?"

    reprompt_text = speech_output
    card_title = "Plan Just Me Response"

    sessionState = "network"

    session_attributes = {"quesPos": sessionState}

    should_end_session = False

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def getPlanJustMeResponse(session):
    speech_output = "You and your family, got it. Let us break down your plan name. Your plan is known as a health maintenance organization, or HMO. And by Health Maintenance Organization, I just mean a team of doctors and hospitals that help keep your family healthy. Do you know what a Network is?"
    #speech_output = "Let us see if this works"

    reprompt_text = speech_output
    card_title = "Plan Just Me Response"

    sessionState = "network"

    session_attributes = {"quesPos": sessionState}

    should_end_session = False
    print("Am I coming here?? ")
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def yesFuncName(session):
    should_end_session = False

    speech_output = "Hello"

    # assign the necessary persistent varaibles from previous section of same session
    sessionGameState = session['attributes']['quesPos']

    if (sessionGameState == 'network'):
        speech_output = "Ok. Do you have a primary care physician?"
    elif (sessionGameState == 'PCP'):
        speech_output = "Well, the most important part of an HMO is choosing a doctor to help manage all of your in network health care. Your primary care physician or PCP is kind of like your medical personal assistant who will give you all your routine care."
        handle_session_end_request()


    session_attributes = {"quesPos": "PCP"}
    card_title = "In No"
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def noFuncName(session):
    should_end_session = False

    speech_output = "Hello"

    # assign the necessary persistent varaibles from previous section of same session
    sessionGameState = session['attributes']['quesPos']

    if (sessionGameState == 'network'):
        speech_output = "Ok. As a quick reminder with an HMO, when you visit specific doctors that is called your network. If you go out of network, it may be that, you may have to pay more for the care. Do you have a primary care physician?"
    elif (sessionGameState == 'PCP'):
        speech_output = "Well, the most important part of an HMO is choosing a doctor to help manage all of your in network health care. Your primary care physician or PCP is kind of like your medical personal assistant who will give you all your routine care."
        handle_session_end_request()


    session_attributes = {"quesPos": "PCP"}
    card_title = "In No"
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response(session):
    card_title = "Help"
    speech_output = "Hello! This is help section still under development."

    reprompt_text = speech_output
    should_end_session = False
    #print("In here at help last step")
    return build_response({},
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Next time you are not feeling good, keep this in mind. The average wait time for a non emergency in the ER is 4 hours and 17 minutes.  For primary care physicians, it is about 24 minutes, and if you head to your nearest in network Urgent Care center, you are looking at an average wait of 11 to 20 minutes. You should always go to an ER, if you think you are having a real emergency, or that delaying care could put your health at risk. But if it is not an emergency, you can save yourself time, by heading to an in network Urgent Care center, a local retail clinic, or to your Primary Care Physician. When we are done here, I can help you pick a Primary Care Physician, set up an appointment, at an IN network Urgent Care center near you, or send you a personalized video, that summarizes your Blue Cross Blue Shield of Illinois health care coverage."
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