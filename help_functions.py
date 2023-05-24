def create_cartesian_products_sets(set_of_sets):
    """
    Erstellt das kartesische Produkt einer Menge von Mengen mit sich selbst

    :param set_of_sets: eine Menge von Mengen
    :return: eine Äquivalenzrelation, die dem kartesischen Produkt der Menge von Mengen mit sich selbst entspricht
    """
    cartesian_product = []
    for set_x in set_of_sets:
        if not set_x:
            continue
        for set_y in set_of_sets:
            if not set_y:
                continue
            cartesian_product.append((set_x, set_y))
    return cartesian_product


def create_cartesian_product(states):
    """
    Erstellt das kartesische Produkt einer Menge mit sich selbst.

    :param states: eine Menge
    :return: eine Äquivalenzrelation, die dem kartesischen Produkt der Menge mit sich selbst entspricht
    """
    cartesian_product = []
    for state_x in states:
        for state_y in states:
            cartesian_product.append((state_x, state_y))
    return cartesian_product


def powerset(states):
    """
    Erstellt die Potenzmenge einer Menge

    :param states: eine Menge
    """
    if len(states) <= 0:
        yield []
    else:
        for item in powerset(states[1:]):
            yield [states[0]] + item
            yield item


def intersection(set_x, set_y):
    """
    Schneidet zwei Mengen miteinander.

    :param set_x: Menge 1
    :param set_y: Menge 2
    :return: der Schnitt der beiden Mengen
    """
    intersect = []
    for element in set_x:
        if element in set_y:
            intersect.append(element)
    return intersect


def union(set_x, set_y):
    """
    Vereinigt zwei Mengen miteinander.

    :param set_x: Menge 1
    :param set_y: Menge 2
    :return: die Vereinigung der beiden Mengen
    """
    unified_set = []
    for x in set_x:
        if x not in unified_set:
            unified_set.append(x)
    for y in set_y:
        if y not in unified_set:
            unified_set.append(y)
    return unified_set


def complement(set_x, superset):
    """
    Erstellt das Komplement einer Menge.

    :param set_x: eine Menge
    :param superset: die übergeordnete Menge aller Elemente
    :return: das Komplement der Menge
    """
    complement_set = []
    for x in superset:
        if x not in set_x:
            complement_set.append(x)
    return complement_set


def conclusion_intersection(set_x):
    """
    Schließt eine Menge von Mengen unter Schnitt ab.

    :param set_x: eine Menge von Mengen
    :return: eine Menge von Mengen, die dem Abschluss unter Schnitt der Menge von Mengen entspricht
    """
    intersection_closing_set = []
    for x in set_x:
        for y in set_x:
            intersection_set = intersection(x, y)
            intersection_set.sort()
            if intersection_set not in intersection_closing_set:
                intersection_closing_set.append(intersection_set)
    return intersection_closing_set


def conclusion_union(set_x):
    """
    Schließt eine Menge von Mengen unter Vereinigung ab.

    :param set_x: eine Menge von Mengen
    :return: eine Menge von Mengen, die dem Abschluss unter Vereinigung der Menge von Mengen entspricht
    """
    unification_closing_set = []
    for x in set_x:
        for y in set_x:
            unification_set = union(x, y)
            unification_set.sort()
            if unification_set not in unification_closing_set:
                unification_closing_set.append(unification_set)
    return unification_closing_set


def conclusion_complement(set_x, superset):
    """
    Schließt eine Menge von Mengen unter Schnitt ab.

    :param set_x: eine Menge von Mengen
    :param superset: die übergeornete Menge von Mengen, die alle möglichen Mengen enthält
    :return: eine Menge von Mengen, die dem Abschluss unter Komplement der Menge von Mengen entspricht
    """
    complement_closing_set = []
    for x in set_x:
        complement_set = complement(x, superset)
        complement_set.sort()
        if complement_set not in complement_closing_set:
            complement_closing_set.append(complement_set)
    complement_closing_set = union(complement_closing_set, set_x)
    return complement_closing_set


def create_equivalence_classes(relation):
    """
    Erstellt die Äquivalenzklassen einer Relation.

    :param relation: eine Relation
    :return: eine Liste, die immer zuerst den Namen der Äquivalenzklasse und anschließend die Elemente dieser als Liste
            enthält
    """
    equivalence_classes_list = []
    relation.sort()
    for tuple_x in relation:
        equivalence_class_name = tuple_x[0]
        if equivalence_class_name not in equivalence_classes_list:
            equivalence_classes_list.append(equivalence_class_name)
        else:
            continue
        equivalence_class_elements = []
        for tuple_y in relation:
            if tuple_y[0] != equivalence_class_name:
                continue
            else:
                equivalence_class_elements.append(tuple_y[1])
        equivalence_classes_list.append(equivalence_class_elements)
    return equivalence_classes_list


def specify_equivalent_equivalence_classes(equivalence_classes_list):
    """
    Erstellt aus einer Liste, die den Namen und die Elemente aller Äquivalenzklassen enthält, einen String mit den
    äquivalenten Äquivalenzklassen ohne deren Elemente.

    :param equivalence_classes_list: Menge von Mengen, die die Namen und Elemente aller Äquivalenzklassen enthält
    :return: einen String, in dem alle äquivalenten Äquivalenzklassen durch ein '=' verbunden sind.
    """
    equivalence_classes_string = ''
    equivalence_list = []
    for i in range(0, len(equivalence_classes_list), 2):
        class_to_compare = equivalence_classes_list[i]
        list_to_compare = equivalence_classes_list[i + 1]
        class_string = str(class_to_compare)
        class_list = [class_to_compare]
        for j in range(0, len(equivalence_classes_list), 2):
            second_class = equivalence_classes_list[j]
            second_list = equivalence_classes_list[j + 1]
            if (list_to_compare == second_list) & (class_to_compare != second_class):
                class_string += ' = ' + str(second_class)
                class_list.append(second_class)
        counter = 0
        for element in class_list:
            if element in equivalence_list:
                break
            equivalence_list.append(element)
            counter += 1
            if counter == len(class_list):
                equivalence_classes_string += class_string + '\n'
    return equivalence_classes_string
