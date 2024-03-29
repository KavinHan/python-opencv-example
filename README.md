# python-opencv-example
python3 opencv server example

### command flow for run server

```bash
$> sudo apt-get update
# install git
$> sudo apt-get install git
# download example code from github
$> git clone https://github.com/KavinHan/python-opencv-example.git
# open code root folder
$> cd python-opencv-example
# install python3 virtual environment
$> sudo apt-get install python3-venv
# create virtual environment using python3
$> python3 -m venv venv
# run virtual environment
$> source venv/bin/active
# install package
$> pip install flask
$> pip install opencv-python
# run server
$> python server.py
```

### install pycharm for develop python project
[download link](https://www.jetbrains.com/pycharm/download/#section=linux)

1. download and unzip
2. open python project
3. run `charm .` open project by pycharm


### using mysql
```bash
# active virtual environment first
$> source venv/bin/active
# install pymysql 
$> pip install PyMySQL

```

**image table**
```
CREATE TABLE `image` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `original_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'original image url',
  `result_url` varchar(255) NOT NULL DEFAULT '' COMMENT 'result image url',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
```

#### Reference
- https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
- https://www.roytuts.com/python-flask-file-upload-example/
- https://www.techcoil.com/blog/serve-static-files-python-3-flask/
- https://pymysql.readthedocs.io/en/latest/user/installation.html