#!/usr/bin/env python
import asyncio
import logging
from business_logic import TaskService

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

sentry_sdk.init(
    dsn="https://7d76275f622495a2e5f5eff763dde248@o4505459592200192.ingest.sentry.io/4505710500249600",
    traces_sample_rate=1.0,
    integrations=[sentry_logging],
)


def main() -> None:
    print("Program has started")
    asyncio.run(TaskService().fetcher_worker())


if __name__ == "__main__":
    main()
