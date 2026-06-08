# portal_db_client.py - Supabase database client and authentication wrapper
import streamlit as st
import os

# Check if we can import supabase. If not, we will handle it gracefully.
try:
    from supabase import create_client, Client
    SUPABASE_IMPORTED = True
except ImportError:
    SUPABASE_IMPORTED = False

# Keyed by (url, key) so if config ever changes the client is re-created,
# rather than a bare module-level global shared across all sessions.
_client_cache: dict = {}

def get_supabase_client():
    """Initialize and return the Supabase client if configured."""
    if not SUPABASE_IMPORTED:
        return None

    # Check secrets.toml first
    url = st.secrets.get("supabase", {}).get("url")
    key = st.secrets.get("supabase", {}).get("key")

    # Fallback to env vars if not in secrets.toml
    if not url:
        url = os.environ.get("SUPABASE_URL")
    if not key:
        key = os.environ.get("SUPABASE_KEY")

    if not (url and key):
        return None

    # Strip whitespace/quotes
    url = url.strip().strip('"').strip("'")
    key = key.strip().strip('"').strip("'")

    cache_key = (url, key)
    if cache_key in _client_cache:
        return _client_cache[cache_key]

    try:
        client = create_client(url, key)
        _client_cache[cache_key] = client
        return client
    except Exception as e:
        st.error(f"Error initializing Supabase client: {e}")
        return None

def is_configured():
    """Check if Supabase is properly configured in secrets or env vars."""
    return get_supabase_client() is not None

def _get_auth_redirect_url():
    try:
        redirect_url = st.secrets.get("supabase", {}).get("auth_redirect_url")
        if redirect_url:
            return redirect_url.strip().strip('"').strip("'")
    except Exception:
        pass
    redirect_url = os.environ.get("SUPABASE_AUTH_REDIRECT_URL")
    if redirect_url:
        return redirect_url.strip()
    return "https://consoleflare.streamlit.app"

def _get_response_value(response, key):
    if isinstance(response, dict):
        return response.get(key)
    return getattr(response, key, None)

def _get_user_value(user, key):
    if isinstance(user, dict):
        return user.get(key)
    return getattr(user, key, None)

def _is_email_verified(user):
    return bool(
        _get_user_value(user, "email_confirmed_at")
        or _get_user_value(user, "confirmed_at")
    )

def sign_up_student(email, password, name, batch, course):
    """
    Register a new student with email and password,
    saving name, batch number, and course name in user metadata.
    """
    client = get_supabase_client()
    if not client:
        return {"error": "Supabase client is not configured."}

    try:
        redirect_url = _get_auth_redirect_url()
        # Standard Supabase Sign Up with custom metadata options
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "email_redirect_to": redirect_url,
                "data": {
                    "name": name,
                    "batch": batch,
                    "course": course
                }
            }
        })
        
        user = _get_response_value(response, "user")
        session = _get_response_value(response, "session")
        if user is None:
            user = response

        email_verified = _is_email_verified(user)
        return {
            "user": user,
            "session": session,
            "email_verified": email_verified,
            "confirmation_required": not bool(session) and not email_verified,
            "error": None,
        }
            
    except Exception as e:
        # Extract friendly error message
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            error_msg = "This email is already registered. Please sign in."
        elif "password should be" in error_msg.lower():
            error_msg = "Password is too weak. Must be at least 6 characters."
        return {"user": None, "error": error_msg}

def sign_in_student(email, password):
    """Sign in an existing student with email and password."""
    client = get_supabase_client()
    if not client:
        return {"session": None, "error": "Supabase client is not configured."}

    try:
        response = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if hasattr(response, "session") and response.session:
            return {"session": response.session, "user": response.user, "error": None}
        elif isinstance(response, dict) and "session" in response:
            return {"session": response["session"], "user": response.get("user"), "error": None}
        else:
            return {"session": response, "user": getattr(response, "user", None), "error": None}
            
    except Exception as e:
        error_msg = str(e)
        if "invalid login credentials" in error_msg.lower() or "invalid credentials" in error_msg.lower():
            error_msg = "Invalid email or password. Please try again."
        elif "email not confirmed" in error_msg.lower() or "not confirmed" in error_msg.lower():
            error_msg = "Please verify your email before signing in. Check your inbox for the confirmation link."
        return {"session": None, "user": None, "error": error_msg}

def _get_password_reset_redirect_url():
    return f"{_get_auth_redirect_url()}?reset=1"

