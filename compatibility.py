from alpha import alpha_t, alpha_b
from gamma import gamma_t, gamma_b
from log_function import log_function


def compatibility_b(states, transitions, logic_function_components, potency_set, cartesian_product):
    """
    Überprüft die Kompatibilität der Logikfunktion für den Fall der Bisimularität.

    :param states: die Menge aller Zustände
    :param transitions: die Relation der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param potency_set: die Potenzmenge der Menge aller Zustände
    :param cartesian_product: das kartesische Produkt der Menge aller Zustände mit sich selbst
    :return: True, wenn die Logikfunktion kompatibel und False, wenn sie nicht kompatibel ist
    """
    left_side = log_function(states, transitions, logic_function_components,
                             gamma_b(potency_set,
                                     alpha_b(cartesian_product, potency_set)))
    right_side = gamma_b(potency_set,
                         alpha_b(cartesian_product,
                                 log_function(states, transitions, logic_function_components, potency_set)))
    for element in left_side:
        if element not in right_side:
            return False
    return True


def compatibility_t(states, transitions, logic_function_components, potency_set, cartesian_product):
    """
    Überprüft die Kompatibilität der Logikfunktion für den Fall der Sprachäquivalenz.

    :param states: die Menge aller Zustände
    :param transitions: die Relation der Übergänge des Transitionssystems
    :param logic_function_components: die gewählten Komponenten der Logikfunktion
    :param potency_set: die Potenzmenge der Menge aller Zustände
    :param cartesian_product: das kartesische Produkt der Potenzmenge aller Zustände mit sich selbst
    :return: True, wenn die Logikfunktion kompatibel und False, wenn sie nicht kompatibel ist
    """
    left_side = log_function(states, transitions, logic_function_components,
                             gamma_t(potency_set,
                                     alpha_t(cartesian_product, potency_set)))
    right_side = gamma_t(potency_set,
                         alpha_t(cartesian_product,
                                 log_function(states, transitions, logic_function_components, potency_set)))
    for element in left_side:
        if element not in right_side:
            return False
    return True
