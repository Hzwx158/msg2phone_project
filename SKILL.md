---
name: msg2phone
description: "Send owner notifications from the shared hzwx158 workspace with the installed msg2phone CLI. Use when a user asks to notify a phone, Feishu, or ServerChan; when a workspace workflow requires an owner decision, manual action, progress update, failure alert, or completion notice; or when integrating msg2phone into Python or shell work under hzwx158. Do not send from offline GPU jobs or expose notification credentials."
---

# Send workspace notifications

Set the workspace root explicitly:

```bash
HROOT=/inspire/qb-ilm/project/advanced-machine-learning/yanjunchi-24040/hzwx158
```

## Send safely

- Send from the networked CPU/login node, never from a scheduler command or offline GPU script.
- Use the installed ELF executable. Do not reinstall the package merely because this source tree exists.
- Never run `config --show`, print `config.yaml`, or expose endpoints, app secrets, tokens, or recipient identifiers.
- Treat a user request to notify as authorization to send. For workspace workflows, treat required Feishu owner notifications as pre-authorized.

```bash
"$HROOT/envs/elf/bin/msg2phone-cli" send \
  -n "<configured-name>" \
  -t "<title>" \
  -m "<actionable-message>" \
  --tags "<project-tag>"
```

Use the tag for the current conversation or project. Known tags include `rebuttal`, `streaming`, and `quantum`; do not reuse one for an unrelated task.

## Notify for owner dependencies

Send before asking the owner to approve an action or choose between material options. Also send when the owner must manually submit an experiment. For an experiment-submission handoff, use the exact title `手动提交要求` and include:

- the exact command;
- when it is safe to run;
- requested node and resources;
- task and durable log names.

Do not use that title for ordinary status, failures, stalled queues, or server-start requests. During long work, send concise updates at meaningful milestones, stalls, failures, completion, or roughly every two hours when useful.

## Configure or extend only when needed

If configuration is missing or the user asks to add a messenger, read `README.md` and the relevant source completely before changing anything. Ask before modifying an environment or persistent configuration. Keep configuration files and delivery responses out of reports and logs.
