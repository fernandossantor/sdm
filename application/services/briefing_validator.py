class BriefingValidator:

    REQUIRED_FIELDS = [

        "company",

        "product",

        "target_audience",

        "objectives",

        "budget"

    ]

    @classmethod
    def progress(cls, briefing):

        if briefing is None:

            return 0

        completed = 0

        for field in cls.REQUIRED_FIELDS:

            value = briefing.get(field)

            if value not in (

                None,

                "",

                0

            ):

                completed += 1

        return int(

            completed

            /

            len(cls.REQUIRED_FIELDS)

            * 100

        )