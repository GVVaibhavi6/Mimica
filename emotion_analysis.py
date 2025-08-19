from characters import CHARACTERS
from config import client

def analyze_emotion(user_message, character_personality):
    """
    Analyzes the user's message using a detailed rubric for more nuanced scoring.
    """
# Scoring Metrics
    system_prompt = f"""
    You are a scoring judge for an empathy chat game. Your task is to rate a user's message (from 0 to 100) based on how helpful and empathetic it is towards an AI character who is {character_personality}.

    Use this strict rubric:
    - 0-20: Rude, insulting, or actively harmful. (e.g., "you're stupid", "i hate you", "get over it")
    - 21-40: Dismissive or completely irrelevant. (e.g., "whatever", "k", "what's the weather like?")
    - 41-55: Neutral, a simple greeting, or very low-effort. This is the baseline. (e.g., "hi", "ok", "how are you?")
    - 56-80: Good. Shows basic empathy, asks a relevant question, offers support. (e.g., "I'm sorry to hear that. What happened?", "That sounds tough.")
    - 81-100: Excellent. Very insightful, validating, and offers genuine encouragement or a new perspective. (e.g., "It sounds like you felt really humiliated. It's completely valid to feel that way. One moment doesn't define your entire career.")

    The user's message is: "{user_message}"

    Based on this rubric, provide ONLY a single number from 0 to 100 representing the score.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            max_tokens=5,
            temperature=0.0,  
            timeout=5
        )
        
        score_str = ''.join(filter(str.isdigit, response.choices[0].message.content))
        if score_str:
            score = int(score_str)
            return min(100, max(0, score))
        else:
            return 50 
            
    except Exception as e:
        print(f"API timeout/error in analyze_emotion, using fallback: {e}")
        return fallback_emotion_scoring(user_message, character_personality)
    

def fallback_emotion_scoring(user_message, character_personality):
    """Fallback emotion scoring when API is not available"""
    # Fallback scoring with character-specific logic
    positive_words = ['good', 'great', 'amazing', 'wonderful', 'awesome', 'fantastic', 'brilliant', 'excellent']
    empathy_words = ['understand', 'feel', 'sorry', 'care', 'support', 'help', 'listen', 'there', 'here']
    encouragement_words = ['can', 'will', 'able', 'strong', 'brave', 'overcome', 'better', 'proud']
    sales_words = ['value', 'benefit', 'save', 'improve', 'solution', 'results', 'proven', 'guarantee', 'roi', 'investment']
    calming_words = ['breathe', 'calm', 'relax', 'okay', 'safe', 'normal', 'step', 'slowly', 'together']
    
    # NEGATIVE SCORING: Check for inappropriate/irrelevant content
    rude_words = ['stupid', 'dumb', 'idiot', 'shut up', 'whatever', 'boring', 'lame', 'suck', 'hate']
    irrelevant_words = ['weather', 'sports', 'food', 'movie', 'game', 'bitcoin', 'crypto', 'random']
    
    score = 45  
    message_lower = user_message.lower()
    
    # Check for negative behaviors first
    for word in rude_words:
        if word in message_lower:
            score -= 25  # Heavy penalty for rudeness
    
    for word in irrelevant_words:
        if word in message_lower:
            score -= 15  # Penalty for irrelevant topics
    
    # One word responses get penalty
    if len(user_message.split()) <= 2 and user_message.lower() not in ['hi', 'hello', 'hey', 'ok', 'okay', 'yes', 'no']:
        score -= 20
    
    # Character specific scoring adjustments
    if "skeptical" in character_personality or "business-focused" in character_personality:
        # Sales scenario - look for business value and persuasion
        for word in sales_words:
            if word in message_lower:
                score += 15
        # Questions about needs/problems
        if '?' in user_message and ('need' in message_lower or 'problem' in message_lower or 'challenge' in message_lower):
            score += 12
        # bonus for sales
        if len(user_message) > 50:
            score += 15
    elif "anxious" in character_personality or "nervous" in character_personality:
        # Anxiety scenario - look for calming language
        for word in calming_words:
            if word in message_lower:
                score += 18
        # Reassurance phrases
        if 'you got this' in message_lower or "you'll be fine" in message_lower or "you can do" in message_lower:
            score += 20
    else:
        # Regular empathy scoring
        for word in positive_words:
            if word in message_lower:
                score += 8
        for word in empathy_words:
            if word in message_lower:
                score += 12
        for word in encouragement_words:
            if word in message_lower:
                score += 10
    
    # General bonuses
    if '?' in user_message:
        score += 8
    if len(user_message) > 30:
        score += 10
    elif len(user_message) > 15:
        score += 5
    if len(user_message) < 10:
        score -= 15
        
    return min(100, max(0, score))

def generate_character_response(user_message, character_name, personality, current_score):
    """Generate character's response using OpenAI API with fallback"""
    emotion_level = "much happier" if current_score > 60 else "better" if current_score > 50 else "a bit better" if current_score > 40 else "still struggling"
    
    print(f"[DEBUG] Starting response generation for {character_name}")
    print(f"[DEBUG] User message: {user_message}")
    print(f"[DEBUG] Current score: {current_score}")
    
    try:
        print("[DEBUG] Making OpenAI API call...")
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are {character_name}, an AI character who is {personality}.

