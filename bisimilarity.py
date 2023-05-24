from alpha import alpha_b
from gamma import gamma_b
from log_function import log_function, fixpoint_log


def bisimilarity_beh(states, transitions, logic_function_components, potency_set, cartesian_product, relation, beh_i):
    """
    Berechnet die Bisimularität mithilfe des Fixpunktes der Verhaltensfunktion

    :param states: die Menge aller Zustände des Transitionssystems
    :param transitions: die Relation der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param potency_set: die Potenzmenge der Menge aller Zustände
    :param cartesian_product: das kartesische Produkt der Menge aller Zustände mit sich selbst
    :param relation: eine Äquivalenzrelation
    :param beh_i: das Ergebnis der Berechnung der Verhaltensfunktion aus der vorherigen Iteration
    :return: eine Äquivalenzrelation, die dem Ergebnis der Bisimularität des Transitionssystems entspricht
    """
    set_of_sets = gamma_b(potency_set, relation)
    log = log_function(states, transitions, logic_function_components, set_of_sets)
    beh = alpha_b(cartesian_product, log)
    if beh != beh_i:
        beh_i1 = bisimilarity_beh(states, transitions, logic_function_components, potency_set, cartesian_product, beh,
                                  beh)
    else:
        beh_i1 = beh
    return beh_i1


def bisimilarity_log(states, transitions, logic_function_components, cartesian_product, set_of_sets, log_i):
    """
    Berechnet die Bisimularität mithilfe des Fixpunktes der Logikfunktion

    :param states: die Menge aller Zustände des Transitionssystems
    :param transitions: die Relation der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param cartesian_product: das kartesische Produkt der Menge aller Zustände mit sich selbst
    :param set_of_sets: eine Menge von Mengen
    :param log_i: Startpunkt der Berechnung des Fixpunktes
    :return: eine Äquivalenzrelation, die dem Ergebnis der Bisimularität des Transitionssystems entspricht
    """
    log = fixpoint_log(states, transitions, logic_function_components, set_of_sets, log_i)
    return alpha_b(cartesian_product, log)
