# /shared/contracts/ — Контракты API

Контракты API между сервисами. Файлы создаются dev-agent в INFRA-блоке (wave 0) по Design INT-N.

| Папка | Технология | Стандарт |
|-------|-----------|----------|
| `openapi/` | OpenAPI 3.1 (REST) | [standard-openapi.md](/specs/docs/.technologies/standard-openapi.md) |
| `protobuf/` | Protobuf v3 (gRPC) | [standard-protobuf.md](/specs/docs/.technologies/standard-protobuf.md) |

**Владение:** Провайдер сервиса владеет контрактом (standard-analysis.md § 3.4).
**Именование:** `{svc}.yaml` / `{svc}.proto` — совпадает с `specs/docs/{svc}.md`.
