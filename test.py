from googletrans import Translator

def translator_(query):
    translator = Translator()
    result= translator.translate(query, dest='ko')
    return result.text

print(translator_('Discover Goodnotes 6, the AI note-taking app loved by millions around the world'))
