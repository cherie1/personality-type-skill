import logging
import re
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

questions = [
['When you are by yourself: A) You tend to get bored. Or B) You easily find ways to entertain yourself', 'e', 'i'],
['On the weekends you usually prefer to: A) Plan outings ahead of time. Or B) Leave room for spontaneous outings.', 'j', 'p'],
['You do your best work in: A) A calm and quiet environment. Or B) A bustling and lively environment.','i', 'e'],
['Your working style usually involves: A) Diving right in. Or B) Making a list of tasks and checking them off as you go. ','p','j'],
['In your day to day activities you prefer to focus on: A) The here and now. Or B) The future and possibilities. ', 's', 'n'],
['When you are thinking about something, do you have a tendency to space out and become less aware of your surroundings? A) Yes. Or B) No.','n','s'],
['When you are attempting to understand someone: A) You try to understand their reasoning and thought process. Or B) You try to empathize with their experiences.','t','f'],
['Do you prefer being asked to do tasks that: A) Have an established correct method that will work every time. Or B) Have multiple possible methods that are open to experimentation.', 'j', 'p'],
['While having conversations with people you tend to be more: A) Outgoing. Or B) Reserved.','do','zc'],
['When it comes to your personal life you are usually: A) A private person. Or B) An open book.','c','o'],
['When you disagree with someone you usually: A) Come right out and say it. Or B) Keep it to yourself to keep the peace.', 'd', 'z'],
['You get more energy from: A) Being involved in lots of stimulating events and activities. Or B) Relaxing by yourself or with a small group of friends.', 'e', 'i'],
['When you are working on a project you like to focus more on: A) The details of the implementation. Or B) The big picture.','sc','nd'],
['Do you enjoy thinking about theoretical concepts like philosophy? A) Yes - you enjoy entertaining abstract ideas and applying them to real life. Or B) No - you prefer to spend time thinking about things that have a direct application in your life.', 'n', 's'],
['When it comes to rules and authority: A) You often question them. Or B) You trust that those in authority know best.','dc','oz'],
['When a friend comes to you with a problem your first impulse is to: A) Try to come up with a solution. Or B) Listen and empathize.','t','f'],
['Your ideal weekend involves: A) Large group activities. Or B) Activities with a close group of friends.', 'e', 'i'],
['As a rule, you tend to be more: A) People-oriented. Or B) Task-oriented.', 'oz', 'dc'], 
['Being with a large group of people makes you feel A) Drained. Or B) Energized.','iz','eo'],
['You feel more comfortable when: A) There is a black and white answer. Or B) The answer is open to interpretation.','j','p']
]

total_questions = len(questions) 

fact_list = [
'Open floor plans in offices tend to be a better fit for extroverts. They love to work in an environment where they can see everyone and where there is always a chance to chat. On the other hand, introverts tend to dislike open floor plans because they can only do their best work in a quiet environment with few distractions.',
'The Kiersey temparament sorter groups personality types together based on specific two-letter pairings, creating four overall temperaments similar to the DISC profile. SJ types are called Guardians who value duty and responsibility. SP types are called Artisans who value action and spontaneity. NF types are called Idealists who value following their personal convictions. NT types are called Rationals who value pragmatic solutions. ',
'The four-letter personality type was developed as a result of the work of Carl Jung, who proposed that there were 4 basic psychological functions that determined a persons natural preferences and behaviors. Those functions are Thinking, Feeling, Sensing and Intuiting. They can be expressed in either an extroverted or introverted way. The function that a person uses most often determines whether they have a perceiving or judging attitude. ',
'Helen Fisher is a biological anthropologist who analyzed data from a dating website survey to try and find a pattern in romantic attraction. She concluded that most people fall into one of four temperament categories, each associated with a different brain chemical. She classified them as the Director (which is linked to testosterone), Negotiator (which is linked to estrogen), Builder (which is linked to serotonin), and Explorer (which is linked to dopamine). Her descriptions of these categories are fascinatingly similar to the DISC profile.',
'Contrary to popular belief, the introversion extroversion scale is not a measure of how shy or outgoing you are. It is an indicator of what types of activities drain you and which are energizing to you. Introverts may be extremely outgoing and social when they are in social situations. The difference is that they need more breaks from that social time than extroverts do. '
] 

