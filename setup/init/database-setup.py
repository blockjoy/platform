#!/usr/bin/env python3
import base64
import os
import time
import getpass
import argparse
import sys
import psycopg2
import uuid
import argon2
from argon2.low_level import Type


def generate_password_hash(password, salt=None):
    # Generate a random salt if none is provided
    if salt is None:
        salt = os.urandom(16)  # 16 bytes salt, same as blockvisor-api
    
    # Use the same parameters as blockvisor-api
    raw_hash = argon2.low_level.hash_secret_raw(
        password.encode('utf-8'),
        salt,
        time_cost=2,          # Default in Rust's Argon2 crate
        memory_cost=19456,    # Default (19 MiB)
        parallelism=1,        # Default
        hash_len=32,          # Output 32 bytes
        type=Type.ID          # Argon2id variant
    )
    
    # Convert to base64 without padding (same as blockvisor-api)
    salt_b64 = base64.b64encode(salt).decode('utf-8').rstrip('=')
    hash_b64 = base64.b64encode(raw_hash).decode('utf-8').rstrip('=')
    
    return salt_b64, hash_b64

def main():
    parser = argparse.ArgumentParser(description='Generate Argon2id password hashes compatible with blockvisor-api')
    parser.add_argument('-p', '--password', help='Password to hash (if not provided, will prompt securely)')
    parser.add_argument('-s', '--salt', help='Base64-encoded salt to use (if not provided, a random one will be generated)')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of hash/salt pairs to generate (default: 1)')
    parser.add_argument('-f', '--fname', help='First Name')
    parser.add_argument('-l', '--lname', help='Last Name')
    parser.add_argument('-e', '--email', help='Email')
    
    args = parser.parse_args()

    # Initialize user information
    fname = args.fname 
    lname = args.lname
    email = args.email

    # Get password if not provided
    password = args.password
    
    # Get salt if provided
    salt = None
    
    # Generate the specified number of hash/salt pairs
    for i in range(args.count):
        # Generate a new random salt for each iteration unless one was provided
        current_salt = salt if salt is not None else None
        
        # Generate the hash
        salt_b64, hash_b64 = generate_password_hash(password, current_salt)
    check_success()
    db_setup(fname, lname, email, hash_b64, salt_b64)

