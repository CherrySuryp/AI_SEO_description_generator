#!/usr/bin/env python
import asyncio
import sentry_sdk
from business_logic import BusinessLogic

sentry_sdk.init(
    dsn="https://7d76275f622495a2e5f5eff763dde248@o4505459592200192.ingest.sentry.io/4505710500249600",
    traces_sample_rate=1.0
)


def main() -> None:
    print('Started')
    business_logic = BusinessLogic()
    asyncio.run(business_logic.fetcher_worker())


if __name__ == '__main__':
    main()
