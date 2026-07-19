from healthCheck.alerts.telegram import send_telegram_message


def build_alert_message(report):
    lines = [
        " System Health Alert",
        f"Host: {report['host']}",
        f"Status: {report['status']}",
        "",
        "Problem checks:",
    ]

    has_problem = False

    for check in report["checks"]:
        if check["status"] != "OK":
            has_problem = True
            lines.append(
                f"- {check['name']}: {check['value']}{check['unit']} "
                f"({check['status']}) - {check['message']}"
            )

    if not has_problem:
        lines.append("- No problems detected.")

    return "\n".join(lines)


def send_alert_if_needed(report, alert_provider):
    if not alert_provider:
        return False

    if report["status"] == "OK":
        return False

    message = build_alert_message(report)

    if alert_provider.lower() == "telegram":
        send_telegram_message(message)
        return True

    raise ValueError(f"Unsupported alert provider: {alert_provider}")