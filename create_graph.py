import graphviz


def create_graph(states, transitions):
    """
    Erstellt das Bild des Transitionssystems.

    :param states: die Menge aller Zustände
    :param transitions: die relation der Übergänge des Transitionssystems
    """
    graph = graphviz.Digraph('Graph', filename='transition_system')
    for state in states:
        graph.node(str(state), str(state))
    for transition in transitions:
        graph.edge(str(transition[0]), str(transition[2]), label=str(transition[1]))
    graph.render(format='png')
