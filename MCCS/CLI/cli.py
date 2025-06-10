# CLI/cli.py

import argparse
from RBAC import rbac_handler
from CREDENTIALS import credentials_handler

# Initialize database tables if needed
credentials_handler.create_credentials_table()

def register(args):
    rbac_handler.register_user(args.username, args.password, args.role)

def login(args):
    success = rbac_handler.login_user(args.username, args.password)
    if success:
        print(f"Welcome, {args.username}!")
    else:
        print("Login failed.")

def add_cred(args):
    credentials_handler.add_credential(
        owner_id=args.username,
        role=rbac_handler.get_user_role(args.username),
        name=args.name,
        raw_value=args.value,
        expires_at=args.expires
    )
    print("Credential added.")

def get_cred(args):
    try:
        cred = credentials_handler.get_credential(args.username, args.cred_id)
        if cred:
            print(f"Credential: {cred}")
        else:
            print("Credential not found.")
    except PermissionError as e:
        print(str(e))

def delete_cred(args):
    try:
        credentials_handler.delete_credential(args.username, args.cred_id)
        print("Credential deleted.")
    except PermissionError as e:
        print(str(e))

def list_creds(args):
    creds = credentials_handler.list_credentials(args.username)
    for cred in creds:
        print(f"ID: {cred[0]}, Name: {cred[1]}, Created: {cred[2]}, Expires: {cred[3]}")

def main():
    parser = argparse.ArgumentParser(description="MCCS CLI - Credential & Access Manager")
    subparsers = parser.add_subparsers(title="Commands")

    # Register
    reg = subparsers.add_parser("register", help="Register a new user")
    reg.add_argument("username")
    reg.add_argument("password")
    reg.add_argument("--role", default="User", help="Role: Admin/User/Auditor")
    reg.set_defaults(func=register)

    # Login
    login_cmd = subparsers.add_parser("login", help="Login as a user")
    login_cmd.add_argument("username")
    login_cmd.add_argument("password")
    login_cmd.set_defaults(func=login)

    # Add credential
    add = subparsers.add_parser("add-cred", help="Add a new credential")
    add.add_argument("username")
    add.add_argument("name")
    add.add_argument("value")
    add.add_argument("--expires", help="Expiration timestamp (optional)", default=None)
    add.set_defaults(func=add_cred)

    # Get credential
    get = subparsers.add_parser("get-cred", help="Retrieve a credential")
    get.add_argument("username")
    get.add_argument("cred_id", type=int)
    get.set_defaults(func=get_cred)

    # Delete credential
    delete = subparsers.add_parser("delete-cred", help="Delete a credential")
    delete.add_argument("username")
    delete.add_argument("cred_id", type=int)
    delete.set_defaults(func=delete_cred)

    # List credentials
    list_cmd = subparsers.add_parser("list-creds", help="List all your credentials")
    list_cmd.add_argument("username")
    list_cmd.set_defaults(func=list_creds)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
