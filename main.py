import tkinter as tkinter
import tkinter.scrolledtext
from functools import partial
from tkinter import messagebox, filedialog

from bisimilarity import bisimilarity_beh, bisimilarity_log
from create_graph import create_graph
from help_functions import create_equivalence_classes, create_cartesian_product, create_cartesian_products_sets, \
    specify_equivalent_equivalence_classes, powerset
from trace_equivalence import trace_equivalence_beh, trace_equivalence_log

# folgende Zeile auskommentieren, wenn die Kompatibilität verwendet werden soll
# from compatibility import compatibility_t, compatibility_b


class Gui:
    # Initialisieren der Komponenten der Eingabeschnittstelle
    def __init__(self, master):
        # Einleitungstext des Werkzeugs
        self.introduction = ' Dieses Werkzeug berechnet die gewählte Verhaltensäquivalenz ' \
                            'mithilfe einer Logikfunktion für ein Transitionssystem.\n ' \
                            'Open from file: Übergänge des Transitionssystem \u0394 aus Datei einlesen ' \
                            '(ACHTUNG: Datei darf nur \u0394 enthalten!)\n ' \
                            'Save to file: Relation \u0394 in Datei speichern\n ' \
                            'New: löscht alle gemachten Eingaben\n ' \
                            'X: alle Zustände des Transitionssystems\n ' \
                            'A: alle Aktionen des Transitionssystems\n ' \
                            '\u0394: alle Übergänge des Transitionssystems\n ' \
                            '(WICHTIG: Namen von Aktionen oder Zuständen, die Strings entsprechen, müssen in ' \
                            'Anführungszeichen gesetzt werden!)\n ' \
                            'cl(S): Abschluss auf den die Operatoren der Logikfunktion angewandt werden sollen ' \
                            '(Vereinigung, Schnitt, Komplement)\n ' \
                            'log: zusammengesetzte Logikfunktion\n ' \
                            '\u00b5beh/\u03b1(\u00b5log): Ergebnis der Berechnung der gewählten Verhaltensäquivalenz\n'\
                            ' Insert: liest Transitionssystem ein und zeigt es an' \
                            ', zusätzlich werden daraus die Optionen für die Logikfunktion log erstellt\n ' \
                            '(WICHTIG: Änderungen am Transitionssystem nur sichtbar nach vorheriger Betätigung' \
                            ' des Buttons "Insert"!)\n ' \
                            'Calculate: startet Berechnung der gewählten Verhaltensäquivalenz'

        # Integer-Variablen
        self.equivalence = tkinter.IntVar()
        self.function = tkinter.IntVar()
        self.union_operator = tkinter.IntVar()
        self.intersection_operator = tkinter.IntVar()
        self.complement_operator = tkinter.IntVar()

        # Liste der Komponenten der Logikfunktion
        self.log_components = []

        # Komponente zum Anzeigen des Einleitungstexts
        self.introduction_text = tkinter.Message(master, text=self.introduction, width=750, bg='#f0f0f0', fg='black')

        # Buttons der Eingabeschnittstelle
        self.open_button = tkinter.Button(master, text='Open from file', width=10, height=2,
                                          highlightbackground='#f0f0f0',
                                          command=self.read_from_file)
        self.save_button = tkinter.Button(master, text='Save to file', width=10, height=2,
                                          highlightbackground='#f0f0f0',
                                          command=self.write_to_file)
        self.new_button = tkinter.Button(master, text='New', width=10, height=2, highlightbackground='#f0f0f0',
                                         command=self.delete_input)
        self.insert_button = tkinter.Button(master, text='Insert', width=10, height=2, highlightbackground='#f0f0f0',
                                            command=self.create_log)
        self.calculate_button = tkinter.Button(master, text='Calculate', width=10, height=2,
                                               highlightbackground='#f0f0f0',
                                               command=self.calculate_beh, state=tkinter.DISABLED)

        # Radiobuttons der Eingabeschnittstelle
        self.option_bisimilarity = tkinter.Radiobutton(master, text='Bisimularität', bg='#f0f0f0', fg='black',
                                                       variable=self.equivalence, value=1)
        self.option_trace = tkinter.Radiobutton(master, text='Sprachäquivalenz', bg='#f0f0f0', fg='black',
                                                variable=self.equivalence, value=2)
        self.option_beh = tkinter.Radiobutton(master, text='\u00b5beh', bg='#f0f0f0', fg='black',
                                              variable=self.function,
                                              value=1)
        self.option_log = tkinter.Radiobutton(master, text='\u03b1(\u00b5log)', bg='#f0f0f0', fg='black',
                                              variable=self.function,
                                              value=2)

        # Beschriftungen der einzelnen Komponenten der Eingabeschnittstelle
        self.equivalence_label = tkinter.Label(master, text='Äquivalenz:', width=10, bg='#f0f0f0', fg='black')
        self.function_label = tkinter.Label(master, text='Funktion:', bg='#f0f0f0', fg='black')
        self.x_label = tkinter.Label(master, text='X =', bg='#f0f0f0', fg='black')
        self.a_label = tkinter.Label(master, text='A =', bg='#f0f0f0', fg='black')
        self.transitions_label = tkinter.Label(master, text='\u0394', bg='#f0f0f0', fg='black')
        self.cl_label = tkinter.Label(master, text='cl(S):', bg='#f0f0f0', fg='black')
        self.log_label = tkinter.Label(master, text='log(S) =', bg='#f0f0f0', fg='black')
        self.result_label = tkinter.Label(master, text='\u00b5beh/\u03b1(\u00b5log)  =', width=10, bg='#f0f0f0',
                                          fg='black')

        # Label zum Anzeigen der zusammengesetzten Logikfunktion
        self.log_string = tkinter.Label(master, text='', bg='#f0f0f0', fg='black')
        # Der Platzhalter für das Transitionssystem
        self.transition_system = tkinter.Label(master, bg='#f0f0f0')

        # Textfelder der Eingabeschnittstelle
        self.x = tkinter.Text(master, width=70, height=2, bg='white', fg='black', highlightcolor='black',
                              highlightbackground='#f0f0f0', padx=3, borderwidth=3, relief=tkinter.RIDGE)
        self.a = tkinter.Text(master, width=70, height=2, bg='white', fg='black', highlightcolor='black',
                              highlightbackground='#f0f0f0', padx=3, borderwidth=3, relief=tkinter.RIDGE)
        self.transitions = tkinter.Text(master, width=70, height=2, bg='white', fg='black', highlightcolor='black',
                                        highlightbackground='#f0f0f0', padx=3, borderwidth=3, relief=tkinter.RIDGE)
        self.result = tkinter.scrolledtext.ScrolledText(master, width=70, height=18, bg='white', fg='black',
                                                        highlightcolor='black', highlightbackground='#f0f0f0',
                                                        padx=3, relief=tkinter.RIDGE, borderwidth=3,
                                                        state=tkinter.DISABLED)

        # Frames zum Generieren der einzelnen Buttons für die Optionen der Logikfunktion
        self.cl_frame = tkinter.Frame(master, bg='#f0f0f0')
        self.log_delete_frame = tkinter.Frame(master, bg='#f0f0f0')
        self.log_diamond_frame = tkinter.Frame(master, bg='#f0f0f0')
        self.log_box_frame = tkinter.Frame(master, bg='#f0f0f0')

        # Checkboxen zum Auswählen des Abschlusses, auf den die Operatoren der Logikfunktion angewandt werden
        self.union_checkbox = tkinter.Checkbutton(self.cl_frame, text='\u222A', bg='#f0f0f0', fg='black',
                                                  variable=self.union_operator)
        self.intersection_checkbox = tkinter.Checkbutton(self.cl_frame, text='\u2229', bg='#f0f0f0', fg='black',
                                                         variable=self.intersection_operator)
        self.complement_checkbox = tkinter.Checkbutton(self.cl_frame, text='S\u0305', bg='#f0f0f0', fg='black',
                                                       variable=self.complement_operator)

        # Anordnung der einzelnen Komponenten der Logikfunktion mittels grid
        self.open_button.grid(row=0, column=1, padx=5, pady=10, sticky=tkinter.W)
        self.new_button.grid(row=0, column=1)
        self.save_button.grid(row=0, column=1, padx=5, pady=10, sticky=tkinter.E)
        self.introduction_text.grid(row=0, column=2, columnspan=2, rowspan=6)

        self.equivalence_label.grid(row=1)
        self.option_bisimilarity.grid(row=1, column=1, sticky=tkinter.W)
        self.option_trace.grid(row=1, column=1, sticky=tkinter.E)
        self.transition_system.grid(row=5, column=2, rowspan=8, padx=20, pady=5)

        self.function_label.grid(row=2)
        self.option_beh.grid(row=2, column=1, sticky=tkinter.W)
        self.option_log.grid(row=2, column=1, sticky=tkinter.E)

        self.x_label.grid(row=3)
        self.x.grid(row=3, column=1, pady=3)
        self.x.insert(tkinter.END, "['zustand1', 'zustand2', ...]")

        self.a_label.grid(row=4)
        self.a.grid(row=4, column=1, pady=3)
        self.a.insert(tkinter.END, "['aktion1', 'aktion2', ...]")

        self.transitions_label.grid(row=5)
        self.transitions.grid(row=5, column=1, pady=3)
        self.transitions.insert(tkinter.END, "[('zustand1', 'aktion1', 'zustand2'), ...]")

        self.cl_label.grid(row=6)
        self.cl_frame.grid(row=6, column=1)
        self.union_checkbox.pack(side=tkinter.LEFT)
        self.intersection_checkbox.pack(side=tkinter.LEFT)
        self.complement_checkbox.pack(side=tkinter.LEFT)

        self.log_delete_frame.grid(row=7)
        self.log_diamond_frame.grid(row=7, column=1)

        self.log_box_frame.grid(row=8, column=1)

        self.log_label.grid(row=9)
        self.log_string.grid(row=9, column=1, pady=3)

        self.result_label.grid(row=10)
        self.result.grid(row=10, column=1, pady=3)

        self.calculate_button.grid(row=11, column=1, sticky=tkinter.E)
        self.insert_button.grid(row=11, column=1, sticky=tkinter.W)

    # Mengen X und A aus den eingegebenen Übergängen herleiten
    def insert_x_and_a(self, states, actions, transition_description):
        for transition in transition_description:
            if transition[0] not in states:
                states.append(transition[0])
            if transition[1] not in actions:
                actions.append(transition[1])
            if transition[2] not in states:
                states.append(transition[2])
        states.sort()
        self.x.delete('0.0', 'end')
        self.a.delete('0.0', 'end')
        self.x.insert(tkinter.END, str(states))
        self.a.insert(tkinter.END, str(actions))

    # Ausgewählten Teil der Logikfunktion dem String und der Liste der Logikfunktion anhängen
    def insert_log(self, action):
        log_text = self.log_string.cget('text')
        log_text += ' ' + action + ' '
        self.log_string.configure(text=log_text)
        self.log_components.append(action)
        self.calculate_button.configure(state=tkinter.NORMAL)

    # Das Ergebnis der Berechnung in das dafür vorgesehene Textfeld eintragen
    def insert_beh(self, beh):
        self.result.configure(state=tkinter.NORMAL)
        self.result.delete('0.0', 'end')
        self.result.insert(tkinter.END, str(beh))
        self.result.configure(state=tkinter.DISABLED)

    # Logikfunktion auf das richtige Format überprüfen
    def verify_log(self):
        counter = 1
        for component in self.log_components:
            if ((component != '∪') & (counter % 2 == 0)) | ((component == '∪') & (counter % 2 != 0)):
                messagebox.showerror('Fehler', 'Die Logikfunktion hat das falsche Format')
                return False
            counter += 1
        return True

    # Nutzereingaben auf das richtige Format überprüfen
    def verify_entries(self):
        try:
            tr = eval(self.transitions.get('1.0', 'end'))
            ac = eval(self.a.get('1.0', 'end'))
            z = eval(self.x.get('1.0', 'end'))
        except SyntaxError:
            messagebox.showerror('Fehler', 'Eine der eingegebenen Mengen hat das falsche Format')
            return False
        except NameError:
            messagebox.showerror('Fehler', 'Strings müssen in Anführungszeichen gesetzt werden')
            return False
        if (tr != [('zustand1', 'aktion1', 'zustand2'), ...]) & (isinstance(tr, list)):
            if (z == ['zustand1', 'zustand2', ...]) & (
                    ac != ['aktion1', 'aktion2', ...]) & (isinstance(ac, list)):
                self.insert_x_and_a([], ac, tr)
                return True
            elif (z != ['zustand1', 'zustand2', ...]) & (
                    ac == ['aktion1', 'aktion2', ...]) & (isinstance(z, list)):
                self.insert_x_and_a(z, [], tr)
                return True
            elif (z == ['zustand1', 'zustand2', ...]) & (
                    ac == ['aktion1', 'aktion2', ...]):
                self.insert_x_and_a([], [], tr)
                return True
            elif (z != ['zustand1', 'zustand2', ...]) & (
                    ac != ['aktion1', 'aktion2', ...]) & (isinstance(z, list)) & (isinstance(ac, list)):
                self.insert_x_and_a(z, ac, tr)
                return True
            else:
                messagebox.showerror('Fehler', 'Eine der eingegebenen Mengen hat das falsche Format')
                return False
        else:
            messagebox.showerror('Fehler', 'Die Liste der Übergänge fehlt oder hat das falsche Format')
            return False

    # Alle Buttons zum Zusammensetzen der Logikfunktion löschen
    def delete_log_components(self):
        for widget in self.log_diamond_frame.winfo_children():
            widget.destroy()
        for widget in self.log_box_frame.winfo_children():
            widget.destroy()
        for widget in self.log_delete_frame.winfo_children():
            widget.destroy()

    # Löschen der zusammengesetzten Logikfunktion und Leeren der Liste der Komponenten der Logikfunktion
    def delete_log_function(self):
        self.log_string.configure(text='')
        self.log_components.clear()
        self.calculate_button.configure(state=tkinter.DISABLED)

    # Alle Eingaben löschen
    def delete_input(self):
        self.x.delete('0.0', 'end')
        self.x.insert(tkinter.END, "['zustand1', 'zustand2', ...]")
        self.a.delete('0.0', 'end')
        self.a.insert(tkinter.END, "['aktion1', 'aktion2', ...]")
        self.transitions.delete('0.0', 'end')
        self.transitions.insert(tkinter.END, "[('zustand1', 'aktion1', 'zustand2'), ...]")
        self.result.configure(state=tkinter.NORMAL)
        self.result.delete('0.0', 'end')
        self.result.configure(state=tkinter.DISABLED)
        self.transition_system.configure(image='')
        self.delete_log_components()
        self.delete_log_function()

    # Übergänge des Transitionssystems aus einer Datei einlesen
    def read_from_file(self):
        self.delete_input()
        filename = filedialog.askopenfilename()
        try:
            file = open(filename, 'r')
            file_content = file.read()
            self.transitions.delete('0.0', 'end')
            self.insert_x_and_a([], [], eval(file_content))
            self.transitions.insert(tkinter.END, file_content)
        except FileNotFoundError:
            messagebox.showerror('Fehler', 'Die Datei konnte nicht gelesen werden')

    # Übergänge des Transitionssystems in einer Datei speichern
    def write_to_file(self):
        filename = filedialog.asksaveasfilename()
        try:
            file = open(filename, 'w')
            content_to_write = eval(self.transitions.get('1.0', 'end'))
            file.write(str(content_to_write))
        except FileNotFoundError:
            messagebox.showerror('Fehler', 'Die Datei konnte nicht gespeichert werden')

    # Graph aus den Zuständen und Übergängen des Transitionssystems erstellen
    def draw_graph(self):
        try:
            states = eval(self.x.get('1.0', 'end'))
            transition_description = eval(self.transitions.get('1.0', 'end'))
            create_graph(states, transition_description)
            lattice = tkinter.PhotoImage(file='transition_system.png')
            self.transition_system.config(image=lattice)
            self.transition_system.image = lattice
        except TypeError:
            self.transition_system.config(image='')

    # Optionen zum Zusammensetzen der Logikfunktion abhängig von den Aktionen des Transitionssystems erstellen
    def create_log(self):
        self.delete_log_components()
        self.delete_log_function()
        if self.verify_entries():
            self.draw_graph()
            union_button = tkinter.Button(self.log_diamond_frame, text='\u222A',
                                          command=partial(self.insert_log, '\u222A'), highlightbackground='#f0f0f0')
            union_button.pack(side=tkinter.LEFT)
            true_button = tkinter.Button(self.log_box_frame, text='true', command=partial(self.insert_log, 'true'),
                                         highlightbackground='#f0f0f0')
            true_button.pack(side=tkinter.LEFT)
            actions = eval(self.a.get('1.0', 'end'))
            for action in actions:
                # Buttons des Diamant-Operators
                diamond_button_text_s = '<> ' + str(action) + ' cl(S)'
                diamond_button_s = tkinter.Button(self.log_diamond_frame,
                                                  text=diamond_button_text_s,
                                                  command=partial(self.insert_log, diamond_button_text_s),
                                                  highlightbackground='#f0f0f0')
                diamond_button_s.pack(side=tkinter.LEFT)

                # Buttons des Box-Operators
                box_button_text_s = '[] ' + str(action) + ' cl(S)'
                box_button_s = tkinter.Button(self.log_box_frame,
                                              text=box_button_text_s,
                                              command=partial(self.insert_log, box_button_text_s),
                                              highlightbackground='#f0f0f0')
                box_button_s.pack(side=tkinter.LEFT)
            # Button zum Löschen der Logikfunktion erstellen
            delete_button = tkinter.Button(self.log_delete_frame, text='delete', command=self.delete_log_function,
                                           highlightbackground='#f0f0f0')
            delete_button.pack()

    # Gewählte Verhaltensäquivalenz und Weise der Berechnung bestimmen und anschließend berechnen
    def calculate_beh(self):
        if self.verify_log():
            states = eval(self.x.get('1.0', 'end'))
            transition_description = eval(self.transitions.get('1.0', 'end'))
            # Liste der Komponenten der Logikfunktion eine Liste der Werte der Checkboxen des Abschlusses anhängen
            self.log_components.append(
                [self.union_operator.get(), self.intersection_operator.get(), self.complement_operator.get()])
            if self.equivalence.get() == 1:
                # Berechnung der Bisimularität
                potency_x = [p for p in powerset(states)]
                cartesian_product = create_cartesian_product(states)

                '''Wenn die Kompatibilität der Bisimularität überprüft werden soll, muss die Raute vor der folgenden
                Zeile und dem auskommentierten else-Zweig gelöscht werden. Zusätzlich müssen dann if...elif...else...
                um eine Stelle weiter eingerückt werden.'''
                # if compatibility_b(states, transition_description, self.log_components, potency_x, cartesian_product):

                if self.function.get() == 1:
                    # Berechnung über den Fixpunkt der Verhaltensfunktion
                    beh = bisimilarity_beh(states, transition_description, self.log_components, potency_x,
                                           cartesian_product,
                                           cartesian_product, [])
                    self.insert_beh(beh)
                elif self.function.get() == 2:
                    # Berechnung über den Fixpunkt der Logikfunktion
                    beh = bisimilarity_log(states, transition_description, self.log_components, cartesian_product,
                                           [[]], [[]])
                    self.insert_beh(beh)
                else:
                    messagebox.showerror('Fehler', 'Sie haben nicht ausgewählt, auf welche Weise die Bisimularität'
                                                   'berechnet werden soll')
                # else:
                #    messagebox.showerror('Fehler', 'Die Logikfunktion ist nicht kompatibel')
            elif self.equivalence.get() == 2:
                # Berechnung der Sprachäquivalenz
                potency_x = [p for p in powerset(states)]
                cartesian_product_potency = create_cartesian_products_sets(potency_x)

                '''Wenn die Kompatibilität der Sprachäquivalenz überprüft werden soll, muss die Raute vor der folgenden
                 Zeile und dem auskommentierten else-Zweig gelöscht werden. Zusätzlich müssen dann if...elif...else...
                 um eine Stelle weiter eingerückt werden.'''
                # if compatibility_t(states, transition_description, self.log_components, potency_x,
                # cartesian_product_potency):

                if self.function.get() == 1:
                    # Berechnung über den Fixpunkt der Verhaltensfunktion
                    beh = trace_equivalence_beh(states, transition_description, self.log_components, potency_x,
                                                cartesian_product_potency, cartesian_product_potency, [])
                    beh_equivalence_classes = create_equivalence_classes(beh)
                    beh_string = specify_equivalent_equivalence_classes(beh_equivalence_classes)
                    self.insert_beh(beh_string)
                elif self.function.get() == 2:
                    # Berechnung über den Fixpunkt der Logikfunktion
                    beh = trace_equivalence_log(states, transition_description, self.log_components,
                                                cartesian_product_potency, [[]], [[]])
                    beh_equivalence_classes = create_equivalence_classes(beh)
                    beh_string = specify_equivalent_equivalence_classes(beh_equivalence_classes)
                    self.insert_beh(beh_string)
                else:
                    messagebox.showerror('Fehler',
                                         'Sie haben nicht ausgewählt, auf welche Weise die Sprachäquivalenz'
                                         'berechnet werden soll')
                # else:
                #    messagebox.showerror('Fehler', 'Die Logikfunktion ist nicht kompatibel')
            else:
                messagebox.showerror('Fehler', 'Sie haben nicht ausgewählt, ob die Bisimularität'
                                     + 'oder die Sprachäquivalenz berechnet berechnet werden soll')
        self.log_components.pop()


def main():
    master = tkinter.Tk()
    master.title('Werkzeug zur Berechnung von Verhaltensäquivalenzen basierend auf Modallogiken')
    master.geometry('1400x700')
    master.configure(bg='#f0f0f0')
    Gui(master)
    master.mainloop()


if __name__ == '__main__':
    main()
