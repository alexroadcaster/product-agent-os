# Файловая система и идентичность корня

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: security/runtime owner + docs-maintainer. Область: исходники PAOS на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении guards, tests или policy. Ссылки на тесты обозначают маршруты проверки, а не новый прогон. Реальные профили, credentials и provider-вызовы не исследовались.

## Регистрация и чтение

[project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) разрешает локальный абсолютный путь и связывает canonical root с identity каталога (device/inode); перед чтением фиксированных control-plane файлов сверяет binding, проверяет regular file, отсутствие symlink и hardlinks, размер до 1 MiB, identity открытого handle и изменения в процессе чтения. Хеш относится к исходным байтам, а возвращаемый текст может быть redacted. Это отдельный ограниченный reader, а не полный проводник проекта.

[app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) снимает наблюдение только pinned task files: максимум 32 файла, 64 KiB на файл и 512 KiB суммарно. Он исключает private paths, links, binary/private-key содержимое, проверяет путь, handle и повторный binding; вывод diff ограничен и redacted. Отказ или excluded означает отсутствие допустимого наблюдения, а не доказательство отсутствия изменений.

[profile identity](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/connections/profile-identity.mts) отдельно проверяет идентичность каталога профиля и namespace credential store. Admission check не является атомарной файловой блокировкой. Для изменений нужны [project source tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/project-sources.test.mts), [file tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-files.test.mts), [profile tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/profile-identity.test.mts) и проверка соответствующей пользовательской поверхности; эти ссылки не означают их запуск сейчас. Реальный проект здесь не сканировался, а полный файловый каталог и будущие интеграции описаны в плане, а не доказаны этим reader.
