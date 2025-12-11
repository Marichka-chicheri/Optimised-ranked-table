from setuptools import setup

setup(
    name='optimized-ranking-table',
    version='0.1.0',
    description="Optimized ranking table using PageRank algorithm for tournament analysis.",
    author="Khrystyna Shymushovska, Anton Vertyporokh, Mariia Fedorenko, "
           "Pavlo Danylkiv, Ustym Trukhin, Viktoriia Hrebeniuk",
    author_email="shymushovska.pn@ucu.edu.ua, vertyporokh.pn@ucu.edu.ua, fedorenko.pn@ucu.edu.ua, "
            "danylkiv.pn@ucu.edu.ua, trukhin.pn@ucu.edu.ua, v.hrebeniuk.pn@ucu.edu.ua",
    py_modules=['optimized_ranking_table'],
    entry_points={
        'console_scripts': [
            'tournament=optimized_ranking_table:main',
        ],
    },
)
