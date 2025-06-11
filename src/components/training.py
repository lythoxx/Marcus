import spacy
from spacy.training.example import Example

DATA_DE = [
    # WEATHER
    ("Wie ist das Wetter heute?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wird es morgen regnen?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wie wird das Wetter morgen?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wie ist die Wettervorhersage für heute?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Ist es heute sonnig?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wird es heute kalt?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wird es heute schneien?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wie ist die Temperatur heute?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Gibt es heute Regen?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wird es morgen warm?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI": 0}}),
    ("Wie ist das Wetter am Wochenende?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Brauche ich heute einen Regenschirm?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wie windig ist es draußen?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wie hoch ist die Luftfeuchtigkeit?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wie ist das Wetter in Berlin?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wird es heute Nacht frieren?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wie ist die Wetterlage für morgen früh?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wie viele Grad sind es draußen?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wie ist das Wetter nächste Woche?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Wird es am Nachmittag regnen?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),

    # ALARM
    ("Stelle einen Wecker für 7 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Setze einen Alarm für 8 Uhr morgens.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Wecker auf 6 Uhr stellen.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm für morgen früh um 5 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Stelle einen Alarm für heute Abend um 9 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Setze einen Wecker für den nächsten Tag um 10 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Wecker auf morgen früh um halb sieben stellen.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm für heute um Mitternacht setzen.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Stelle einen Wecker für den nächsten Morgen um acht Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Setze einen Alarm für heute Nachmittag um drei Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Wecker auf 5:30 Uhr stellen.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Stelle einen Alarm für morgen Mittag.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Kannst du mich um 6 Uhr wecken?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm für Samstag um 8 Uhr einstellen.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Stelle einen Wecker für 22 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Wecker für morgen um 7:15 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm auf 9 Uhr setzen.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Stelle einen Alarm für übermorgen um 6 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Kannst du einen Wecker für 5 Uhr stellen?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm für heute Abend um 20 Uhr.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),

    # MUSIC
    ("Spiele meine Lieblingsmusik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik von Ed Sheeran.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele entspannende Musik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Rockmusik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Popmusik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Jazzmusik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele klassische Musik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik für gute Laune.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik zum Entspannen.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele meine Playlist.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele etwas von den Beatles.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Mach Musik an.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Kannst du Musik spielen?", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Weihnachtsmusik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik zum Tanzen.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik für die Party.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik zum Einschlafen.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik von Queen.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele Musik aus den 80ern.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Spiele laute Musik.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),

    # AI (General Questions)
    ("Hallo Marcus!", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wie geht es dir?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was kannst du tun?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Erzähle mir einen Witz.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was ist die Hauptstadt von Deutschland?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wie spät ist es?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was ist dein Lieblingsessen?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Kannst du mir bei meinen Aufgaben helfen?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was ist dein Lieblingsfilm?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Erzähl mir etwas Interessantes.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wie funktioniert künstliche Intelligenz?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wer hat dich programmiert?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wie alt bist du?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Kannst du mir helfen?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was ist der Sinn des Lebens?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Erzähl mir etwas über Berlin.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wie heißt du?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was kannst du alles?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Wie programmiert man einen Bot?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Was ist Python?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}})
]

DATA_EN = [
    # WEATHER
    ("How is the weather today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Will it rain tomorrow?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("How will the weather be tomorrow?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("What is the weather forecast for today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Is it sunny today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Will it be cold today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Will it snow today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("What is the temperature today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Is it going to rain today?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("Will it be warm tomorrow?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    ("How is the weather this weekend?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0,"AI" :0}}),
    ("Do I need an umbrella today?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("How windy is it outside?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("What is the humidity level?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("How is the weather in Berlin?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("Will it freeze tonight?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("What is the weather like tomorrow morning?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("How many degrees is it outside?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("How is the weather next week?", {"cats" :{"WEATHER" :1,"MUSIC" :0,"ALARM" :0,"AI" :0}}),
    ("Will it rain in the afternoon?", {"cats": {"WEATHER": 1, "MUSIC": 0, "ALARM": 0, "AI": 0}}),
    
    # ALARM
    ("Set an alarm for 7 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for 8 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set a wake-up call for 6 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm for tomorrow morning at 5 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for tonight at 9 PM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set a wake-up call for the next day at 10 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for tomorrow morning at half past six.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Alarm for tonight at midnight.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set a wake-up call for the next morning at eight o'clock.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for this afternoon at three o'clock.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set a wake-up call for five thirty.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for tomorrow noon.", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :1,"AI" :0}}),
    ("Can you wake me up at six o'clock?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :1,"AI" :0}}),
    ("Alarm for Saturday at 8 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for 10 PM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Wake-up call for tomorrow at 7:15 AM.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for nine o'clock.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Set an alarm for the day after tomorrow at six o'clock.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 1, "AI": 0}}),
    ("Can you set a wake-up call for five o'clock?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :1,"AI" :0}}),
    ("Alarm for tonight at eight o'clock.", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :1,"AI" :0}}),

    # MUSIC
    ("Play my favorite music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play music by Ed Sheeran.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play relaxing music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play rock music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play pop music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play jazz music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play classical music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play happy music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play music to relax.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play my playlist.", {"cats" :{"WEATHER" :0,"MUSIC" :1,"ALARM" :0,"AI" :0}}),
    ("Play something by the Beatles.", {"cats" :{"WEATHER" :0,"MUSIC" :1,"ALARM" :0,"AI" :0}}),
    ("Turn on the music.", {"cats" :{"WEATHER" :0,"MUSIC" :1,"ALARM" :0,"AI" :0}}),
    ("Can you play some music?", {"cats" :{"WEATHER" :0,"MUSIC" :1,"ALARM" :0,"AI" :0}}),
    ("Play Christmas music.", {"cats" :{"WEATHER" :0,"MUSIC" :1,"ALARM" :0,"AI" :0}}),
    ("Play music to dance to.", {"cats" :{"WEATHER" :0,"MUSIC" :1,"ALARM" :0,"AI" :0}}),
    ("Play party music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play music to sleep to.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play music by Queen.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play music from the 80s.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),
    ("Play loud music.", {"cats": {"WEATHER": 0, "MUSIC": 1, "ALARM": 0, "AI": 0}}),

    # AI (General Questions)
    ("Hello Marcus!", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("How are you?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("What can you do?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Tell me a joke.", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("What is the capital of Germany?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("What time is it?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("What is your favorite food?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("Can you help me with my tasks?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("What is your favorite movie?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("Tell me something interesting.", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("How does artificial intelligence work?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("Who programmed you?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("How old are you?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("Can you assist me?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("What is the meaning of life?", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("Tell me something about Berlin.", {"cats" :{"WEATHER" :0,"MUSIC" :0,"ALARM" :0,"AI" :1}}),
    ("What is your name?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("What can you do?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("How do you program a bot?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}}),
    ("What is Python?", {"cats": {"WEATHER": 0, "MUSIC": 0, "ALARM": 0, "AI": 1}})
]

def train_intent_model(train_data, model, model_path="src/components/models/intent_model", n_iter=20, continue_training=False):
    if continue_training:
        nlp = spacy.load(model_path)
    else:
        nlp = spacy.load(model)

    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    # Add any new labels from training data
    labels = set()
    for _, annotations in train_data:
        labels.update(annotations["cats"].keys())
    for label in labels:
        if label not in textcat.labels:
            textcat.add_label(label)

    # Training loop
    optimizer = nlp.resume_training() if continue_training else nlp.initialize()
    for i in range(n_iter):
        losses = {}
        for text, annotations in train_data:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.2, losses=losses)

    nlp.to_disk(model_path)

