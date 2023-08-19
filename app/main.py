#!/usr/bin/env python
import asyncio

from config import settings
from business_logic import TaskService

import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    integrations=[sentry_logging],
)


def main() -> None:
    print("Program has started")
    asyncio.run(TaskService().fetcher_worker())


if __name__ == "__main__":
    main()
