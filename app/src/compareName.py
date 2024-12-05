import unicodedata
from googletrans import Translator      # Use this command to install the googletrans library : pip install googletrans==4.0.0-rc1
import difflib

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
        print(f"Translation error: {e}")
        return name

def levenshtein_similarity(s1: str, s2: str) -> float:
    seq_matcher = difflib.SequenceMatcher(None, s1, s2)
    return seq_matcher.ratio()

def compare_identities(
    name1: str, first_name1: str, lang1: str,
    name2: str, first_name2: str, lang2: str
) -> float:
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

# Fonction principale (interaction utilisateur)
def main():
    print("Entrez les informations pour les deux identités :")
    """
    name1 = input("Nom 1 : ").strip()
    first_name1 = input("Prénom 1 : ").strip()
    lang1 = input("Langue 1 (code ISO, ex. 'fr') : ").strip()

    name2 = input("Nom 2 : ").strip()
    first_name2 = input("Prénom 2 : ").strip()
    lang2 = input("Langue 2 (code ISO, ex. 'en') : ").strip()
    """
    name1 = "Henri"
    first_name1 = "Charonnet"
    lang1 = "fr"
    name2 = "Henry"
    first_name2 = "Charonnet"
    lang2 = "en"
    probability = compare_identities(name1, first_name1, lang1, name2, first_name2, lang2)

    print(f"Probabilité que les deux identités appartiennent à la même personne : {probability} %")

if __name__ == "__main__":
    main()
