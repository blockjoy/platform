#!/usr/bin/env python3
import typer
from typing_extensions import Annotated
import base64
import os
import time
import getpass
import sys
import psycopg2
import uuid
import argon2
from argon2.low_level import Type
import getpass


def generate_password_hash(passwd, salt=None):
    # Generate a random salt if none is provided
    if salt is None:
        salt = os.urandom(16)  # 16 bytes salt, same as blockvisor-api

    # Use the same parameters as blockvisor-api
    raw_hash = argon2.low_level.hash_secret_raw(
        passwd.encode('utf-8'),
        salt,
        time_cost=2,  # Default in Rust's Argon2 crate
        memory_cost=19456,  # Default (19 MiB)
        parallelism=1,  # Default
        hash_len=32,  # Output 32 bytes
        type=Type.ID  # Argon2id variant
    )

    # Convert to base64 without padding (same as blockvisor-api)
    salt_b64 = base64.b64encode(salt).decode('utf-8').rstrip('=')
    hash_b64 = base64.b64encode(raw_hash).decode('utf-8').rstrip('=')

    return salt_b64, hash_b64


def main(fname: Annotated[str, typer.Argument(help="First Name", envvar="FIRST_NAME")] = None,
         lname: Annotated[str, typer.Argument(help="Last Name", envvar="LAST_NAME")] = None,
         email: Annotated[str, typer.Argument(help="Email", envvar="EMAIL")] = None,
         passwd: Annotated[
             str, typer.Argument(help="Password to hash (if not provided, will prompt securely)",
                                 envvar="PASSWORD")] = None,
         salt: Annotated[
             str, typer.Argument(help="Base64-encoded salt to use (if not provided, a random one will be generated)",
                                 envvar="SALT")] = None,
         count: Annotated[int, typer.Argument(help="Number of hash/salt pairs to generate", envvar="COUNT")] = 1):
    fname = fname if fname is not None else input("Enter your first name: ")
    lname = lname if lname is not None else input("Enter your last name: ")
    email = email if email is not None else input("Enter your email: ")
    passwd = passwd if passwd is not None else getpass.getpass("Enter your password: ")

    # Generate the specified number of hash/salt pairs
    for i in range(count):
        # Generate a new random salt for each iteration unless one was provided
        current_salt = salt if salt is not None else None

        # Generate the hash
        salt_b64, hash_b64 = generate_password_hash(passwd, current_salt)

    db_setup(fname, lname, email, hash_b64, salt_b64)

    print("\n***Initial User Set is Complete***\n")
    print("\n----------Credentials----------\n")
    print("Admin User: \t\t" + email + "\n")
    print("Non-Admin User: \tuser@example.com\n")
    print("Both user passwords are set to what you defined.\n")
    print("The Blockvisor stack setup is complete.  You can now access it at http://<server_ip>\n\n")


def db_setup(fname, lname, email, hash_b64, salt_b64):
    # Generate a random UUID for the user
    admin_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    admin_token_id = str(uuid.uuid4())
    user_token_id = str(uuid.uuid4())
    region_token_id = str(uuid.uuid4())

    admin_token = 'Hqzv8Ux7LWRR'
    user_token = 'Aczv9Ux7LxR3'

    conn = psycopg2.connect(
        host="database",
        port=5432,
        database="blockvisor_db",
        user="blockvisor",
        password="password"
    )
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO users (id, email, hashword, salt, created_at, first_name, last_name, confirmed_at) 
                   VALUES (%s, %s, %s, %s, now(), %s, %s, now());''',
                   (admin_id, email, hash_b64, salt_b64, fname, lname))
    cursor.execute('''
                   INSERT INTO users (id, email, hashword, salt, created_at, first_name, last_name, confirmed_at) 
                   VALUES (%s, 'user@example.com', %s, %s, now(), 'Test', 'User', now());''',
                   (user_id, hash_b64, salt_b64))
    cursor.execute('''
                   INSERT INTO orgs (id, name, is_personal, created_at, updated_at, deleted_at, host_count, node_count, member_count, stripe_customer_id, address_id)
                   VALUES (%s, 'Main Org', FALSE, now(), now(), NULL, 1, 0, 2, NULL, NULL);''', (org_id,))
    cursor.execute('''
                   INSERT INTO tokens (id, token_type, token, created_by_type, created_by_id, org_id, created_at, updated_at)
                   VALUES (%s, 'host_provision', %s, 'user', %s, %s, now(), now());''',
                   (admin_token_id, admin_token, admin_id, org_id))
    cursor.execute('''
                   INSERT INTO tokens (id, token_type, token, created_by_type, created_by_id, org_id, created_at, updated_at)
                   VALUES (%s, 'host_provision', %s, 'user', %s, %s, now(), now());''',
                   (user_token_id, user_token, user_id, org_id))
    cursor.execute('''
                   INSERT INTO regions (id,sku_code,key,display_name)
                   VALUES
                   (%s,'DEV1','dev','DEV');''', (region_token_id,))
    cursor.execute('''
                   INSERT INTO user_roles (user_id, org_id, role, created_at)
                   VALUES (%s, %s, 'blockjoy-admin', now());''', (admin_id, org_id))
    cursor.execute('''
                   INSERT INTO user_roles (user_id, org_id, role, created_at)
                   VALUES (%s, %s, 'org-member', now());''', (user_id, org_id))
    cursor.execute(open('test_roles_permissions.query', 'r').read())
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    typer.run(main)
