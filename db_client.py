# db_client.py - Supabase database client and authentication wrapper
import streamlit as st
import os

# Check if we can import supabase. If not, we will handle it gracefully.
try:
    from supabase import create_client, Client
    SUPABASE_IMPORTED = True
except ImportError:
    SUPABASE_IMPORTED = False

_client = None

def get_supabase_client():
    """Initialize and return the Supabase client if configured."""
    global _client
    if _client is not None:
        return _client

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

    if url and key:
        try:
            # Strip whitespace/quotes
            url = url.strip().strip('"').strip("'")
            key = key.strip().strip('"').strip("'")
            _client = create_client(url, key)
            return _client
        except Exception as e:
            st.error(f"Error initializing Supabase client: {e}")
            return None
    return None

def is_configured():
    """Check if Supabase is properly configured in secrets or env vars."""
    return get_supabase_client() is not None

def sign_up_student(email, password, name, batch):
    """
    Register a new student with email and password,
    saving Name and Batch Number in user metadata.
    """
    client = get_supabase_client()
    if not client:
        return {"error": "Supabase client is not configured."}

    try:
        # Standard Supabase Sign Up with custom metadata options
        response = client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "batch": batch
                }
            }
        })
        
        # In newer versions of Supabase Python library, response could be an object or dictionary.
        # Let's inspect or normalize the return
        if hasattr(response, "user") and response.user:
            return {"user": response.user, "error": None}
        elif isinstance(response, dict) and "user" in response:
            return {"user": response["user"], "error": None}
        else:
            # If email confirmation is required, the user might be returned inside the session or as created
            return {"user": getattr(response, "user", response), "error": None}
            
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
        return {"session": None, "user": None, "error": error_msg}

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
        return False
    try:
        # Perform upsert in Supabase
        data = {
            "id": user_id,
            "resume_data": resume_data
        }
        client.table("resumes").upsert(data).execute()
        return True
    except Exception as e:
        # We fail silently or log to debug
        print(f"Error saving resume: {e}")
        return False

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
