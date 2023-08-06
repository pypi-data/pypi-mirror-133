from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="itkaven",  # 这里是pip项目发布的名称
    version="1.0.1",  # 版本号，数值大的会优先被pip
    keywords=["pip", "itkaven"],
    description="test",
    long_description="test",
    license="MIT Licence",

    # url="https://github.com/LiangjunFeng/SICA",  # 项目相关文件地址，一般是github
    author="LiangjunFeng",
    author_email="1433188757@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    # install_requires=[]  # 这个项目需要的第三方库
)
