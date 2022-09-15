


def error_messages(type, lang, field):
    if type == "blank":
        if lang == 'fr':
            return f"Le champ {field} ne doit pas être vide !"
        return f"The {field} field must not be blank!"
    if type == "required":
        if lang == 'fr':
            return f"Le champ {field} est obligatoire !"
        return f"The {field} field is required!"

def response_messages(lang):
    if lang == 'fr':
        return {
            "PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH": "Le mot de passe et le mot de passe de confirmation ne correspondent pas",
            "TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED": "Le jeton n'est pas valide ou a expiré !",
            "EMAIL_ADDRESS_DOES_NOT_EXIST": "L'adresse e-mail n'existe pas !",
            "USER_DOES_NOT_EXIST": "L'utilisateur ne existe pas !",
            "CONFIRM_YOUR_ADDRESS_EMAIL": "Veuillez confirmer votre adresse e-mail !",
            "EMAIL_OR_PASSWORD_IS_NOT_VALID": "L'email ou le mot de passe n'est pas valide !",
            "MISSING_PARAMETER": "paramètre manquant !",
            "SOMETHING_WENT_WRONG": "Quelque chose a mal tourné !",
            "SOMETHING_WENT_WRONG": "Quelque chose a mal tourné !",
            "YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION": "Vous n'êtes pas autoriser pour cette action.",
            
            "SUCCESSFUL_REGISTRATION": "Inscription réussie !",
            "SUCCESSFUL_ACTIVATION_ACCOUNT": "Votre compte a été créé et activé avec succès !",
            "LOGIN_SUCCESS": "Connexion réussie !",
            "PASSWORD_CHANGED_SUCCESSFULLY": "Le mot de passe a été changé avec succès !",
            "PASSWORD_RESET_SUCCESSFULLY": "Réinitialisation du mot de passe réussie !",
            "PASSWORD_RESET_LINK_SEND": "Le lien de réinitialisation du mot de passe a été envoyé. Veuillez vérifier votre e-mail.",
            "LOGOUT_SUCCESSFULLY": "Déconnexion réussie !",
        }
    return {
        "PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH": "Password and confirmation password do not match!",
        "TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED": "The token is not valid or has expired!",
        "EMAIL_ADDRESS_DOES_NOT_EXIST": "The e-mail address does not exist!",
        "USER_DOES_NOT_EXIST": "The user does not exist!",
        "CONFIRM_YOUR_ADDRESS_EMAIL": "Please confirm your email address!",
        "EMAIL_OR_PASSWORD_IS_NOT_VALID": "The email or the password is not valid!",
        "MISSING_PARAMETER": "missing parameter",
        "SOMETHING_WENT_WRONG": "Something went wrong!",
        "YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION": "You are not authorized for this action.",
        
        "SUCCESSFUL_REGISTRATION": "Successful registration!",
        "SUCCESSFUL_ACTIVATION_ACCOUNT": "Your account has been successfully created and activated!",
        "LOGIN_SUCCESS": "Successful login!",
        "PASSWORD_CHANGED_SUCCESSFULLY": "The password has been successfully changed!",
        "PASSWORD_RESET_SUCCESSFULLY": "Password reset successful!",
        "PASSWORD_RESET_LINK_SEND": "The password reset link has been sent. Please check your email.",
        "LOGOUT_SUCCESSFULLY": "Successful logout!",
    }