# Changelog

All notable changes to BeeCompose will be documented in this file.


## [26.3.2](https://github.com/beevelop/BeeCompose/compare/v26.3.1...v26.3.2) (2026-03-03)

### Bug Fixes

* **claude-code:** update README and .env.example for SSH deploy key configuration ([3669867](https://github.com/beevelop/BeeCompose/commit/3669867e04c518c5df12079d163d673e5cdfe254))

## [26.3.1](https://github.com/beevelop/BeeCompose/compare/v26.3.0...v26.3.1) (2026-03-03)

### Bug Fixes

* **claude-code:** use deploy key path as volume mount ([b73ee0e](https://github.com/beevelop/BeeCompose/commit/b73ee0e92d9775c18b40a22c908ab7c31dae6dfb))
* **claude-code:** use ENV for ssh deployment key ([0bc31d6](https://github.com/beevelop/BeeCompose/commit/0bc31d6e1fb1946f539d4596cd92491241ebd02b))

### Maintenance

* **claude-code:** add .ci-skip file to skip CI testing for services ([84940b0](https://github.com/beevelop/BeeCompose/commit/84940b0b8a929ecae6e198f8d3721cb4123e4f08))

## [26.3.0](https://github.com/beevelop/BeeCompose/compare/v26.1.7...v26.3.0) (2026-03-03)

### Features

* **claude-code:** add new service configuration and documentation for Claude Code ([fba76a8](https://github.com/beevelop/BeeCompose/commit/fba76a81e1d07d020f21bac961300cd239a28210))

### Maintenance

* **claude-code:** comment out git repository and identity fields in example env file ([aca21f2](https://github.com/beevelop/BeeCompose/commit/aca21f2e7d9e820f52a468528ec66ce0192a3b5a))

### CI/CD

* bump actions/download-artifact from 7 to 8 ([#9](https://github.com/beevelop/BeeCompose/issues/9)) ([d550094](https://github.com/beevelop/BeeCompose/commit/d550094dfa128506d9dc00d935f9f05a345b547a))
* bump actions/upload-artifact from 6 to 7 ([#8](https://github.com/beevelop/BeeCompose/issues/8)) ([d2bee89](https://github.com/beevelop/BeeCompose/commit/d2bee89cf50f63f5538713001a279b6e8d3c01bf))

## [26.1.7](https://github.com/beevelop/BeeCompose/compare/v26.1.6...v26.1.7) (2026-01-24)

### Features

* **ci:** add bc CLI helper tests and update CI workflow ([7ec0600](https://github.com/beevelop/BeeCompose/commit/7ec0600a75dafd59dba64c18117eeefa99d43e9c))
* **ci:** add service coverage check to CI pipeline and update documentation ([62c1733](https://github.com/beevelop/BeeCompose/commit/62c1733c689fe566865f4163bd19561e993e44f5))
* **cloudflared:** add cloudflared service with configuration and documentation for tunnel-only mode ([1602885](https://github.com/beevelop/BeeCompose/commit/160288519eb696e37938dd66f6f6f4ebd743116d))
* **n8n:** add n8n service with configuration and environment setup (closes [#7](https://github.com/beevelop/BeeCompose/issues/7)) ([9fc5a72](https://github.com/beevelop/BeeCompose/commit/9fc5a72ce2a92dce607d610210cf618ec19e6bdd))

### Documentation

* **AGENTS:** update agent manual to embed version tags in docker-compose.yml and clarify environment file usage ([c1af106](https://github.com/beevelop/BeeCompose/commit/c1af1066a60c8a1253ae91aa284989bba0c3db46))
* **AGENTS:** update agent manual to reflect changes in environment file usage and service deployment instructions ([a1c5bb2](https://github.com/beevelop/BeeCompose/commit/a1c5bb224e28f31c3da9349606f5399af4c8d760))
* **README:** add traefik-tunnel service and update networking modes section ([a65bf58](https://github.com/beevelop/BeeCompose/commit/a65bf58951a65719e27d16fc01ca5fe989e6f468))
* **README:** update cloudflared and traefik documentation for tunnel-only mode ([76a49b4](https://github.com/beevelop/BeeCompose/commit/76a49b43a51e2c992692d21081479c940cb87e6a))
* **services:** update README files to use environment-specific files for deployment and add bc CLI commands ([d791062](https://github.com/beevelop/BeeCompose/commit/d7910627a6f8553801b5b2f8813a650c7e218fb1))
* **traefik:** add comment for Traefik v3 reverse proxy with Let's Encrypt ([4513934](https://github.com/beevelop/BeeCompose/commit/4513934245b8cc49140b5bccd862fd5eee8e942b))

### Maintenance

* **cloudflared:** update command and healthcheck for metrics reporting ([ab42417](https://github.com/beevelop/BeeCompose/commit/ab42417977e91c4208e7c571592cef803ecbb8fd))
* **n8n:** update n8n image version to 2.4.6 ([f37b5bb](https://github.com/beevelop/BeeCompose/commit/f37b5bb8851ce1eeafdf975c21a3ced11a2ad87c))
* **publish-oci:** update publishing logic to ensure all services are published consistently ([138dfca](https://github.com/beevelop/BeeCompose/commit/138dfcad35bb4aa5e4fede8179373f5e23a13306))
* remove references to bee helper and update CI skip reasons ([78f255b](https://github.com/beevelop/BeeCompose/commit/78f255b325ba830336a71943f1c2ec0065e5e280))
* **services:** correct external network definition in docker-compose ([d489e63](https://github.com/beevelop/BeeCompose/commit/d489e63d9e88548eaeb4eb69c29ce9a123e43d09))
* **services:** remove obsolete version field from docker-compose files ([f6a1a4f](https://github.com/beevelop/BeeCompose/commit/f6a1a4f490054d487411a88cbe28e3eddde1cffb))
* **services:** remove version field from docker-compose tunnel configuration ([60d20a5](https://github.com/beevelop/BeeCompose/commit/60d20a5ce06fa565ea55de409b1a3fd696ba3901))
* **services:** update docker-compose configurations and remove unused environment files ([7689305](https://github.com/beevelop/BeeCompose/commit/7689305a27eb9aab1b71db7cdfe47820123785a0))
* **services:** update network configuration in docker-compose for traefik service ([2ea8a22](https://github.com/beevelop/BeeCompose/commit/2ea8a22a87f2e58928fe5b715021b35e618936a5))
* **traefik:** add configuration files for tunnel mode and update documentation ([cc3122c](https://github.com/beevelop/BeeCompose/commit/cc3122c81a637459009ac4027b6e894318cdd33e))
* **traefik:** enhance port configuration options and update documentation ([136c770](https://github.com/beevelop/BeeCompose/commit/136c770cb3cc2202f6386915cb8c084862170089))
* **traefik:** remove logging volume and update access log configuration ([b9e358e](https://github.com/beevelop/BeeCompose/commit/b9e358e733f8e93ffbf2ace4eab23884887b7487))
* **traefik:** remove tls labels from service configurations and update documentation ([688bd64](https://github.com/beevelop/BeeCompose/commit/688bd64109cedace28d75b8208058bf77af4ac1c))
* **traefik:** update configuration for exposed and tunnel modes, remove obsolete files ([0509508](https://github.com/beevelop/BeeCompose/commit/0509508b2304428d43fd523d313fa23f135a56da))

### CI/CD

* **ci-cd:** skip network creation for traefik services in CI pipeline ([1f1702d](https://github.com/beevelop/BeeCompose/commit/1f1702de7485d4a631c5bafd5b4ddf533be9ca01))
* **cloudflared:** add .ci-skip file to skip CI testing for service requiring Cloudflare Tunnel token ([2e75291](https://github.com/beevelop/BeeCompose/commit/2e7529127ee5c1d7d6babcee6948dd7c48cb2b73))
* **publish-oci:** add workaround for bind mount prompts in docker compose publish ([7a84502](https://github.com/beevelop/BeeCompose/commit/7a8450214cf0229acdaf4a1a57397e5041d0da37))
* **publish-oci:** refine version determination logic and update comments ([fd1c846](https://github.com/beevelop/BeeCompose/commit/fd1c846c3a5b04bc75d04260b8102bbc0e55fc38))

### Styling

* **bc:** fix string quoting in trap command and update example delimiter ([65aae56](https://github.com/beevelop/BeeCompose/commit/65aae56dd821097c6f5b3bc156d8bb48ccd8b5be))

## [26.1.6](https://github.com/beevelop/BeeCompose/compare/v26.1.5...v26.1.6) (2026-01-22)

### Documentation

* **README:** add dependencies section for various services ([0e179d0](https://github.com/beevelop/BeeCompose/commit/0e179d02c66061814bdb3c4756cf7c9b5ed17a64))
* **README:** update service list and deployment instructions for clarity ([82b3665](https://github.com/beevelop/BeeCompose/commit/82b366561debb14a1ce6caefd1988354c030e282))

## [26.1.5](https://github.com/beevelop/BeeCompose/compare/v26.1.4...v26.1.5) (2026-01-22)

### CI/CD

* **publish-oci:** remove crane installation and update publish commands for non-interactive mode ([91c545a](https://github.com/beevelop/BeeCompose/commit/91c545ae924c19b7d92a7b2de3f51755418659bb))

## [26.1.4](https://github.com/beevelop/BeeCompose/compare/v26.1.3...v26.1.4) (2026-01-22)

### Bug Fixes

* **gitlab:** update port configuration to use new syntax for publishing ([d2ff27b](https://github.com/beevelop/BeeCompose/commit/d2ff27bb0d2a7fc49b37ca795c6b5b6d4a0ff5b9))

### Maintenance

* **license:** update license from Apache 2.0 to MIT and adjust README reference ([8c943b2](https://github.com/beevelop/BeeCompose/commit/8c943b208a0f0dba002d173c1a8f74fb09f8c587))

### CI/CD

* **publish-oci:** add crane installation and link package to repository ([654a768](https://github.com/beevelop/BeeCompose/commit/654a768c4684149d99d041971e1a1a813333ac8f))

## [26.1.3](https://github.com/beevelop/BeeCompose/compare/v26.1.2...v26.1.3) (2026-01-22)

### CI/CD

* **publish-oci:** include environment variables in OCI artifact publishing ([6243afa](https://github.com/beevelop/BeeCompose/commit/6243afaf569e0d4d9aaf8402764425d827911cde))

## [26.1.2](https://github.com/beevelop/BeeCompose/compare/v26.1.1...v26.1.2) (2026-01-22)

### Documentation

* add README files for new services with deployment instructions and configurations ([2db6402](https://github.com/beevelop/BeeCompose/commit/2db64025f07be69527ecd755c6d77c0c549b95fc))

### Maintenance

* **services:** update docker-compose files to set default environment variables and improve service domain handling ([ba8b3b9](https://github.com/beevelop/BeeCompose/commit/ba8b3b96ea93a2cf13e6debadc1d0f51f8dd94f5))

## [26.1.1](https://github.com/beevelop/BeeCompose/compare/v26.1.0...v26.1.1) (2026-01-22)

### CI/CD

* bump actions/checkout from 4 to 6 ([#5](https://github.com/beevelop/BeeCompose/issues/5)) ([13581bf](https://github.com/beevelop/BeeCompose/commit/13581bf3547932483bb3744a4ff32b7c96796c24))
* bump actions/download-artifact from 4 to 7 ([#6](https://github.com/beevelop/BeeCompose/issues/6)) ([094cabc](https://github.com/beevelop/BeeCompose/commit/094cabcdd138ab25990d3aa76845506d3d6d6fe9))
* bump actions/upload-artifact from 4 to 6 ([#3](https://github.com/beevelop/BeeCompose/issues/3)) ([7c00ab2](https://github.com/beevelop/BeeCompose/commit/7c00ab236678f6f98d06c448278a5ddb350517a1))
* bump peter-evans/create-pull-request from 6 to 8 ([#2](https://github.com/beevelop/BeeCompose/issues/2)) ([a6f96e3](https://github.com/beevelop/BeeCompose/commit/a6f96e3b72261f1035a1cf3eaf069dafc4f4c4b7))
* **ci-cd:** enhance bind mount detection and OCI compatibility validation ([b995e23](https://github.com/beevelop/BeeCompose/commit/b995e231f29045bb58fb04a4795f079ab6e61b93))

## 26.1.0 (2026-01-22)

### Features

* **ci-cd:** enhance parallel testing for Docker Compose services and improve result aggregation ([e69ade2](https://github.com/beevelop/BeeCompose/commit/e69ade2d28cbc997a6e8bbf822ac2ab1159aaaa4))
* **ci:** add CI/CD pipeline for docker compose testing and vulnerability scanning ([e98e3ed](https://github.com/beevelop/BeeCompose/commit/e98e3ed42e883aa1ca22432c71f1ed8a3010da91))
* **OCI:** switch to OCI artifacts ([ce61e3b](https://github.com/beevelop/BeeCompose/commit/ce61e3bcdd1d4f956e2294f3ff2978a0fa7bbb53))
* **services:** update docker-compose configurations for multiple services to enhance traefik integration and improve environment variable management ([de60e8d](https://github.com/beevelop/BeeCompose/commit/de60e8d8b10b59a431e1a7b653421898213d64b0))

### Refactoring

* **scripts:** improve handling of environment variables and image extraction in bash scripts ([e654d41](https://github.com/beevelop/BeeCompose/commit/e654d41efef1f20cb9f9f7d1b138884a55396ee6))

### Documentation

* add backup, deployment, naming, and testing guides for BeeCompose services ([e98f2d3](https://github.com/beevelop/BeeCompose/commit/e98f2d3a998e8e846a0a5615a03746bafb2d3e5a))
* **agents:** add comprehensive AI agent operating manual for T-SHITS ([c3820e9](https://github.com/beevelop/BeeCompose/commit/c3820e926eca38b3a0410dccc9d2466764f3ceae))
* **agents:** update Traefik version and enhance linting guidelines ([cb7fa6a](https://github.com/beevelop/BeeCompose/commit/cb7fa6aec2336f1e4d818f5b316644e7f6265079))
* **ci-cd:** update CI/CD documentation to reflect new workflows and OCI publishing details ([2b59d28](https://github.com/beevelop/BeeCompose/commit/2b59d283418684763f9f95d1d88417712247cb04))
* **readme:** update project description and enhance quick start instructions ([dacf77f](https://github.com/beevelop/BeeCompose/commit/dacf77ff3e537763658fe00ec9bb5dcb80b743ce))

### Maintenance

* add .vscode to .gitignore ([489c607](https://github.com/beevelop/BeeCompose/commit/489c607478121ab85fa77877b03c9070fcc71df9))
* add release-it configuration and changelog ([6f42551](https://github.com/beevelop/BeeCompose/commit/6f42551269d332b617c60ff5be7ec7cd3dcf2f21))
* **docs:** update references from T-SHITS to BeeCompose in documentation and configuration files ([0d90a97](https://github.com/beevelop/BeeCompose/commit/0d90a973eedf92ace5da85aecf1337379921bc47))
* **gitlab, minio:** update environment variables for gitlab and minio services ([6ffcb73](https://github.com/beevelop/BeeCompose/commit/6ffcb73d1e644c948553eb7d38e3e353006f2a54))
* **gitlab:** update git port configuration and fix traefik network definition ([efc7ebb](https://github.com/beevelop/BeeCompose/commit/efc7ebb8265dfff12f2c493ab9218003bed895a5))
* **gitlab:** update gitlab port mapping to use default 2222 ([728a4cf](https://github.com/beevelop/BeeCompose/commit/728a4cfcd18bbf918d9335d0cfeebc768e4422c5))
* **services:** add .ci-skip files for nexus and traefik services and update environment variables for weblate ([8554ced](https://github.com/beevelop/BeeCompose/commit/8554ced63c86e65f606d8af1e93b6b4cd025e8f7))
* **services:** update dependency versions and configurations ([f2b753b](https://github.com/beevelop/BeeCompose/commit/f2b753b9a9bef13620b276e79c8162d455db04ba))
* **services:** update docker-compose configurations and environment variables for multiple services ([1471b04](https://github.com/beevelop/BeeCompose/commit/1471b041eaa99400fe3204a81ef5ab2a753946d9))
* **services:** update docker-compose configurations and environment variables for multiple services ([bad25de](https://github.com/beevelop/BeeCompose/commit/bad25de0b07c3ed1b1b1c372dd7c0ebad78a7ea6))
* **services:** update service versions in environment files ([f1b5e41](https://github.com/beevelop/BeeCompose/commit/f1b5e41d157e2bc13110a549fa37dbc0b19702be))
* **services:** update various service versions and configurations ([90535f9](https://github.com/beevelop/BeeCompose/commit/90535f9974b2993764c9382582eb250387433072))
* **traefik:** update network handling and replace traefik.toml with traefik.yml ([9ad287f](https://github.com/beevelop/BeeCompose/commit/9ad287f5a8bfd782ee65d968598bf46ce697ffdf))
* **zabbix:** update environment variables and fix traefik network definition ([00f1ac7](https://github.com/beevelop/BeeCompose/commit/00f1ac7eac7168427e662b27aadb5b0b2d3058e7))

### CI/CD

* add .ci-skip marker for openvpn service and improve service skipping logic ([0b5cf40](https://github.com/beevelop/BeeCompose/commit/0b5cf40634afb6a1f3a282aabadfd854feb3c353))
* add Docker Compose linter configuration and integrate linting step in CI pipeline ([0162e07](https://github.com/beevelop/BeeCompose/commit/0162e07f3a06d2cef6b765674f597ed2cd711739))
* **cve-scan:** enhance CVE scanning with parallel execution and improved result aggregation ([ca0e809](https://github.com/beevelop/BeeCompose/commit/ca0e809ac28c7b3d56bc6de0aa49da3cce2280e2))
* **lint:** improve error and warning count validation in lint results ([ad7ef36](https://github.com/beevelop/BeeCompose/commit/ad7ef361eef5aa66df83371087692aa3bd765bea))
* silence cleanup logs for improved actionable output ([2eaaff2](https://github.com/beevelop/BeeCompose/commit/2eaaff2e941d687d7397384b69c8e458f4552faf))
* update CVE scanning configuration to be non-blocking and improve reporting ([0e58dc6](https://github.com/beevelop/BeeCompose/commit/0e58dc6f460e07deb0c79cd7752ea340c641bfcb))
* update docker compose commands to use quiet mode for reduced log noise ([d810b5e](https://github.com/beevelop/BeeCompose/commit/d810b5e664f9492b73b0485647427e26ba4ebcba))

# Changelog

All notable changes to BeeCompose will be documented in this file.
