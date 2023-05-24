from help_functions import intersection


def alpha_b(cartesian_product, set_of_sets):
    """
    Berechnet die Funktion alpha für den Fall der Bisimularität.

    :param cartesian_product: das kartesische Produkt der Menge der Zustände mit sich selbst
    :param set_of_sets: eine Menge von Mengen
    :return: eine Äquivalenzrelation, deren Elemente die Bedingung von alpha erfüllen
    """
    relation = []
    for tupel in cartesian_product:
        counter = 0
        for set_x in set_of_sets:
            if ((tupel[0] in set_x) & (tupel[1] not in set_x)) | ((tupel[0] not in set_x) & (tupel[1] in set_x)):
                break
            counter += 1
            if counter == len(set_of_sets):
                relation.append(tupel)
    return relation


def alpha_t(cartesian_product, set_of_sets):
    """
    Berechnet die Funktion alpha für den Fall der Sprachäquivalenz.

    :param cartesian_product: das kartesische Produkt der Potenzmenge der Menge aller Zustände mit sich selbst
    :param set_of_sets: eine Menge von Mengen
    :return: eine Äquivalenzrelation, deren Elemente die Bedingung von alpha erfüllen
    """
    relation = []
    for tupel in cartesian_product:
        counter = 0
        for set_x in set_of_sets:
            if ((not intersection(tupel[0], set_x)) & (intersection(tupel[1], set_x) != [])) | (
                    (intersection(tupel[0], set_x) != []) & (not intersection(tupel[1], set_x))):
                break
            counter += 1
            if counter == len(set_of_sets):
                relation.append(tupel)
    return relation
