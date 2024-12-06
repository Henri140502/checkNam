import unicodedata
from googletrans import Translator, LANGUAGES      # Use this command to install the googletrans library : pip install googletrans==4.0.0-rc1
import difflib
import tkinter as tk
from tkinter import messagebox

def normalize_name(name: str) -> str:
    """
    Normalize a given name by removing accents and converting it to lowercase.

    Parameters:
    name (str): The input name to be normalized.

    Returns:
    str: The normalized name.
    """
    return ''.join(
        char for char in unicodedata.normalize('NFD', name)
        if unicodedata.category(char) != 'Mn'
    ).lower()

def translate_name_api(name: str, target_lang: str, src_lang: str) -> str:
    """
    Translate a given name from one language to another using Google Translate API.

    Parameters:
    name (str): The input name to be translated.
    target_lang (str): The target language code (ISO 639-1) to translate the name into.
    src_lang (str): The source language code (ISO 639-1) of the input name. If not provided, the API will auto-detect the language.

    Returns:
    str: The translated name. If an error occurs during translation, the original name is returned.
    """
    translator = Translator()
    try:
        translated = translator.translate(name, dest=target_lang, src=src_lang).text
        return translated
    except Exception as e:
        print(f"Translation error: The probabilistic calculation will be done without translation, the result can be affected \n {e}")
        return name

def levenshtein_similarity(s1: str, s2: str) -> float:
    seq_matcher = difflib.SequenceMatcher(None, s1, s2)
    return seq_matcher.ratio()

def compare_identities(name1: str, first_name1: str, lang1: str, name2: str, first_name2: str, lang2: str) -> float:
    """
    Compares two identities based on their names and first names, considering language translation and similarity metrics.

    Parameters:
    name1 (str): The name of the first identity.
    first_name1 (str): The first name of the first identity.
    lang1 (str): The language code (ISO 639-1) of the first identity's name and first name.
    name2 (str): The name of the second identity.
    first_name2 (str): The first name of the second identity.
    lang2 (str): The language code (ISO 639-1) of the second identity's name and first name.

    Returns:
    float: A percentage representing the similarity between the two identities based on their names and first names.
    """
    name1, first_name1 = normalize_name(name1), normalize_name(first_name1)
    name2, first_name2 = normalize_name(name2), normalize_name(first_name2)
    name2_translated = translate_name_api(name2, target_lang=lang1, src_lang=lang2)
    first_name2_translated = translate_name_api(first_name2, target_lang=lang1, src_lang=lang2)
    name_similarity = levenshtein_similarity(name1, normalize_name(name2_translated))
    first_name_similarity = levenshtein_similarity(first_name1, normalize_name(first_name2_translated))
    overall_similarity = (name_similarity + first_name_similarity) / 2
    return round(overall_similarity * 100, 2)

def launch_ui():
    def update_language_list(entry, listbox, lang_options):
        search_term = entry.get().lower()
        listbox.delete(0, tk.END)
        filtered_languages = [lang for lang in lang_options if lang.startswith(search_term)]
        for lang in filtered_languages:
            listbox.insert(tk.END, lang)

    def select_language(event, entry, listbox):
        selection = listbox.get(tk.ACTIVE)
        entry.delete(0, tk.END)
        entry.insert(0, selection)

    def calculate_similarity():
        name1 = name1_entry.get().strip()
        first_name1 = first_name1_entry.get().strip()
        lang1 = lang1_entry.get().strip()

        name2 = name2_entry.get().strip()
        first_name2 = first_name2_entry.get().strip()
        lang2 = lang2_entry.get().strip()

        if not ([name1, first_name1, name2, first_name2]):
            messagebox.showerror("Error", "Please enter the following fields: Name 1, First name 1, Name 2 and First name 2")
            return

        try:
            similarity = compare_identities(name1, first_name1, lang1, name2, first_name2, lang2)
            messagebox.showinfo("Résultat", f"La probabilité que les deux identités appartiennent à la même personne est de {similarity} %")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    root = tk.Tk()
    root.title("Comparaison d'identités")
    root.geometry("600x400")

    lang_options = sorted(LANGUAGES.keys())

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    for row in range(8):
        root.rowconfigure(row, weight=1)

    tk.Label(root, text="Nom 1").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
    name1_entry = tk.Entry(root)
    name1_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.E+tk.W)

    tk.Label(root, text="Prénom 1").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
    first_name1_entry = tk.Entry(root, width=30)
    first_name1_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.E+tk.W)

    tk.Label(root, text="Langue 1 :").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
    lang1_entry = tk.Entry(root, width=30)
    lang1_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.E+tk.W)

    lang1_listbox = tk.Listbox(root, height=5)
    lang1_listbox.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E+tk.W)
    lang1_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=lang1_listbox.yview)
    lang1_listbox.config(yscrollcommand=lang1_scroll.set)
    lang1_scroll.grid(row=3, column=2, padx=10, sticky=tk.N+tk.S)
    lang1_entry.bind('<KeyRelease>', lambda event: update_language_list(lang1_entry, lang1_listbox, lang_options))
    lang1_listbox.bind('<ButtonRelease-1>', lambda event: select_language(event, lang1_entry, lang1_listbox))

    tk.Label(root, text="Nom 2 :").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
    name2_entry = tk.Entry(root)
    name2_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W + tk.E)

    tk.Label(root, text="Prénom 2 :").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
    first_name2_entry = tk.Entry(root)
    first_name2_entry.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W + tk.E)

    tk.Label(root, text="Langue 2 :").grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)
    lang2_entry = tk.Entry(root)
    lang2_entry.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W + tk.E)

    lang2_listbox = tk.Listbox(root, height=5)
    lang2_listbox.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W + tk.E)
    lang2_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=lang2_listbox.yview)
    lang2_listbox.configure(yscrollcommand=lang2_scroll.set)
    lang2_scroll.grid(row=7, column=2, sticky=tk.N + tk.S)
    lang2_entry.bind('<KeyRelease>', lambda event: update_language_list(lang2_entry, lang2_listbox, lang_options))
    lang2_listbox.bind('<ButtonRelease-1>', lambda event: select_language(event, lang2_entry, lang2_listbox))

    tk.Button(root, text="Calculer", command=calculate_similarity).grid(row=8, columnspan=3, pady=10, sticky=tk.E+tk.W)

    root.mainloop()

if __name__ == "__main__":
    launch_ui()