import unicodedata
import difflib

# Fonction pour normaliser les noms (supprimer accents, mettre en minuscule)
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

# Fonction pour calculer la similarité avec Levenshtein (ou équivalent)
def levenshtein_similarity(s1: str, s2: str) -> float:
    seq_matcher = difflib.SequenceMatcher(None, s1, s2)
    return seq_matcher.ratio()

# Fonction pour évaluer la correspondance entre deux identités
def compare_identities(
    name1: str, first_name1: str, lang1: str,
    name2: str, first_name2: str, lang2: str
) -> float:
    """
    Compare two identities based on their names and first names using a weighted Levenshtein similarity score.

    Parameters:
    name1 (str): The name of the first identity.
    first_name1 (str): The first name of the first identity.
    lang1 (str): The language of the first identity.
    name2 (str): The name of the second identity.
    first_name2 (str): The first name of the second identity.
    lang2 (str): The language of the second identity.

    Returns:
    float: A percentage representing the similarity between the two identities. The score is calculated
    by normalizing the names and first names, comparing them using a Levenshtein similarity algorithm,
    and averaging the results. The final score is rounded to two decimal places.
    """
    # Normalisation
    name1, first_name1 = normalize_name(name1), normalize_name(first_name1)
    name2, first_name2 = normalize_name(name2), normalize_name(first_name2)

    # Similarité sur les noms
    name_similarity = levenshtein_similarity(name1, name2)
    # Similarité sur les prénoms
    first_name_similarity = levenshtein_similarity(first_name1, first_name2)

    # Calcul du score global (poids égal pour noms et prénoms)
    overall_similarity = (name_similarity + first_name_similarity) / 2

    # Convertir en pourcentage
    return round(overall_similarity * 100, 2)

# Fonction principale (interaction utilisateur)
def main():
    print("Entrez les informations pour les deux identités :")
    # Entrée des identités
    name1 = input("Nom 1 : ").strip()
    first_name1 = input("Prénom 1 : ").strip()
    lang1 = input("Langue 1 : ").strip()

    name2 = input("Nom 2 : ").strip()
    first_name2 = input("Prénom 2 : ").strip()
    lang2 = input("Langue 2 : ").strip()

    # Calcul de la probabilité
    probability = compare_identities(name1, first_name1, lang1, name2, first_name2, lang2)

    # Résultat
    print(f"Probabilité que les deux identités appartiennent à la même personne : {probability} %")

if __name__ == "__main__":
    main()
