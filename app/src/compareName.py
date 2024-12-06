import unicodedata

import googletrans
from googletrans import Translator      # Use this command to install the googletrans library : pip install googletrans==4.0.0-rc1
import difflib
import tkinter as tk
from tkinter import messagebox, ttk

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
        print(f"Translation error: The probabilistic calculation will be done without translation, the result can be affected")
        return name

def levenshtein_similarity(s1: str, s2: str) -> float:
    seq_matcher = difflib.SequenceMatcher(None, s1, s2)
    return seq_matcher.ratio()

def compare_identities(
    name1: str, first_name1: str, lang1: str, name2: str, first_name2: str, lang2: str) -> float:
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
    def calculate_similarity():
        name1 = name1_entry.get().strip()
        first_name1 = first_name1_entry.get().strip()
        lang1 = lang1_combobox.get()

        name2 = name2_entry.get().strip()
        first_name2 = first_name2_entry.get().strip()
        lang2 = lang2_combobox.get()

        if not ([name1, first_name1, lang1, name2, first_name2, lang2]):
            messagebox.showerror("Error", "Please enter all fields")
            return

        try:
            similarity = compare_identities(name1, first_name1, lang1, name2, first_name2, lang2)
            messagebox.showinfo("Résultat", f"La probabilité que les deux identités appartiennent à la même personne est de {similarity} %")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    root = tk.Tk()
    root.title("Comparaison d'identités")

    lang_options = list(googletrans.LANGUAGES.keys())

    tk.Label(root, text="Nom 1").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    name1_entry = tk.Entry(root, width=30)
    name1_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Prénom 1").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    first_name1_entry = tk.Entry(root, width=30)
    first_name1_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Langue 1").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    lang1_combobox = ttk.Combobox(root, values=lang_options, width=30)
    lang1_combobox.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Nom 2").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    name2_entry = tk.Entry(root, width=30)
    name2_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Prénom 2").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    first_name2_entry = tk.Entry(root, width=30)
    first_name2_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(root, text="Langue 2").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
    lang2_combobox = ttk.Combobox(root, values=lang_options, width=30)
    lang2_combobox.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(root, text="Calculer", command=calculate_similarity).grid(row=6, column=1, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    launch_ui()