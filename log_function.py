from box import box
from diamond import diamond
from help_functions import conclusion_intersection, conclusion_complement, conclusion_union, union


def create_conclusion(states, closing_list, set_of_sets):
    """
    Bestimmt unter welchen Operatoren eine Menge von Mengen abgeschlossen werden soll und berechnet diesen Abschluss.

    :param states: die Menge aller Zuständes
    :param closing_list: eine Liste, die die Werte der gewählten Operatoren enthält
    :param set_of_sets: die Menge von Mengen, die abgeschlossen werden soll
    :return: die abgeschlossene Mengen von Mengen
    """
    if closing_list == [1, 0, 0]:
        closing = conclusion_union(set_of_sets)
    elif closing_list == [0, 1, 0]:
        closing = conclusion_intersection(set_of_sets)
    elif closing_list == [0, 0, 1]:
        closing = conclusion_complement(set_of_sets, states)
    elif closing_list == [1, 1, 0]:
        union_conclusion = conclusion_union(set_of_sets)
        closing = conclusion_intersection(union_conclusion)
    elif closing_list == [1, 0, 1]:
        union_conclusion = conclusion_union(set_of_sets)
        closing = conclusion_complement(union_conclusion, states)
    elif closing_list == [0, 1, 1]:
        intersection_conclusion = conclusion_intersection(set_of_sets)
        closing = conclusion_complement(intersection_conclusion, states)
    elif closing_list == [1, 1, 1]:
        union_conclusion = conclusion_union(set_of_sets)
        intersection_union_conclusion = conclusion_intersection(union_conclusion)
        closing = conclusion_complement(intersection_union_conclusion, states)
    else:
        closing = set_of_sets
    return closing


def fixpoint_conclusion(states, closing_list, set_of_sets, closing_i):
    """
    Erstellt wiederholt den Abschluss einer Menge von Mengen, um die Menge von Mengen und ihre Zwischenergebnisse
    unter den gewählten Operatoren abzuschließen.

    :param states: die Menge aller Zustände
    :param closing_list: eine Liste, die die Werte der gewählten Operatoren enthält
    :param set_of_sets: die Menge von Mengen, die abgeschlossen werden soll
    :param closing_i: der Abschluss der vorherigen Iteration
    :return: den kompletten Abschluss der Menge von Mengen unter den gewählten Operatoren
    """
    closing = create_conclusion(states, closing_list, set_of_sets)
    closing.sort()
    if closing != closing_i:
        closing_i1 = fixpoint_conclusion(states, closing_list, closing, closing)
    else:
        closing_i1 = closing
    return closing_i1


def log_function(states, transitions, logic_function_components, set_of_sets):
    """
    Berechnet die Logikfunktion des Transitionssystems für eine gegebene Menge von Mengen.

    :param states: die Menge aller Zustände
    :param transitions: die Relation der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param set_of_sets: die Menge von Mengen, auf die die Operatoren der Logikfunktion angewandt werden sollen
    :return: eine Menge von Mengen, die dem Ergebnis der Logikfunktion für das Transitionssystem entspricht
    """
    log = []
    closing_list = logic_function_components.pop()
    closing = fixpoint_conclusion(states, closing_list, set_of_sets, [[]])
    for component in logic_function_components:
        if '<>' in component:
            action = component.split()[1]
            diamond_result = diamond(states, transitions, closing, action)
            log = union(log, diamond_result)
        if '[]' in component:
            action = component.split()[1]
            box_result = box(states, transitions, closing, action)
            log = union(log, box_result)
        if 'true' in component:
            log = union(log, [states])
    logic_function_components.append(closing_list)
    return log


def fixpoint_log(states, transitions, logic_function_components, set_of_sets, log_i):
    """
    Berechnet den Fixpunkt der Logikfunktion.

    :param states: die Menge aller Zustände
    :param transitions: die Relationd der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param set_of_sets: eine Menge von Mengen, auf die die Operatoren der Logikfunktion angewandt werden sollen
    :param log_i: das Ergebnis der Logikfunktion der vorherigen Iteration
    :return: eine Menge von Mengen, die dem Fixpunkt der Logikfunktion entspricht
    """
    log = log_function(states, transitions, logic_function_components, set_of_sets)
    log.sort()
    if log != log_i:
        log_i1 = fixpoint_log(states, transitions, logic_function_components, log, log)
    else:
        log_i1 = log
    return log_i1