def reset_password_student(email):
    """Send a Supabase password reset email for the given student email."""
    client = get_supabase_client()
    if not client:
        return {"ok": False, "error": "Supabase client is not configured."}

    email = (email or "").strip()
    if not email:
        return {"ok": False, "error": "Please enter your email to reset password."}

    try:
        redirect_url = _get_password_reset_redirect_url()
        options = {"redirect_to": redirect_url} if redirect_url else None

        if hasattr(client.auth, "reset_password_email"):
            if options:
                client.auth.reset_password_email(email, options=options)
            else:
                client.auth.reset_password_email(email)
        elif hasattr(client.auth, "reset_password_for_email"):
            if options:
                client.auth.reset_password_for_email(email, options=options)
            else:
                client.auth.reset_password_for_email(email)
        else:
            return {"ok": False, "error": "This Supabase client version does not support password reset emails."}

        return {"ok": True, "error": None}
    except Exception as e:
        error_msg = str(e)
        if "email rate limit" in error_msg.lower() or "rate limit" in error_msg.lower():
            error_msg = "Too many password reset attempts. Please wait a few minutes and try again."
        elif "invalid email" in error_msg.lower():
            error_msg = "Please enter a valid email address."
        return {"ok": False, "error": error_msg}

def update_password_after_recovery(
    new_password,
    access_token=None,
    refresh_token=None,
    code=None,
    token_hash=None,
):
    """Update a password after the user opens a Supabase recovery email link."""
    client = get_supabase_client()
    if not client:
        return {"ok": False, "error": "Supabase client is not configured."}

    new_password = (new_password or "").strip()
    if len(new_password) < 6:
        return {"ok": False, "error": "Password must be at least 6 characters."}

    try:
        if token_hash:
            verify_otp = getattr(client.auth, "verify_otp", None)
            if not verify_otp:
                return {"ok": False, "error": "This Supabase client version does not support recovery token verification."}
            verify_otp({"token_hash": token_hash, "type": "recovery"})
        elif code:
            exchange_code_for_session = getattr(client.auth, "exchange_code_for_session", None)
            if not exchange_code_for_session:
                return {"ok": False, "error": "This Supabase client version does not support recovery code exchange."}
            exchange_code_for_session(code)
        elif access_token and refresh_token:
            set_session = getattr(client.auth, "set_session", None)
            if not set_session:
                return {"ok": False, "error": "This Supabase client version does not support recovery sessions."}
            set_session(access_token, refresh_token)
        else:
            return {"ok": False, "error": "Password reset link is missing recovery credentials. Please request a new reset email."}

        update_user = getattr(client.auth, "update_user", None)
        if not update_user:
            return {"ok": False, "error": "This Supabase client version does not support password updates."}
        update_user({"password": new_password})
        return {"ok": True, "error": None}
    except Exception as e:
        error_msg = str(e)
        if "expired" in error_msg.lower() or "invalid" in error_msg.lower():
            error_msg = "This password reset link is invalid or expired. Please request a new reset email."
        return {"ok": False, "error": error_msg}

def sign_out_student():
    """Sign out the current active session."""
    client = get_supabase_client()
    if not client:
        return
    try:
        client.auth.sign_out()
    except Exception:
        pass

def save_resume(user_id, resume_data):
    """
    Save the student's CV JSON data to the public.resumes table.
    Uses upsert (insert or update) based on user_id as primary key.
    """
    client = get_supabase_client()
    if not client:
        return {"ok": False, "error": "Supabase client is not configured."}
    if not user_id:
        return {"ok": False, "error": "No authenticated user ID was found. Please sign out and sign in again."}
    try:
        # Perform upsert in Supabase
        data = {
            "id": user_id,
            "resume_data": resume_data
        }
        client.table("resumes").upsert(data).execute()
        return {"ok": True, "error": None}
    except Exception as e:
        error_message = str(e)
        print(f"Error saving resume: {error_message}")
        return {"ok": False, "error": error_message}

def load_resume(user_id):
    """
    Load the student's saved CV JSON data from the public.resumes table.
    """
    client = get_supabase_client()
    if not client:
        return None
    try:
        response = client.table("resumes").select("resume_data").eq("id", user_id).execute()
        # Parse response data
        rows = getattr(response, "data", [])
        if rows:
            return rows[0].get("resume_data")
        return None
    except Exception as e:
        print(f"Error loading resume: {e}")
        return None
    
def get_user_role(user_id):
    client = get_supabase_client()
    if not client:
        return "student"
    try:
        response = client.table("profiles").select("role").eq("id", user_id).execute()
        rows = getattr(response, "data", [])
        if rows:
            return rows[0].get("role", "student")
        return "student"
    except Exception:
        return "student"