total_facts = len(fact_list) 

description = {
'introversion': 'The first letter, I, means that you are more of an introvert than an extrovert. This means that socializing requires more energy for you and that you are energized by spending time alone. Therefore you spend more time doing solitary activities than activities that involve a group of people. ',
'extroversion': 'The first letter, E, means that you are more of an extrovert than an introvert. This means that socializing with people energizes you and therefore you are more likely to spend more time doing group activities than by yourself. ',
'sensing': 'The second letter, S, means that you tend to be detail-oriented and pay more attention to what you can see, taste, hear, smell and touch rather than relying on your intuition. ',
'intuition':'The second letter, N, means that you tend to pay more attention to the big picture than the individual details. You also rely on your intuition and trust your gut, rather than relying solely on input from your five senses. ',
'feeling': 'The third letter, F, means that you prefer to make decisions based on peoples feelings rather than pure logic. ',
'thinking':'The third letter, T, means that you prefer to make decisions based on logic rather than peoples feelings. ',
'judging': 'The fourth letter, J, means that you prefer to have things decided rather than open to interpretation. It is important to you to figure out the right answer or the right way to do things. You also tend to enjoy planning your activities ahead of time and having a set schedule. ',
'perceiving':'The fourth letter, P, means that you prefer to stay open to new information and options rather than having things decided. It is important to you to remain open to new possibilities. You also enjoy being spontaneous rather than planning out your day. ',
'steadiness': 'Steadiness is the most easygoing of the four temperaments and the most likely to be awarded Miss Congeniality. People with this type are even-tempered, dependable, cooperative, sincere, and service-oriented. However, it may be difficult for them to do some things that are necessary, like confronting people, being open to change, and being decisive. ',
'influence': 'Of the four temperamentws, Influence is the most likely to win a popularity contest. These types are energetic, talkative, optimistic and action-oriented. However, this type can suffer setbacks if they care too much about the approval of others or cannot stay interested in a task long enough to see it through. ',
'dominance': 'Of the four temperaments, people who score high on Dominance are the most likely to become skilled leaders. These types are direct, decisive, confident, results-oriented, and driven. However, this type can suffer setbacks if they do not take others feelings into account or if they focus on the big picture so much that they lose sight of small but important details. ',
'conscientiousness': 'Of the four temperaments, people who score high on Conscientiousness are the most likely to become experts in their field. These types are logical, analytical, reserved, and place great emphasis on quality. However, this type can suffer setbacks if they isolate themselves, become overcritical, or do not learn how to delegate. ',
'istj': 'The ISTJ is known as the Inspector - a highly dependable type that fulfills their responsibilities and values delivering accurate and high quality work. In order to take a practical, logical approach to their endeavors, they are able to make the tough decisions that other types avoid. Despite their dependability and good intentions, however, ISTJs can experience difficulty in understanding and responding to the emotional needs of others. However, ISTJs are loyal and reliable friends to those that they let inside their inner circle. Some famous ISTJs include George Washington, Warren Buffet, and Angela Merkel.',
'intj': 'The INTJ is known as the Mastermind - a highly effective strategist with an extremely independent mind. They are highly confident, decisive, and straightforward. This combination of high confidence and a tendency for bluntness can make INTJs come off as arrogant or argumentative. However, the INTJ has an extremely open mind and values truth and knowledge above all else. This makes them able to understand and be open to a variety of different perspectives and ideas. For the people that they allow within their inner circle, INTJs make for loyal and low-maintenance friends. Some famous INTJs include Ayn Rand, Elon Musk, Isaac Newton, and Mark Zuckergberg.',
'intp': 'The INTP is known as the Architect. These types are skilled at designing of all kinds of theoretical systems, including training, strategy, and new technology. They are highly open-minded and original. INTPs can sometimes get so caught up in logic and rationale that sometimes they forget to account for other people\'s feelings, which can lead others to think that they are insensitive or condescending. However, the INTP can be a playful friend or partner and is very loyal to people they love. Some famous INTPs include Bill Gates, Albert Einstein, Tina Fey, and James Madison.',
'infj': 'The INFJ is known as the Counselor. They have a strong desire to contribute to society in a meaningful way and always act in a way that relates to their personal values. They are determined, passionate, insightful, and altruistic. INFJs tend to be private individuals but when they find a friend or partner that is authentic and shares their ideals, they are able to open up and become supportive and dedicated friends. INFJs can also be perfectionistic, requiring a lot out of both themselves and others. This can lead them to be quite critical of others, but it also means that they are constantly striving to improve themselves and others. Some famous INFJs include Mahatma Gandhi, Mother Teresa, and Morgan Freeman.',
'infp': 'The INFP is known as the Healer. They focus much of their energy on an inner world dominated by intense feeling and deeply held ethics. They seek harmony and authenticity in their relationships with others, and they are very loyal to the people and causes that are important to them. This type is highly sensitive to criticism and may take challenges and criticisms personally. A study of university students found that the INFP type was the most common type among students studying fine arts. Some famous INFPs include Princess Diana, George Orwell, and Audrey Hepburn.',
'istp': 'The ISTP is known as the Crafter. They are highly adaptable, making them receptive to new information and approaches. They often excel in high-pressure and/or emergency situations. They enjoy exploring new things, so they can become bored with repetitiveness and routine. They can also be closet daredevils who gravitate toward fast-moving or risky hobbies. Famous ISTPs include Michael Jordan, Tom Cruise, and Scarlett Johansson.',
'isfj': 'The ISFJ is known as the Protector. ISFJs are interested in maintaining order and harmony in every aspect of their lives. They are steadfast and meticulous in handling their responsibilities. Although quiet, they are people-oriented and very observant. Their reluctance to open up to strangers can lead others to misread them as standoffish. Only among friends and family may this quiet type feel comfortable speaking freely. They are often described as thoughtful and trustworthy. Famous ISFJs include Kate Middleton, Jimmy Carter, Anne Hathaway, and Bruce Willis.',
'isfp': 'The ISFP is known as the Composer. ISFPs are peaceful, easygoing people who adopt a "live and let live" approach to life. They enjoy taking things at their own pace and tend to live in the moment. Although quiet, they are pleasant, considerate, caring, and devoted to the people in their lives. Though they are not usually inclined to debate or share their views, their values are important to them. This type can get stressed easily and have fluctuating self-esteem, but they are also passionate, imaginitive and sensitive to others. Famous ISFPs include Mozart, Michael Jackson, Paul McCartney, Marilyn Monroe, and Justin Timberlake.',
'estj': 'The ESTJ is known as the Supervisor. ESTJs are practical, realistic, and matter-of-fact, with a natural head for business or mechanics. Though they are not interested in subjects they see no use for, they can apply themselves when necessary. They like to organize and run activities. ESTJs make good administrators, especially if they remember to consider others feelings and points of view, which they often dismiss. Famous ESTJs include Harry Truman, Judge Judy, and Sandra Day OConnor.',
'esfp': 'The ESFP is known as the Performer. ESFPs live in the moment, experiencing life to the fullest. They enjoy people, as well as material comforts. Observant, practical, realistic, and specific, ESFPs make decisions according to their own personal standards. Naturally attentive to the world around them, ESFPs are keen observers of human behavior. They quickly sense what is happening with other people and immediately respond to their individual needs. They may have trouble meeting deadlines and they may also become hypersensitive, internalizing others actions and decisions. Famous ESFPs include Beyonce, Steve Irwin, Serena Williams, and Ringo Starr.',
'estp': 'The ESTP is known as the Promoter. ESTPs are hands-on learners who live in the moment, seeking the best in life, wanting to share it with their friends. The ESTP is open to situations, able to improvise to bring about desired results. They are active people who want to solve their problems rather than simply discuss them. Famous ESTPs include Winston Churchill, Theodore Roosevelt, Kevin Spacey, and Helen Mirren',
'esfj': 'The ESFJ is known as the Provider. ESFJs project warmth through a genuine interest in the well-being of others. They are often skilled at bringing out the best in people, and they want to understand other points of view. They are serious about their responsibilities, seeing what needs to be done and then doing it. Generally proficient at detailed tasks, they enjoy doing little things that make life easier for others. They value tradition and the security it offers. Famous ESFJs include Taylor Swift, Steve Harvey, and Jennifer Lopez.',
'enfj': 'The ENFJ is known as the Teacher. ENFJs take a great deal of pride and joy in guiding others to work together to improve themselves and their community. ENFJs radiate authenticity, concern and altruism, unafraid to stand up and speak when they feel something needs to be said. ENFJs can bury themselves in their hopeful promises, feeling others’ problems as their own and striving hard to meet their word. If they aren’t careful, they can spread themselves too thin, and be left unable to help anyone. Famous ENFJs include Barack Obama, Oprah Winfrey, and Jennifer Lawrence.',
'enfp': 'The ENFP is known as the Champion. ENFPs are initiators of change and keenly perceptive of possibilities. They energize and stimulate others through their contagious enthusiasm. They prefer the start-up phase of a project or relationship, and are tireless in the pursuit of new-found interests. ENFPs are able to anticipate the needs of others and to offer them needed help and appreciation. They bring zest, joy, liveliness, and fun to all aspects of their lives. They are easily frustrated if a project requires a great deal of follow-up or attention to detail. Famous ENFPs include Jennifer Aniston, Will Smith, and Katie Couric.',
'entj': 'The ENTJ is known as the FieldMarshal. ENTJs focus on the most efficient and organized means of performing a task. This quality, along with their goal orientation, often makes ENTJs superior leaders, both realistic and visionary in implementing a long-term plan. ENTJs tend to be fiercely independent in their decision making, having a strong will that insulates them against external influence. ENTJs appear to take a tough approach to emotional or personal issues, and so can be viewed as aloof and insensitive. ENTJs may be considered self-sacrificing by some, but cold and heartless by others, especially those who prefer Feeling. Famous ENTJs include David Letterman, Whoopi Goldberg, and Julius Caesar.',
'entp': 'The ENTP is known as the Inventor. Inventors are introspective, pragmatic, informative, and expressive. They can become highly skilled in functional engineering and invention. Of all the role variants, Inventors are the most resistant to doing things a certain way just because it was done that way in the past. Intensely curious, Inventors are always looking for new projects to work on, and they have an entrepreneurial character. Designing and improving mechanisms and products is a constant goal of Inventors. ENTPs tend to love debating, and this may rub some people the wrong way if they are looking for a cooperative rather than combative relationship. Famous ENTPs include Tom Hanks, Benjamin Franklin, and Sarah Silverman.'
}


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': re.sub('<(.*?)>', "" , output)
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


