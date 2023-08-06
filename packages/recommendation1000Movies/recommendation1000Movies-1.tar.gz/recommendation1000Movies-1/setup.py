from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name = 'recommendation1000Movies',
        packages=find_packages(),
        include_package_data = True,
        version = '1',
        license='MIT',
        description = 'Recommending movies based on text synopsis using DistilBERT',
        author = 'Ugo Tanielian',
        author_email = 'firstname.lastname@outluuk.fr',  
        url = 'https://github.com/tanouch/recommending_movies',
        entry_points={"console_scripts": ["recommendation1000Movies = recommending_movies.movie_recommendations:main"]},
        keywords = ['NLP', 'movies'],
        install_requires=[
            "numpy",
            "wikipedia",
            "transformers",
            "torch", 
            "fire",
            "scipy"
        ],
        #package_data={"":['data/movie_summaries.json', 'data/movie_vectors.json']},
        data_files=[('', ['recommending_movies/data/movie_summaries.json', 'recommending_movies/data/movie_vectors.json'])],
        classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        ]
    )
