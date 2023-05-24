def diamond(states, transitions, set_of_sets, action):
    """
    Berechnet das Ergebnis des Diamant-Operators für die gegebene Aktion der gegebenen Menge von Mengen

    :param states: die Menge aller Zustände
    :param transitions: die relation der Übergänge des Transitionssystems
    :param set_of_sets: eine Menge von Mengen, auf die der Diamant-Operator angewandt werden soll
    :param action: die Aktion des Diamant-Operators, die untersucht werden soll
    :return: eine Menge von Mengen, deren Elemente mit der gegebenen Aktion mindestens einen Übergang in eine Teilmenge
            von set_of_sets besitzen
    """
    result = []
    for set_x in set_of_sets:
        interim_result = []
        for transition in transitions:
            if (str(transition[1]) == action) & (transition[2] in set_x) & (transition[0] in states) & (
                    transition[0] not in interim_result):
                interim_result.append(transition[0])
            else:
                continue
        interim_result.sort()
        if interim_result not in result:
            result.append(interim_result)
    return result