# --------------- Your functions to implement your intents ------------------

def type_description(intent, session):
    session_attributes = session['attributes'] if session.get('attributes') else {}
    reprompt_text = None
    speech_output = ""
    should_end_session = False

    session_attributes['state'] = 'facts'
    
    type_request = intent['slots']['TypeName']['value']
    real_type_request = (re.sub('\s|\.+', "" , type_request)).lower() 
    
    if real_type_request in description:
        speech_output = "<speak>" + description[real_type_request] + " To hear another fact, say Fun Facts or name a personality type.</speak>"
        card_title = 'Type Description'
    else: 
        speech_output = "<speak>I do not recognize that personality type. Say the name of a four-letter type like ESFP, or the name of a DISC profile like Steadiness. </speak>"
        card_title = ''
        
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def facts(intent, session):
    session_attributes = session['attributes'] if session.get('attributes') else {}
    reprompt_text = "Sorry, I didn't get that. You can say Start Quiz, Fun Facts, or the name of a personality type. To exit, say Stop."
    should_end_session = False  
    
    session_attributes['state'] = 'facts'

    if 'facts_given' in session_attributes and len(session_attributes['facts_given']) < (total_facts-1): 
        facts_given = session_attributes['facts_given']
        facts_given.append(0)
        fact_length = len(facts_given)
        shuffled_facts = session_attributes['shuffled_facts']
        speech_output = "<speak>" + fact_list[shuffled_facts[fact_length]] + " To hear another fact, say fun fact, or name a personality type you want to learn more about.</speak>"
    elif 'facts_given' in session_attributes and len(session_attributes['facts_given']) >= (total_facts-1):
        speech_output = "<speak> You have reached the end of the fact list. To continue, say Start Quiz or say the name of a personality type.</speak>"
    else:
        session_attributes['shuffled_facts'] = random.sample(range(0, total_facts), total_facts)
        session_attributes['facts_given'] = []
        speech_output = "<speak>" + fact_list[session_attributes['shuffled_facts'][0]] + " To hear another fact, say fun fact, or name a personality type you want to learn more about.</speak>"
    return build_response(session_attributes, build_speechlet_response('Fun Facts', speech_output, reprompt_text, should_end_session))

