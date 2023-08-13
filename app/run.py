#!/usr/bin/env python
import asyncio
from business_logic import BusinessLogic


def main() -> None:
    print('Started')
    business_logic = BusinessLogic()
    asyncio.run(business_logic.fetcher_worker())


if __name__ == '__main__':
    main()
