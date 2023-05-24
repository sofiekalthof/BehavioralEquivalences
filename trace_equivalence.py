from alpha import alpha_t
from gamma import gamma_t
from log_function import log_function, fixpoint_log


def trace_equivalence_beh(states, transitions, logic_function_components, potency_set, cartesian_product_potency,
                          relation, beh_i):
    """
   Berechnet die Sprachäquivalenz mithilfe des Fixpunktes der Verhaltensfunktion

   :param states: die Menge aller Zustände des Transitionssystems
   :param transitions: die Relation der Übergänge des Transitionssystems
   :param logic_function_components: die gewählten Komponenten der Logikfunktion
   :param potency_set: die Potenzmenge der Menge aller Zustände
   :param cartesian_product_potency: das kartesische Produkt der Potenzmenge aller Zustände mit sich selbst
   :param relation: eine Äquivalenzrelation
   :param beh_i: das Ergebnis der Berechnung der Verhaltensfunktion aus der vorherigen Iteration
   :return: eine Äquivalenzrelation, die dem Ergebnis der Sprachäquivalenz des Transitionssystems entspricht
   """
    set_of_sets = gamma_t(potency_set, relation)
    log = log_function(states, transitions, logic_function_components, set_of_sets)
    beh = alpha_t(cartesian_product_potency, log)
    if beh != beh_i:
        beh_i1 = trace_equivalence_beh(states, transitions, logic_function_components, potency_set,
                                       cartesian_product_potency, beh, beh)
    else:
        beh_i1 = beh
    return beh_i1


def trace_equivalence_log(states, transitions, logic_function_components, cartesian_product_potency, set_of_sets,
                          log_i):
    """
    Berechnet die Sprachäquivalenz mithilfe des Fixpunktes der Logikfunktion

    :param states: die Menge aller Zustände des Transitionssystems
    :param transitions: die Relation der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param cartesian_product_potency: das kartesische Produkt der Potenzmenge aller Zustände mit sich selbst
    :param set_of_sets: eine Menge von Mengen
    :param log_i: Startpunkt der Berechnung des Fixpunktes
    :return: eine Äquivalenzrelation, die dem Ergebnis der Sprachäquivalenz des Transitionssystems entspricht
    """
    log = fixpoint_log(states, transitions, logic_function_components, set_of_sets, log_i)
    return alpha_t(cartesian_product_potency, log)
