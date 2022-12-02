import wikipedia

wikipedia.set_lang('ru')


def search_wiki(word):
    print(word)
    try:
        w = wikipedia.search(word)
        if w:
            w2 = wikipedia.page(word).url
            w1 = wikipedia.summary(word)
            return w1, '\nСсылка: ' + w2
        return "Запрос в Википедии не найден. Уточните поиск.", ""
    except:
        return "Википедия не доступна. Повторите позже.", ""
