from setuptools import setup, find_packages

setup(
    name='DRFTrabajo',  # Nombre de tu paquete/distribución
    version='0.1.0',  # La versión de tu paquete
    author='Tu Nombre',  # Tu nombre o el de tu organización
    author_email='tu.email@example.com',  # Tu correo electrónico o el de tu organización
    description='Una descripción corta de tu proyecto',  # Una breve descripción de tu proyecto
    long_description=open('README.md').read(),  # Una descripción larga, puede ser tu README
    long_description_content_type='text/markdown',  # Indica que tu archivo README.md es Markdown
    url='http://url-a-tu-proyecto.com',  # La URL de tu proyecto (si aplica)
    packages=find_packages(where='src'),  # Dónde encontrar los paquetes de Python
    package_dir={'': 'src'},  # Diccionario que indica dónde están los paquetes
    include_package_data=True,  # Incluir archivos no-Python especificados en MANIFEST.in
    install_requires=[
        # Lista de dependencias de tu paquete, por ejemplo:
        # 'numpy >= 1.18.1',
        # 'pandas >= 1.0.3',
    ],
    classifiers=[
        # Clasificadores de PyPI para indicar quién debería usarlo, de qué trata, etc.
        # Consulta: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
    entry_points={
        # Puntos de entrada, por ejemplo, scripts que se ejecutarán en la línea de comandos
        # 'console_scripts': ['nombre-script = nombre_paquete.modulo:funcion_main'],
    },
)

    