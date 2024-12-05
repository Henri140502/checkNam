import unicodedata
from googletrans import Translator
import difflib

# Fonction pour normaliser les noms (supprimer accents, mettre en minuscule)
def normalize_name(name: str) -> str:
    return ''.join(
        char for char in unicodedata.normalize('NFD', name)
        if unicodedata.category(char) != 'Mn'
    ).lower()

# Fonction pour traduire un nom ou prénom dans une langue cible via Google Translate
def translate_name_api(name: str, target_lang: str, src_lang:str) -> str:
    translator = Translator()
    try:
        # Traduction via l'API
        translated = translator.translate(name, dest=target_lang, src=src_lang).text
        return translated
    except Exception as e:
        print(f"Erreur de traduction : {e}")
        return name  # Retourne le nom original en cas d'erreur

# Fonction pour calculer la similarité avec Levenshtein (ou équivalent)
def levenshtein_similarity(s1: str, s2: str) -> float:
    seq_matcher = difflib.SequenceMatcher(None, s1, s2)
    return seq_matcher.ratio()

# Fonction pour évaluer la correspondance entre deux identités
def compare_identities(
    name1: str, first_name1: str, lang1: str,
    name2: str, first_name2: str, lang2: str
) -> float:
    # Normalisation
    name1, first_name1 = normalize_name(name1), normalize_name(first_name1)
    name2, first_name2 = normalize_name(name2), normalize_name(first_name2)

    # Traduction des noms dans la langue de "lang1"
    name2_translated = translate_name_api(name2, target_lang=lang1, src_lang=lang2)
    first_name2_translated = translate_name_api(first_name2, target_lang=lang1, src_lang=lang2)

    # Similarité sur les noms
    name_similarity = levenshtein_similarity(name1, normalize_name(name2_translated))
    # Similarité sur les prénoms
    first_name_similarity = levenshtein_similarity(first_name1, normalize_name(first_name2_translated))

    # Calcul du score global (poids égal pour noms et prénoms)
    overall_similarity = (name_similarity + first_name_similarity) / 2

    # Convertir en pourcentage
    return round(overall_similarity * 100, 2)

# Fonction principale (interaction utilisateur)
def main():
    print("Entrez les informations pour les deux identités :")
    # Entrée des identités
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
    # Calcul de la probabilité
    probability = compare_identities(name1, first_name1, lang1, name2, first_name2, lang2)

    # Résultat
    print(f"Probabilité que les deux identités appartiennent à la même personne : {probability} %")

if __name__ == "__main__":
    main()