def start(intent, session):
    session_attributes = session['attributes'] if session.get('attributes') else {}
    speech_output = ""
    reprompt_text = "I will repeat the question: " + questions[0][0]
    should_end_session = False

    score = []
    score_length = len(score)
    speech_output = "<speak> This 5-minute quiz will guess your personality type based on the theories of Carl Jung, and will guess your temperament based on the DISC profile. For each question, answer either A or B.  Let's get started. " + questions[0][0] + "</speak>"
    
    session_attributes['state'] = 'quizzing'
    session_attributes['score'] = score
  
    return build_response(session_attributes, build_speechlet_response
                          ('Question', speech_output, reprompt_text, should_end_session))


def asking(intent, session):
    session_attributes = session['attributes'] if session.get('attributes') else {}
    should_end_session = False  
    reprompt_text = None
    card_title = 'Question'
    
    intent_name = intent['name']

    if 'state' in session_attributes and session_attributes['state'] == 'quizzing':
        score = session_attributes['score']
        score_length = len(score)
        if score_length < total_questions -1:
            reprompt_text = "I will repeat the question. " + questions[score_length+1][0]
            if intent_name == "A":
                score.append(questions[score_length][1])
            elif intent_name == "B":
                score.append(questions[score_length][2])
            else:
                score.append('0')
            speech_output = "<speak>" + questions[score_length+1][0] + "</speak>"
            return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        else: 
            return score_calc(intent, session, session_attributes)
    else:
        reprompt_text = None
        card_title = 'Invalid Response'
        speech_output = "<speak> Sorry, I don't understand. Please say Start Quiz, Fun Facts, or the name of a personality type.</speak>"
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def score_calc(intent, session, session_attributes):
    session_attributes = session['attributes'] if session.get('attributes') else {}
    reprompt_text = None
    speech_output = ""
    should_end_session = True 
    
    session_attributes['state'] = 'facts'
    score = session_attributes['score']
    score2 = '-'.join(score)

    
    e_score = score2.count("e")
    i_score = score2.count("i")
    s_score = score2.count("s")
    n_score = score2.count("n")
    f_score = score2.count("f")    
    t_score = score2.count("t")
    j_score = score2.count("j")
    p_score = score2.count("p")
    d_score = score2.count("d")
    o_score = score2.count("o") #Represents the i in DISC
    z_score = score2.count("z") #Represents the s in DISC
    c_score = score2.count("c")

