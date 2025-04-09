up:
	cp api/blockvisor-api/src/database/test_roles_permissions.query setup/init/
	docker compose build
	docker compose up -d
	docker compose run init ./database-setup.py

down:
	docker compose down

test-images:
	docker rmi test_v1
	docker build -t test_v1 blockvisor/bv/tests/image_v1
	docker rmi test_v2
	docker build -t test_v2 blockvisor/bv/tests/image_v2

host-setup:
	bv stop || true
	apptainer instance stop -a || true
	rm -rf /var/lib/blockvisor/*
	rm -rf /opt/blockvisor
	cd blockvisor && make bundle-base
	/tmp/bundle/installer

tests: up host-setup test-images
	export RUST_LOG="off"
	cd blockvisor && cargo test -p blockvisord --test itests -- --test-threads=9
	docker compose down
