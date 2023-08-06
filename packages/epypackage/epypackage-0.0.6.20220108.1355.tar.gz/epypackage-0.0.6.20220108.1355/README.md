由于没学会git合并~~~

在原模块上进行添加pyefun

修改 code version

py -m build

有坑 要先上传测试 在上传正式 要不然不知道为什么找不到模块
py -m twine upload --repository testpypi dist/*
py -m twine upload --repository pypi dist/*


https://pypi.org/project/epypackage/0.0.5.20220108.1326/
pip install epypackage==0.0.5.20220108.1326