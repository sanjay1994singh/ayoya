def save_social_profile(backend, user, response, *args, **kwargs):
    if backend.name != "google-oauth2" or not user:
        return
    changed = False
    avatar = response.get("picture", "")
    if avatar and not user.avatar_url:
        user.avatar_url = avatar
        changed = True
    if response.get("email") and not user.email:
        user.email = response["email"]
        changed = True
    if changed:
        user.save(update_fields=["avatar_url", "email", "updated_at"])