def check_success():
    success_file = '/data/success'

    if os.path.exists(success_file):
        print(f"File ./setup/success exists already.  Waiting for it to be removed...")

        while os.path.exists(success_file):
            time.sleep(1)
        print(f"Success file has been removed. Continuing")
    else:
        print(f"./setup/success does not exist, continuing setup")
    return

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
                   VALUES (%s, %s, %s, %s, now(), %s, %s, now());''', (admin_id, email, hash_b64, salt_b64, fname, lname))
    cursor.execute('''
                   INSERT INTO users (id, email, hashword, salt, created_at, first_name, last_name, confirmed_at) 
                   VALUES (%s, 'user@example.com', %s, %s, now(), 'Test', 'User', now());''', (user_id, hash_b64, salt_b64))
    cursor.execute('''
                   INSERT INTO orgs (id, name, is_personal, created_at, updated_at, deleted_at, host_count, node_count, member_count, stripe_customer_id, address_id)
                   VALUES (%s, 'Main Org', FALSE, now(), now(), NULL, 1, 0, 2, NULL, NULL);''', (org_id,))
    cursor.execute('''
                   INSERT INTO tokens (id, token_type, token, created_by_type, created_by_id, org_id, created_at, updated_at)
                   VALUES (%s, 'host_provision', %s, 'user', %s, %s, now(), now());''', (admin_token_id, admin_token, admin_id, org_id))
    cursor.execute('''
                   INSERT INTO tokens (id, token_type, token, created_by_type, created_by_id, org_id, created_at, updated_at)
                   VALUES (%s, 'host_provision', %s, 'user', %s, %s, now(), now());''', (user_token_id, user_token, user_id, org_id))
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
    cursor.execute('''
                   INSERT INTO role_permissions (role, permission)
                   VALUES
        ('blockjoy-admin', 'auth-admin-list-permissions'),
        ('blockjoy-admin', 'billing-exempt'),
        ('blockjoy-admin', 'command-admin-list'),
        ('blockjoy-admin', 'command-admin-pending'),
        ('blockjoy-admin', 'host-admin-create-region'),
        ('blockjoy-admin', 'host-admin-delete-host'),
        ('blockjoy-admin', 'host-admin-get-host'),
        ('blockjoy-admin', 'host-admin-list-hosts'),
        ('blockjoy-admin', 'host-admin-list-regions'),
        ('blockjoy-admin', 'host-admin-restart'),
        ('blockjoy-admin', 'host-admin-start'),
        ('blockjoy-admin', 'host-admin-stop'),
        ('blockjoy-admin', 'host-admin-update-host'),
        ('blockjoy-admin', 'host-admin-update-region'),
        ('blockjoy-admin', 'host-admin-view-cost'),
        ('blockjoy-admin', 'image-admin-add'),
        ('blockjoy-admin', 'image-admin-get'),
        ('blockjoy-admin', 'image-admin-list-archives'),
        ('blockjoy-admin', 'image-admin-update-archive'),
        ('blockjoy-admin', 'image-admin-update-image'),
        ('blockjoy-admin', 'invitation-admin-create'),
        ('blockjoy-admin', 'invitation-admin-list'),
        ('blockjoy-admin', 'invitation-admin-revoke'),
        ('blockjoy-admin', 'mqtt-admin-acl'),
        ('blockjoy-admin', 'node-admin-create'),
        ('blockjoy-admin', 'node-admin-delete'),
        ('blockjoy-admin', 'node-admin-get'),
        ('blockjoy-admin', 'node-admin-list'),
        ('blockjoy-admin', 'node-admin-report-error'),
        ('blockjoy-admin', 'node-admin-report-status'),
        ('blockjoy-admin', 'node-admin-restart'),
        ('blockjoy-admin', 'node-admin-start'),
        ('blockjoy-admin', 'node-admin-stop'),
        ('blockjoy-admin', 'node-admin-transfer'),
        ('blockjoy-admin', 'node-admin-update-config'),
        ('blockjoy-admin', 'node-admin-upgrade'),
        ('blockjoy-admin', 'node-admin-view-cost'),
        ('blockjoy-admin', 'org-address-delete'),
        ('blockjoy-admin', 'org-address-get'),
        ('blockjoy-admin', 'org-address-set'),
        ('blockjoy-admin', 'org-admin-get'),
        ('blockjoy-admin', 'org-admin-list'),
        ('blockjoy-admin', 'org-admin-update'),
        ('blockjoy-admin', 'org-billing-get-billing-details'),
        ('blockjoy-admin', 'org-billing-init-card'),
        ('blockjoy-admin', 'org-billing-list-payment-methods'),
        ('blockjoy-admin', 'protocol-admin-add-protocol'),
        ('blockjoy-admin', 'protocol-admin-add-version'),
        ('blockjoy-admin', 'protocol-admin-get-pricing'),
        ('blockjoy-admin', 'protocol-admin-get-protocol'),
        ('blockjoy-admin', 'protocol-admin-get-latest'),
        ('blockjoy-admin', 'protocol-admin-list-protocols'),
        ('blockjoy-admin', 'protocol-admin-list-variants'),
        ('blockjoy-admin', 'protocol-admin-list-versions'),
        ('blockjoy-admin', 'protocol-admin-update-protocol'),
        ('blockjoy-admin', 'protocol-admin-update-version'),
        ('blockjoy-admin', 'protocol-admin-view-all-stats'),
        ('blockjoy-admin', 'protocol-admin-view-private'),
        ('blockjoy-admin', 'protocol-get-pricing'),
        ('blockjoy-admin', 'user-admin-filter'),
        ('blockjoy-admin', 'user-admin-get'),
        ('blockjoy-admin', 'user-admin-update'),
        ('blockjoy-admin', 'user-settings-admin-delete'),
        ('blockjoy-admin', 'user-settings-admin-get'),
        ('blockjoy-admin', 'user-settings-admin-update'),
        ('email-invitation', 'invitation-accept'),
        ('email-invitation', 'invitation-decline'),
        ('email-invitation', 'user-create'),
        ('email-registration-confirmation', 'auth-confirm'),
        ('email-reset-password', 'auth-update-password'),
        ('grpc-login', 'api-key-create'),
        ('grpc-login', 'api-key-delete'),
        ('grpc-login', 'api-key-list'),
        ('grpc-login', 'auth-list-permissions'),
        ('grpc-login', 'auth-refresh'),
        ('grpc-login', 'auth-update-ui-password'),
        ('grpc-login', 'bundle-list-versions'),
        ('grpc-login', 'bundle-retrieve'),
        ('grpc-login', 'command-ack'),
        ('grpc-login', 'command-create'),
        ('grpc-login', 'command-get'),
        ('grpc-login', 'command-list'),
        ('grpc-login', 'command-pending'),
        ('grpc-login', 'discovery-services'),
        ('grpc-login', 'image-get'),
        ('grpc-login', 'image-list-archives'),
        ('grpc-login', 'invitation-accept'),
        ('grpc-login', 'invitation-decline'),
        ('grpc-login', 'invitation-list'),
        ('grpc-login', 'metrics-host'),
        ('grpc-login', 'metrics-node'),
        ('grpc-login', 'mqtt-acl'),
        ('grpc-login', 'node-report-error'),
        ('grpc-login', 'org-create'),
        ('grpc-login', 'org-get'),
        ('grpc-login', 'org-list'),
        ('grpc-login', 'org-provision-get-token'),
        ('grpc-login', 'org-provision-reset-token'),
        ('grpc-login', 'protocol-get-protocol'),
        ('grpc-login', 'protocol-get-latest'),
        ('grpc-login', 'protocol-get-pricing'),
        ('grpc-login', 'protocol-list-protocols'),
        ('grpc-login', 'protocol-list-variants'),
        ('grpc-login', 'protocol-list-versions'),
        ('grpc-login', 'protocol-view-public'),
        ('grpc-login', 'user-create'),
        ('grpc-login', 'user-delete'),
        ('grpc-login', 'user-filter'),
        ('grpc-login', 'user-get'),
        ('grpc-login', 'user-settings-delete'),
        ('grpc-login', 'user-settings-get'),
        ('grpc-login', 'user-settings-update'),
        ('grpc-login', 'user-update'),
        ('grpc-new-host', 'archive-get-download-chunks'),
        ('grpc-new-host', 'archive-get-download-metadata'),
        ('grpc-new-host', 'archive-get-upload-slots'),
        ('grpc-new-host', 'archive-put-download-manifest'),
        ('grpc-new-host', 'auth-refresh'),
        ('grpc-new-host', 'bundle-list-versions'),
        ('grpc-new-host', 'bundle-retrieve'),
        ('grpc-new-host', 'command-ack'),
        ('grpc-new-host', 'command-create'),
        ('grpc-new-host', 'command-get'),
        ('grpc-new-host', 'command-list'),
        ('grpc-new-host', 'command-pending'),
        ('grpc-new-host', 'command-update'),
        ('grpc-new-host', 'crypt-get-secret'),
        ('grpc-new-host', 'crypt-put-secret'),
        ('grpc-new-host', 'discovery-services'),
        ('grpc-new-host', 'host-get-host'),
        ('grpc-new-host', 'host-list-hosts'),
        ('grpc-new-host', 'host-list-regions'),
        ('grpc-new-host', 'host-update-host'),
        ('grpc-new-host', 'image-get'),
        ('grpc-new-host', 'image-list-archives'),
        ('grpc-new-host', 'metrics-host'),
        ('grpc-new-host', 'metrics-node'),
        ('grpc-new-host', 'mqtt-acl'),
        ('grpc-new-host', 'node-create'),
        ('grpc-new-host', 'node-delete'),
        ('grpc-new-host', 'node-get'),
        ('grpc-new-host', 'node-list'),
        ('grpc-new-host', 'node-report-error'),
        ('grpc-new-host', 'node-report-status'),
        ('grpc-new-host', 'node-restart'),
        ('grpc-new-host', 'node-start'),
        ('grpc-new-host', 'node-stop'),
        ('grpc-new-host', 'node-update-config'),
        ('grpc-new-host', 'node-upgrade'),
        ('grpc-new-host', 'protocol-get-protocol'),
        ('grpc-new-host', 'protocol-get-latest'),
        ('grpc-new-host', 'protocol-list-protocols'),
        ('grpc-new-host', 'protocol-list-variants'),
        ('grpc-new-host', 'protocol-list-versions'),
        ('grpc-new-host', 'protocol-view-public'),
        ('org-owner', 'org-address-delete'),
        ('org-owner', 'org-address-get'),
        ('org-owner', 'org-address-set'),
        ('org-owner', 'org-billing-get-billing-details'),
        ('org-owner', 'org-billing-init-card'),
        ('org-owner', 'org-billing-list-payment-methods'),
        ('org-owner', 'org-delete'),
        ('org-admin', 'crypt-get-secret'),
        ('org-admin', 'crypt-put-secret'),
        ('org-admin', 'host-billing-get'),
        ('org-admin', 'host-delete-host'),
        ('org-admin', 'host-provision-create'),
        ('org-admin', 'host-provision-get'),
        ('org-admin', 'invitation-create'),
        ('org-admin', 'invitation-revoke'),
        ('org-admin', 'node-create'),
        ('org-admin', 'node-delete'),
        ('org-admin', 'org-address-delete'),
        ('org-admin', 'org-address-get'),
        ('org-admin', 'org-address-set'),
        ('org-admin', 'org-billing-get-billing-details'),
        ('org-admin', 'org-billing-init-card'),
        ('org-admin', 'org-billing-list-payment-methods'),
        ('org-admin', 'org-remove-member'),
        ('org-admin', 'org-update'),
        ('org-admin', 'protocol-get-pricing'),
        ('org-member', 'host-get-host'),
        ('org-member', 'host-list-hosts'),
        ('org-member', 'host-list-regions'),
        ('org-member', 'host-restart'),
        ('org-member', 'host-start'),
        ('org-member', 'host-stop'),
        ('org-member', 'node-get'),
        ('org-member', 'node-list'),
        ('org-member', 'node-report-error'),
        ('org-member', 'node-restart'),
        ('org-member', 'node-start'),
        ('org-member', 'node-stop'),
        ('org-member', 'node-update-config'),
        ('org-member', 'org-create'),
        ('org-member', 'org-get'),
        ('org-member', 'org-list'),
        ('org-member', 'org-provision-get-token'),
        ('org-member', 'org-provision-reset-token'),
        ('org-member', 'org-remove-self'),
        ('org-personal', 'crypt-get-secret'),
        ('org-personal', 'crypt-put-secret'),
        ('org-personal', 'host-billing-get'),
        ('org-personal', 'host-delete-host'),
        ('org-personal', 'host-get-host'),
        ('org-personal', 'host-list-hosts'),
        ('org-personal', 'host-list-regions'),
        ('org-personal', 'host-provision-create'),
        ('org-personal', 'host-provision-get'),
        ('org-personal', 'host-restart'),
        ('org-personal', 'host-start'),
        ('org-personal', 'host-stop'),
        ('org-personal', 'node-create'),
        ('org-personal', 'node-delete'),
        ('org-personal', 'node-get'),
        ('org-personal', 'node-list'),
        ('org-personal', 'node-report-error'),
        ('org-personal', 'node-report-status'),
        ('org-personal', 'node-restart'),
        ('org-personal', 'node-start'),
        ('org-personal', 'node-stop'),
        ('org-personal', 'node-update-config'),
        ('org-personal', 'org-address-delete'),
        ('org-personal', 'org-address-get'),
        ('org-personal', 'org-address-set'),
        ('org-personal', 'org-billing-get-billing-details'),
        ('org-personal', 'org-billing-init-card'),
        ('org-personal', 'org-billing-list-payment-methods'),
        ('org-personal', 'org-create'),
        ('org-personal', 'org-get'),
        ('org-personal', 'org-list'),
        ('org-personal', 'org-provision-get-token'),
        ('org-personal', 'org-provision-reset-token'),
        ('org-personal', 'org-update'),
        ('org-personal', 'protocol-get-pricing'),
        ('view-developer-preview', 'protocol-view-development');
    ''')
    conn.commit()
    cursor.close()
    conn.close()

    f = open("/data/success", "x")
    f.close()

if __name__ == "__main__":
    main() 
