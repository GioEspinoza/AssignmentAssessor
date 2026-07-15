# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability or exposed
credential. Instead, use GitHub's private vulnerability reporting feature for
this repository.

Include the affected component, reproduction steps, and potential impact.
Reports will be acknowledged as soon as practical.

## Credential handling

- Never commit `.env` files or database connection strings.
- Use `.env.example` for documented placeholder values only.
- Rotate a credential immediately if it may have entered Git history.
- Use a dedicated development database account with the least required access.