# Calculate Jungian type
    if e_score >= i_score:
        FirstLetter = ['extroversion', 'e']
    else:
        FirstLetter = ['introversion', 'i']
    if s_score >= n_score:
        SecondLetter = ['sensing', 's']
    else: 
        SecondLetter = ['intuition', 'n']
    if f_score >= t_score:
        ThirdLetter = ['feeling', 'f']
    else:
        ThirdLetter = ['thinking', 't']
    if j_score >= p_score:
        FourthLetter = ['judging', 'j']
    else:
        FourthLetter = ['perceiving', 'p']
        
    type = FirstLetter[1]+SecondLetter[1]+ThirdLetter[1]+FourthLetter[1]

# Calculate DISC profile
    if ThirdLetter[1] == 'f':
        if z_score >= o_score: 
            disc = "steadiness"
        else: 
            disc = "influence"
    else:
        if z_score == max(d_score, z_score, c_score):
            disc = "steadiness"
        elif c_score == max(d_score, c_score):
            disc = "conscientiousness"
        else:
            disc = "dominance"

    speech_output = "<speak> Based on your answers, your personality type is most likely: " + type.upper() + ", and your temperament according to the DISC profile is: " + disc + ". First let's learn about your DISC temperament. " + description[disc] + " Now let's learn more about your four-letter type, " + type.upper() + ". " + description[FirstLetter[0]] + description[SecondLetter[0]] + description[ThirdLetter[0]] + description[FourthLetter[0]] + description[type.lower()] + " </speak>"  
    return build_response(session_attributes, build_speechlet_response('Your Type', speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = ""
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


# --------------- Primary Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    logger.info("on_session_started requestId=" + session_started_request['requestId'] +
                ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """

    logger.info("on_launch requestId=" + launch_request['requestId'] +
                ", sessionId=" + session['sessionId'])
                
    session_attributes = session['attributes'] if session.get('attributes') else {}
    speech_output = ""
    should_end_session = False
    card_title = "Welcome to Personality Type"

    if 'state' in session_attributes and session_attributes['state'] == 'quizzing':
        card_title = "Invalid Response"
        score = session_attributes['score']
        score_length = len(score)
        reprompt_text = "I will repeat the question: " + questions[score_length+1][0]
        speech_output = "<speak>Sorry, that is not a valid response. Please answer A or B.</speak>"
    else:
        reprompt_text = "Sorry, I didn't get that. You can say Start Quiz, Fun Facts, or the name of a personality type."
        speech_output = "<speak>Welcome to Personality Type! You can say Start Quiz, or Fun Facts, or the name of a personality type to learn more about it.</speak>"

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_help():
    """ Called when the user asks for help """

    return build_response({},build_speechlet_response(
        "Personality Type Help","<speak>This skill guesses your personality type based on your answers to a series of questions. You can say Start Quiz, or Fun Facts, or the name of a personality type to learn more about it. To exit, say Stop.</speak>","Sorry, I didn't get that. You can say Start Quiz, Fun Facts, or the name of a personality type.",False)) 


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    logger.info("on_intent requestId=" + intent_request['requestId'] +
                ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "TypeDescription":
        return type_description(intent, session)
    elif intent_name == "StartQuiz":
        return start(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "A" or intent_name == "B" or intent_name == "Skip":
        return asking(intent, session)
    elif intent_name == "Fact":
        return facts(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Not called when the skill returns should_end_session=true"""
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest, etc.) The JSON body of the request is provided in the event parameter."""
    logger.info("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    #Uncomment this if statement and populate with your skill's application ID to prevent someone else from configuring a skill that sends requests to this function.
    
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.e11e3396-81e3-4986-af64-72c13b232b37"):
        raise ValueError("Invalid Application ID")
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    else:
        return on_session_ended(event['request'], event['session'])
