from anki.collection import Collection, SearchNode, SearchJoiner


# Windows Path
# TODO: Add Windows path here

# WSL Path
# Remember that you're in WSL and the path to the Collection needs to be via mnt!!
col = Collection("/mnt/c/users/leste/AppData/Roaming/Anki2/User 1/collection.anki2")
# cardIds = col.find_cards(col.build_search_string("deck:Chinese Vocab Mining"))

# rthz1IDs = col.find_notes("\"note:Remember Traditional Hanzi\"")

# print(SearchNode(Jyutping=""))
# search = col.build_search_string(SearchNode(note="Remember Traditional Hanzi"), SearchNode(negated=SearchNode("\"Jyupting:\"")))
# print(search)


rthz1IDs = col.find_notes("\"note:Remember Traditional Hanzi\" Jyutping:")
for id in rthz1IDs:
    note = col.get_note(id)
    if not note["Jyutping"]:
        # Need to find a way to access a dictionary, PyCantonese is interesting but I don't think it provides what I need
        # CC-Canto probably has some sort of Python library out there
        print(note["Traditional Hanzi"] + " Keyword: " + note["Keyword"])

# if col.get_note(1721504136876)["Jyutping"]:
#     print(col.get_note(1721504136876)["Jyutping"])


# Seems like you need to encapsulate search queries with escaped quotes. Maybe using SearchNode is better.
# rthz1IDs = col.find_notes("\"note:Remember Traditional Hanzi\"")
# print(rthz1IDs)

# Multiple search arguments in SearchNode leave just the last one.
# print(col.build_search_string(SearchNode(deck="Chinese Vocab Mining", note="LapisZH", dupe=SearchNode.Dupe()), joiner="\"AND\""))

# Why the actual wack does setting the joiner as AND turn it into "OR"?
# Seems like it defaults to AND, and if you put in SearchJoiner for the joiner argument, it turns into OR.
# print(col.build_search_string(SearchNode(deck="Chinese Vocab Mining"), SearchNode(note="LapisZH"), SearchNode(dupe=SearchNode.Dupe()), joiner="\"AND\""))
# print(col.build_search_string(SearchNode(deck="Chinese Vocab Mining"), SearchNode(note="LapisZH"), SearchNode(dupe=SearchNode.Dupe()), joiner=SearchJoiner))
# print(SearchNode.Dupe())

# Guess the below can be used to programmatically construct search strings in an easier way than stitching strings, although it is basically stitching strings,
# print(col.build_search_string(SearchNode(deck="Chinese Vocab Mining"), "\"AND\"", SearchNode(note="LazpisZH")))


# TODO: Need to figure out how build_search_string works

# Model for getting a card and it's note. Does print the correct meaning. Can modify it with the methods shown here.
# https://addon-docs.ankiweb.net/the-anki-module.html
# print(col.get_card(1749441340181).note()["Meaning"])


# for cardId in cardIds:
#     card = col.get_card(cardId)
#     print(cardId)
    # note = card.note()
    # if not note["jyutping"]:
    #     print(note["Chinese"])
# print(col.sched.deck_due_tree())

#test