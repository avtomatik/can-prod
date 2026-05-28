from econcan.providers.statcan.provider import StatCanProvider

_provider = StatCanProvider()

ARCHIVE_IDS = [3800106, 3800566, 18100081, 36100210]

for archive_id in ARCHIVE_IDS:
    print(_provider.load_table(archive_id))
