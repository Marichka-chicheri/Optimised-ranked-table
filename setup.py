from setuptools import setup

setup(
    name='Optimased-ranked-table',
    version='0.1.0',
    description="Optimased ranked table, which analysis the data in the file and show it like the graph.",
    author="Khrystyna Shymushovska, Anton Vertyporokh, Mariia Fedorenko, "
           "Pavlo Danylkiv, Ustym Trukhin, Viktoriia Hrebeniuk",
    author_email="shymushovska.pn@ucu.edu.ua, vertyporokh.pn@ucu.edu.ua, fedorenko.pn@ucu.edu.ua, "
            "danylkiv.pn@ucu.edu.ua, trukhin.pn@ucu.edu.ua, v.hrebeniuk.pn@ucu.edu.ua",
    packages=['optimized_ranking_table'],
    entry_points={
        'console_scripts': [
            'tournament=optimized_ranking_table:main',
        ],
    },
)
