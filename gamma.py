from help_functions import intersection


def gamma_b(potency_set, relation):
    """
    Berechnet die Funktion gamma für den Fall der Bisimularität.

    :param potency_set: die Potenzmenge der Menge aller Zustände
    :param relation: eine Äquivalenzrelation
    :return: eine Menge von Mengen, die die Bedingung von gamma erfüllen
    """
    set_of_sets = []
    for set_x in potency_set:
        counter = 0
        for tupel in relation:
            if ((tupel[0] in set_x) & (tupel[1] not in set_x)) | ((tupel[0] not in set_x) & (tupel[1] in set_x)):
                break
            counter += 1
            if counter == len(relation):
                set_of_sets.append(set_x)
    return set_of_sets


def gamma_t(potency_set, relation):
    """
    Berechnet die Funktion gamma für den Fall der Sprachäquivalenz.

    :param potency_set: die Potenzmenge der Menge aller Zustände
    :param relation: eine Äquivalenzrelation
    :return: eine Menge von Mengen, die die Bedingung von gamma erfüllen
    """
    set_of_sets = []
    for set_x in potency_set:
        counter = 0
        for tupel in relation:
            if ((not intersection(tupel[0], set_x)) & (intersection(tupel[1], set_x) != [])) | (
                    (intersection(tupel[0], set_x) != []) & (not intersection(tupel[1], set_x))):
                break
            counter += 1
            if counter == len(relation):
                set_of_sets.append(set_x)
    return set_of_sets
