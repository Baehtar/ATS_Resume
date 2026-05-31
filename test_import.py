# test_import.py
import inspect
import portal_db_client as db_client

print("Signature of sign_up_student:")
print(inspect.signature(db_client.sign_up_student))
