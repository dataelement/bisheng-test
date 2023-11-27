import os
import shutil


def clear_allure():
    """
    shutil.rmtree( src )   #递归删除一个目录以及目录内的所有内容
    os.makedirs() 方法用于递归创建目录。
    解决allure报告缓存问题，防止大文件过多
    """

    filepath = os.environ.get('ALLURE_RESULT_PATH', '/app/output/allure_result')
    if os.path.exists(filepath):
        shutil.rmtree("{}".format(filepath))
        os.makedirs("{}".format(filepath))
    else:
        os.makedirs("{}".format(filepath))

    path_report = os.environ.get(
        'ALLURE_RESULT_PATH', '/app/output/allure_report')
    if os.path.exists(path_report):
        shutil.rmtree("{}".format(path_report))


