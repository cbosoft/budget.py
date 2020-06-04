from distutils.core import setup

def main():
    setup(
        name='budget',
        description='simple budget management in python',
        version='0.1',
        packages=['budget'],
        install_requires=[
            'matplotlib',
        ]
    )

if __name__ == "__main__":
    main()
