# Импорт недавно установленного пакета setuptools.
import setuptools

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    name="pymultilang",
    version="1.1",
    author="Bekhruz Iskandarzoda",
    author_email="avesto.inn@gmail.com",
    description="Multi-language support for your project",
    url="https://github.com/avestoinn/pymultilang",
    packages=["pymultilang"],
    python_requires='>=3.6',
)
