#!/usr/bin/env python
import asyncio
import sentry_sdk
from business_logic import BusinessLogic


def main() -> None:
    print('Started')
    business_logic = BusinessLogic()
    asyncio.run(business_logic.fetcher_worker())


if __name__ == '__main__':
    sentry_sdk.init(
        dsn="https://49a5d4df70ce2f39664e6523ece689c8@o4505459592200192.ingest.sentry.io/4505710328414208",
        traces_sample_rate=1.0
    )
    main()
