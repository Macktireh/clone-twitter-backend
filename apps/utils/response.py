


def error_messages(type, lang, field):
    if type == "blank":
        return f"Le champ {field} ne doit pas être vide."
    if type == "required":
        return f"Le champ {field} est obligatoire."

def messages(lang):
    if lang == 'fr':
        return {
            "PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH": "Le mot de passe et le mot de passe de confirmation ne correspondent pas",
            "TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED": "Le jeton n'est pas valide ou a expiré",
            "EMAIL_ADDRESS_DOES_NOT_EXIST": "L'adresse e-mail n'existe pas",
            "USER_DOES_NOT_EXIST": "L'utilisateur ne existe pas !",
        }