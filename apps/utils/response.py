


def error_messages(type, lang, field):
    if type == "blank":
        return f"Le champ {field} ne doit pas être vide."
    if type == "required":
        return f"Le champ {field} est obligatoire."

def res(lang):
    if lang == 'fr':
        return {
            "PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH": "Le mot de passe et le mot de passe de confirmation ne correspondent pas",
            "TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED": "Le jeton n'est pas valide ou a expiré !",
            "EMAIL_ADDRESS_DOES_NOT_EXIST": "L'adresse e-mail n'existe pas !",
            "USER_DOES_NOT_EXIST": "L'utilisateur ne existe pas !",
            "CONFIRM_YOUR_ADDRESS_EMAIL": "Veuillez confirmer votre adresse e-mail !",
            "EMAIL_OR_PASSWORD_IS_NOT_VALID": "L'email ou le mot de passe n'est pas valide !",
            
            "SUCCESSFUL_REGISTRATION": "Inscription réussie !",
            "SUCCESSFUL_ACTIVATION_ACCOUNT": "Votre compte a été créé et activé avec succès !",
            "LOGIN_SUCCESS": "Connexion réussie !",
            "PASSWORD_CHANGED_SUCCESSFULLY": "Le mot de passe a été changé avec succès !",
            "PASSWORD_RESET_SUCCESSFULLY": "Réinitialisation du mot de passe réussie !",
            "PASSWORD_RESET_LINK_SEND": "Le lien de réinitialisation du mot de passe a été envoyé. Veuillez vérifier votre e-mail.",
            "LOGOUT_SUCCESSFULLY": "Déconnexion réussie !",
        }