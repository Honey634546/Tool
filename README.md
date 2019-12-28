# downloadPDF

此工具用于下载网页到本地，保存为pdf

## 起因
>运营学院公众号时，需要将每篇推文保存成pdf进行存档归类，以前都是由人工完成，速度太慢。于是想写个小工具加快速度
>只对自己的公众号进行了测试，其他不清楚，一般的网页估计是不行的

## 已知BUG
>pdfkit.from_file(html, file_name, options=options)

>>raise IOError("wkhtmltopdf exited with non-zero code {0}. error:\n{1}".format(exit_code, stderr))
>>OSError: wkhtmltopdf exited with non-zero code 1. error:

>虽然报错，但是还是会正确的的输出pdf？？
>目前把他加入try里面了

## 已知缺陷
>没有将中间产生的文件（图片，html文件等）删除
