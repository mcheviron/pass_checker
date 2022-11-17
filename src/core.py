import asyncio
import hashlib
from typing import Generator, List, Tuple

import httpx


def pwned(suffix: str, ls_hashes: Generator) -> Tuple[bool, int]:
    """
    Checks whether the password's hash suffix is found in the returned
    hash suffix and infer whether the password was thus pwned before or not

    Args:
        suffix (str): The suffix to check
        ls_hashes (Generator): The list of returned hash suffix that need to
        be checked for a match

    Returns:
        Tuple: A tuple of bool value for whether the password has been
        leaked before or not and the number of times it has been
        leaked/found in the databases
    """
    # A more descriptive way of doing the line of code below

    # for hash, num in hashes:
    #     if hash == suffix:
    #         return (True, num)
    #     return (False, 0)

    return next(
        ((True, num) for hash, num in ls_hashes if hash == suffix), (False, 0)
    )
    # Vanila try
    # return any(suffix == k for k, v in ls_hashes)


def hash(password: str) -> Tuple[str, str]:
    """
    Uses SHA-1 to hash the password

    Args:
        password (str): The password to be hashed

    Returns:
        Tuple[str, str]: The prefix and suffix of the bifurcated hash
    """
    pass_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = pass_hash[:5], pass_hash[5:]
    return (prefix, suffix)


async def fetch_hashes(prefix: str) -> Generator:
    """
    Uses k-anonymity to ensure that your password never really traverses
    the internet. A hash digest is bifurcated into two and the prefix is
    sent to the databases. A list of suffixes is returned and these
    suffixes are later shearched for a matching suffix to determine
    whether the password has been pwned or not in the past

    Args:
        prefix (str): The prefix of the passowrd to be checked

    Returns:
        Generator: The returned suffixes in the form of generator rather than
        a list
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        return (line.split(":") for line in r.text.splitlines())


async def run_coros(*prefixes) -> List[Tuple[str, Generator]]:
    """
    Runs the coroutines that fetch the hashes from the remote databases

    Returns:
        List[Tuple[str, Generator]]: A list of tuples of prefixes and
        the hash suffixes returned, in the form of a generator
    """
    # tasks = [asyncio.create_task(fetch_hashes(prefix)) for prefix in prefixes]
    tasks = [fetch_hashes(prefix) for prefix in prefixes]
    gens = await asyncio.gather(*tasks)
    return list(zip(prefixes, gens))
