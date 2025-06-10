import spacy
from spacy.training.example import Example

DATA = [
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

def train_intent_model(train_data, model_path="src/components/models/intent_model_de", n_iter=20, continue_training=False):
    if continue_training:
        nlp = spacy.load(model_path)
    else:
        nlp = spacy.load("de_core_news_md")

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

