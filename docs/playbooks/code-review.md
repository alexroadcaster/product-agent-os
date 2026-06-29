# Playbook: code review через Codex

Source status: `official + experiment`  
Источники: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex subagents](https://developers.openai.com/codex/concepts/subagents), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

## Цель

Использовать Codex как reviewer, который ищет bugs, regressions, test gaps, security risks и maintainability issues.

## Prompt для одного агента

```text
Review current changes as a code reviewer.

Prioritize:
1. Bugs and behavioral regressions.
2. Security or data-safety risks.
3. Missing tests for changed behavior.
4. Professional coding failures that create real debt: unnecessary custom code, missing existing-capability scan, needless dependency, weak abstraction, brittle refactor or low-signal comments.
5. Maintainability issues only if they affect correctness.

Output findings first.
Each finding must include file, line, severity, and why it matters.
Do not rewrite code unless asked.
```

## Профессиональный review кода

Для не механических изменений кода reviewer проверяет `.codex/workflows/coding-standards.md` и `.codex/artifact-templates/coding-standard-checklist.md`, если они есть в пакете задачи. Замечания должны указывать:

- самописный код, где удаление, конфигурация, стандартная библиотека, фреймворк, текущая зависимость или проектный `helper` решают ту же задачу;
- новую зависимость без `negative_dependency_rule`, отклоненных альтернатив, совместимости и доказательств отката или удаления;
- `refactor`, который меняет `legacy seams` без `characterization tests` или явного `accepted gap`;
- поверхностный `wrapper`, `clever abstraction` или комментарии, которые пересказывают код вместо объяснения намерения, `invariant`, риска или `trade-off`;
- неподтвержденные `claims` вроде `clean`, `simple`, `senior`, `safe` или `minimal` без доказательств.

Предпочтения только по стилю не являются `blockers`, если они не создают `behavioral`, `operational`, `security` или `maintainability risk`.

## Parallel review

Для больших PR можно явно попросить subagents:

```text
Use one parallel subagent per review track:
- Security risks
- Correctness bugs
- Test gaps
- Maintainability

Wait for all agents and return a consolidated review.
Do not include duplicate findings.
```

## Verification

- Проверить, что findings ссылаются на реальные файлы и строки.
- Запросить reproduction или failing test для каждого high-severity bug.
- Не принимать stylistic comments как blockers без behavioral risk.
- Отсутствие доказательств профессионального кодирования считать `review gap`, а не доказательством `runtime behavior`.
