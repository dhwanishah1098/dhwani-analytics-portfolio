# Automated BI Reports

**Tech:** Python · SQLAlchemy · Jinja2 · openpyxl · schedule · SMTP

## What it does
Replaces manual weekly/monthly report generation with a fully automated pipeline:
SQL query runner → HTML rendering → Excel export → scheduled email delivery.

## Key features
- Parameterised SQL query templates for easy customisation
- Jinja2 HTML email templates with KPI summary cards
- RAG status flagging (Red/Amber/Green) for budget variance
- Churn risk identification query for reactivation targeting
- Query result caching with configurable TTL
- Slack webhook integration for delivery alerts

## Outcome
Designed to reduce report turnaround from 2 days to under 6 hours.

[View repo →](https://github.com/dhwanishah1098/automated-bi-reports)
