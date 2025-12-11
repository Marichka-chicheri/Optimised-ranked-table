from setuptools import setup

setup(
<<<<<<< HEAD
    name='optimized-ranking-table',
    version='0.1.0',
    description="Optimized ranking table using PageRank algorithm for tournament analysis.",
=======
    name='Optimased-ranked-table',
    version='0.1.0',
    description="Optimased ranked table, which analysis the data in the file and show it like the graph.",
>>>>>>> a4c6972050285cf2cd476eef003c35f9823df60e
    author="Khrystyna Shymushovska, Anton Vertyporokh, Mariia Fedorenko, "
           "Pavlo Danylkiv, Ustym Trukhin, Viktoriia Hrebeniuk",
    author_email="shymushovska.pn@ucu.edu.ua, vertyporokh.pn@ucu.edu.ua, fedorenko.pn@ucu.edu.ua, "
            "danylkiv.pn@ucu.edu.ua, trukhin.pn@ucu.edu.ua, v.hrebeniuk.pn@ucu.edu.ua",
<<<<<<< HEAD
    py_modules=['optimized_ranking_table'],
=======
    packages=['optimized_ranking_table'],
>>>>>>> a4c6972050285cf2cd476eef003c35f9823df60e
    entry_points={
        'console_scripts': [
            'tournament=optimized_ranking_table:main',
        ],
    },
)