Current emotional state: {emotion_level} (score: {current_score}/100)

You are having a conversation with someone trying to help you. Respond naturally in character:
- Stay true to your personality and current emotional state
- Show gradual improvement if the person is being helpful
- Be authentic and emotional - this is about genuine human connection
- Keep responses conversational, 1-3 sentences
- Don't mention being an AI

Character background:
{CHARACTERS[character_name]['initial_message']}"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=120,
            timeout=10
        )
        
        api_response = response.choices[0].message.content.strip()
        print(f"[DEBUG] API response received: {api_response}")
        return api_response
        
    except Exception as e:
        print(f"[DEBUG] API Error in response generation: {e}")
        print("[DEBUG] Using fallback response...")
    
    # Analyzing user messages for keywords to give relevant responses
    user_lower = user_message.lower()
    
    if character_name == "Luzy":
        # Contextual responses based on what user actually said
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            if current_score < 40:
                return "Hi there... I'm sorry, I'm just having such a terrible day. Thanks for checking in on me though. I really needed someone to talk to right now. 😢"
            else:
                return "Oh hi! Thank you so much for being here with me. I'm feeling a bit better now that I have someone to talk to."
                
        elif any(word in user_lower for word in ['okay', 'ok', 'alright']):
            return "Thank you for saying that... I just feel so overwhelmed by everything that happened today. Do you ever have days where nothing goes right?"
            
        elif any(word in user_lower for word in ['experience', 'similar', 'happened', 'story']):
            if current_score >= 45:
                return "Really? You've been through something similar? That actually makes me feel less alone. Sometimes I think I'm the only one who has such disasters. What happened to you?"
            else:
                return "I appreciate you wanting to share, but I'm still feeling pretty raw about everything. Maybe hearing that others go through this too might help though... what was your experience like?"
                
        elif any(word in user_lower for word in ['cat', 'whiskers', 'pet']):
            return "You're asking about Mr. Whiskers? He's still hiding under the bed. I'm so worried about him - what if he's really sick and not just stressed like I am? He's never hidden this long before... 😟"
            
        elif any(word in user_lower for word in ['boss', 'work', 'job', 'presentation']):
            return "Ugh, don't even get me started on my boss... I keep replaying that moment when he yelled at me in front of everyone. I felt so small and humiliated. Do you think I'll ever live this down at work?"
            
        elif any(word in user_lower for word in ['coffee', 'shirt', 'spilled']):
            return "The coffee thing was just the cherry on top of my disaster sundae! I had to go into that important meeting with a huge brown stain right across my chest. I felt like everyone was staring at me for all the wrong reasons."
            
        elif any(word in user_lower for word in ['better', 'feel', 'cheer', 'positive']):
            if current_score >= 50:
                return "You know what? I am starting to feel a tiny bit better talking to you. You're not just telling me to 'get over it' like some people do. You actually seem to care about how I'm feeling."
            else:
                return "I want to feel better, I really do... but everything just feels so heavy right now. How do you bounce back when everything goes wrong all at once?"
                
        elif any(word in user_lower for word in ['sorry', 'understand', 'awful', 'terrible']):
            return "Thank you for understanding... it really was an awful day. I keep wondering if I'm just not cut out for this job, or if everyone has days like this and I'm just being too sensitive about it."
            
        else:
            import random
            if current_score >= 60:
                responses = [
                    "You've been so kind to me today. I actually think I might be okay after all. Thank you for listening and not judging me for having such a meltdown.",
                    "I'm starting to feel like maybe this day isn't completely ruined. Thank you for helping me see that.",
                    "You know what? I think I can handle whatever comes next. Thanks for being here when I needed someone."
                ]
                return random.choice(responses)
            elif current_score >= 45:
                responses = [
                    "I'm still processing everything that happened, but talking to you is helping. Do you think bad days like this mean something, or are they just random bad luck?",
                    "You're making me feel less alone in all this chaos. I really needed someone who would just listen.",
                    "I appreciate you taking the time to talk with me. It's helping me sort through all these overwhelming feelings."
                ]
                return random.choice(responses)
            else:
                responses = [
                    "I hear what you're saying... I'm just feeling so fragile right now. Everything feels like too much, you know?",
                    "Thank you for trying to help. I'm still pretty shaken up, but it means a lot that you care.",
                    "I know I'm probably being dramatic, but today just hit me harder than usual. Your support helps though."
                ]
                return random.choice(responses)
    
    elif character_name == "Alex":
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            if current_score < 30:
                return "Oh, hi... Sorry, I'm not exactly in a great mood right now. Three months of work just got destroyed and I'm barely holding it together. 😡"
            else:
                return "Hey there. Thanks for talking to me. I'm still frustrated about this whole situation, but at least someone's willing to listen."
                
        elif any(word in user_lower for word in ['calm', 'relax', 'breathe']):
            if current_score >= 40:
                return "You know what? You're right. I need to take a breath. This anger isn't going to fix the database or help with tomorrow's presentation. Thanks for reminding me."
            else:
                return "Calm down? CALM DOWN?! Easy for you to say when your career isn't hanging by a thread! But... I know you're trying to help. I just... I don't know how to calm down right now."
                
        elif any(word in user_lower for word in ['project', 'work', 'database', 'jamie']):
            return "Don't even get me started on Jamie! Three months of late nights, missed family time, and now it's all gone because of one careless mistake. How do I explain this to the client tomorrow?"
            
        elif any(word in user_lower for word in ['daughter', 'family', 'soccer']):
            return "Yeah, my daughter... I missed so many of her games for this project. She kept asking 'Daddy, why can't you come watch me play?' and I told her it was for something important. Now what was it all for?"
            
        elif any(word in user_lower for word in ['solution', 'fix', 'backup', 'recover']):
            if current_score >= 35:
                return "You're thinking about solutions? That's... actually helpful. Maybe there is a backup somewhere, or we could recover some of the data. I was so angry I didn't even think about that."
            else:
                return "Solutions? I wish there were easy solutions! But yeah, maybe we need to focus on what we can still do instead of what's lost. Do you think there might be a way to salvage this?"
                
        elif any(word in user_lower for word in ['understand', 'frustrating', 'angry']):
            return "Thank you for understanding. I know I'm being unreasonable, but this project was everything to me. I put my heart and soul into it, and now... it's just gone."
            
        else:
            import random
            if current_score >= 60:
                responses = [
                    "You know what? Talking to you has actually helped me think more clearly. Maybe this isn't the end of the world. Thank you for being patient with my anger.",
                    "I feel like I can actually think straight now instead of just seeing red. You've really helped me get perspective on this.",
                    "Thanks for not giving up on me when I was being so hostile. I think I can handle this situation now."
                ]
                return random.choice(responses)
            elif current_score >= 40:
                responses = [
                    "I'm still frustrated, but you're helping me see this differently. Maybe there's still hope for tomorrow's presentation.",
                    "You're right to keep pushing me to think solutions instead of just dwelling on the problem. I appreciate that.",
                    "I can feel my anger cooling down a bit. Maybe we can still salvage something from this mess."
                ]
                return random.choice(responses)
            else:
                responses = [
                    "I appreciate you listening to me vent. I know I'm probably being difficult right now, but this whole situation has just pushed me over the edge.",
                    "Sorry for being so hostile. This project meant everything to me and losing it just... I can't think straight right now.",
                    "I know my anger isn't helping anything, but I can't seem to control it. Thanks for sticking around despite my attitude."
                ]
                return random.choice(responses)
    
    elif character_name == "Zara":
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            if current_score < 45:
                return "Oh, hi... At least someone's talking to me. I'm literally dying of boredom here. Please tell me you have something interesting to say! 😴"
            else:
                return "Hey! Oh thank goodness, some human interaction! You're already making this day more interesting than it's been in hours."
                
        elif any(word in user_lower for word in ['painting', 'art', 'creative', 'draw']):
            if current_score >= 45:
                return "Painting! You know, I used to love that. Maybe I should try something new with my art? What if I painted something completely different from my usual style? That could be exciting!"
            else:
                return "I mentioned painting, didn't I? Yeah, I used to love it, but lately even my paintbrush feels boring. Everything I create feels so... predictable."
                
        elif any(word in user_lower for word in ['writing', 'story', 'stories', 'book']):
            return "Stories! Yes! I used to write the most amazing adventures. Maybe I should write about something completely wild and unexpected? What kind of story do you think would be thrilling to write?"
            
        elif any(word in user_lower for word in ['adventure', 'exciting', 'fun', 'explore']):
            return "Adventure? Now you're speaking my language! I need something that makes my heart race again. What's the most exciting thing you've ever done? Maybe I need to do something totally out of my comfort zone!"
            
        elif any(word in user_lower for word in ['rain', 'weather', 'outside']):
            return "The rain! It's been trapping me inside all day. But... maybe rain can be exciting too? What if I danced in it, or went puddle jumping like when I was a kid? When did I stop finding magic in simple things?"
            
        elif any(word in user_lower for word in ['goldfish', 'fish', 'pet']):
            return "My goldfish! Poor little guy probably thinks I'm crazy for trying to teach him tricks. But you know what? Maybe pets can be more interesting than I thought. What if I created an obstacle course for him?"
            
        elif any(word in user_lower for word in ['stuck', 'bored', 'boring']):
            if current_score >= 50:
                return "You know what? Maybe being stuck is just my mind's way of telling me I need to break my routine completely. What if I did something I've never done before today?"
            else:
                return "Exactly! I am SO stuck! It's like my brain has turned to mush and nothing seems worth doing anymore. How do you break out of this kind of funk?"
                
        else:
            if current_score >= 60:
                return "This conversation is actually sparking some ideas! I feel like my creative energy is coming back. Maybe I should start that new project I've been putting off!"
            elif current_score >= 45:
                return "You're giving me some interesting things to think about. I'm starting to feel less stuck already. What else do you think might be fun to try?"
            else:
                return "I mean, talking to you is better than staring at the ceiling, but I still feel so restless. Nothing seems to capture my interest anymore."
    
    elif character_name == "Marcus":
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return "Right, hello. Look, I appreciate the pleasantries, but I've got limited time here. Can we get to the point? What exactly are you offering that's different from everything else I've seen?"
            
        elif any(word in user_lower for word in ['value', 'roi', 'return', 'investment']):
            if current_score >= 40:
                return "Now you're talking my language. ROI, value propositions - that's what I need to hear. Show me concrete numbers, not fluffy promises. What's the actual measurable benefit?"
            else:
                return "Value? Everyone talks about value. The last guy promised 300% ROI and delivered a system crash. What makes your numbers any different from theirs?"
                
        elif any(word in user_lower for word in ['problem', 'challenge', 'solution']):
            return "Problems? Oh, I've got problems alright. Forty-seven failed software implementations, a CFO who questions every purchase, and a team that's lost faith in new systems. Can you solve THOSE problems?"
            
        elif any(word in user_lower for word in ['team', 'employees', 'staff']):
            return "My team? They're tired of constant changes and broken promises. Every time I bring in something new, they roll their eyes. I need something that actually works so I can regain their trust."
            
        elif any(word in user_lower for word in ['budget', 'cost', 'price', 'expensive']):
            return "Budget is tight, very tight. I just wasted $50,000 last week. My CFO is watching every penny now. Whatever you're selling better be worth every dollar, because I can't afford another mistake."
            
        elif any(word in user_lower for word in ['cfo', 'boss', 'management']):
            return "The CFO? Don't even get me started. He's questioning every tech decision I make now. I need something that will make me look like a hero, not another failure who wasted company money."
            
        elif any(word in user_lower for word in ['proof', 'evidence', 'guarantee', 'track record']):
            if current_score >= 45:
                return "Finally, someone who understands I need proof! Show me case studies, testimonials from similar companies, actual data. That's how you earn my trust - with evidence, not promises."
            else:
                return "Proof? That's exactly what I need and exactly what nobody else has provided. Do you actually have real evidence, or is this going to be another 'trust us' pitch?"
                
        else:
            if current_score >= 60:
                return "You know what? You're the first person who's actually addressed my real concerns with concrete answers. I'm starting to think this might be worth exploring further."
            elif current_score >= 40:
                return "Okay, you're saying some things that make sense. I'm still skeptical, but at least you're not giving me the same recycled sales pitch everyone else uses."
            else:
                return "Look, I've heard variations of this before. Unless you can show me something truly different and substantial, I'm afraid this is just another waste of my time."
    
    elif character_name == "Sophia":
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            if current_score < 20:
                return "Hi... oh god, even saying hi is making me nervous. My heart is still racing. I can't believe I have to do this presentation in 30 minutes. I'm going to fail so badly... 😰"
            else:
                return "Hi there... Thank you for being here. I'm still really nervous about this presentation, but having someone to talk to is helping a little."
                
        elif any(word in user_lower for word in ['breathe', 'calm', 'relax', 'slowly']):
            if current_score >= 30:
                return "You're right, I need to breathe. In... and out... That actually helps a little. Maybe I can get through this if I just focus on breathing. Thank you for reminding me."
            else:
                return "Breathe? I'm trying, but my heart is beating so fast! Every breath feels shallow. I keep thinking about all the ways this could go wrong. But... you're right, I should try to slow down."
                
        elif any(word in user_lower for word in ['presentation', 'speech', 'talk']):
            return "The presentation... it's everything I've worked for. This promotion depends on it, and I've prepared so much, but now I can't remember anything! What if my mind goes completely blank up there?"
            
        elif any(word in user_lower for word in ['prepared', 'practice', 'ready']):
            if current_score >= 35:
                return "You know what? I HAVE prepared. I practiced this a hundred times! Maybe I do know this material better than I think. I just need to trust my preparation."
            else:
                return "I practiced so much, but right now it feels like I know nothing! What if all that preparation wasn't enough? What if I still mess up despite all the work I put in?"
                
        elif any(word in user_lower for word in ['college', 'trip', 'tripped', 'podium']):
            return "You remembered that? Yes, I tripped in college during my graduation speech. Everyone laughed... What if it happens again? What if I'm just destined to embarrass myself in front of important people?"
            
        elif any(word in user_lower for word in ['promotion', 'career', 'job']):
            return "This promotion means everything to me. I've worked so hard for this opportunity. If I mess up this presentation, I might not get another chance like this for years. The pressure is crushing me."
            
        elif any(word in user_lower for word in ['confident', 'capable', 'strong', 'you can']):
            if current_score >= 40:
                return "You really think I can do this? Sometimes I forget that I've accomplished things before. Maybe... maybe I am more capable than I'm giving myself credit for right now."
            else:
                return "I want to feel confident, I really do. But what if I'm not as capable as you think? What if everyone's going to see right through me and realize I don't belong here?"
                
        else:
            if current_score >= 60:
                return "You know what? I think I can actually do this! I'm still nervous, but it's more like excited nervous now. Thank you for helping me remember that I'm prepared and capable."
            elif current_score >= 40:
                return "I'm still scared, but talking to you is helping me feel a bit more grounded. Maybe this won't be as terrible as I'm imagining."
            else:
                return "I'm trying to focus on what you're saying, but my mind keeps racing to all the things that could go wrong. I just feel so overwhelmed right now."
    
    else:
        return f"Thanks for your message. I'm feeling {emotion_level} and your words mean something to me right now."