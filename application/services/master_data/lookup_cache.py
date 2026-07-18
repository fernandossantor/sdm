from application.services.master_data_service import MasterDataService


class LookupCache:

    _cache = {}

    @classmethod
    def labels(cls, table, label="name"):

        key = f"{table}:{label}"

        if key not in cls._cache:

            rows = MasterDataService(table).list()

            cls._cache[key] = {
                row["id"]: row.get(label, "")
                for row in rows
            }

        return cls._cache[key]

    @classmethod
    def clear(cls):

        cls._cache.clear()