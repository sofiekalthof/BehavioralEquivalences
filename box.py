def box(states, transitions, set_of_sets, action):
    """
    Berechnet das Ergebnis des Box-Operators für die gegebene Aktion der gegebenen Menge von Mengen

    :param states: die Menge aller Zustände
    :param transitions: die relation der Übergänge des Transitionssystems
    :param set_of_sets: eine Menge von Mengen, auf die der Box-Operator angewandt werden soll
    :param action: die Aktion des Box-Operators, die untersucht werden soll
    :return: eine Menge von Mengen, deren Elemente mit der gegebenen Aktion nur Übergänge in eine Teilmenge von
            set_of_sets besitzen
    """
    result = []
    for set_x in set_of_sets:
        interim_result = []
        for state in states:
            truth_values = []
            for transition in transitions:
                if (transition[0] == state) & (str(transition[1]) == action) & (transition[2] not in set_x):
                    truth_values.append(0)
                elif (transition[0] == state) & (str(transition[1]) == action) & (transition[2] in set_x):
                    truth_values.append(1)
            if (0 not in truth_values) & (truth_values != []):
                interim_result.append(state)
        interim_result.sort()
        if interim_result not in result:
            result.append(interim_result)
    return result
