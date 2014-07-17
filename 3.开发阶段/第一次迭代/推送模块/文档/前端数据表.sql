drop table IF EXISTS tbl_help;
drop table IF EXISTS tbl_aid;
drop table IF EXISTS tbl_user;

/*
�¼���
id:����id
eventid:�¼�id
username:�����ߵ��û���
avatar:������ͷ���URL��ַ
content:������Ϣ����
time:����������Ϣ��ʱ��
kind:�¼�����(��ȫ���������)
attention:��ע����
participants:��������
state:�¼�״̬(�����У�����)
*/
CREATE TABLE tbl_help (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
avatar TEXT,
content TEXT,
time TEXT,
kind INTEGER,
attention INTEGER,
participants INTEGER,
state INTEGER
);

/*
������
�����¼�������ͼƬ���������ļ�
eventid:�¼�id
filename:�����ļ�����
path:�������ص�ַ��洢·��
state:����״̬(0-δ���أ�1-������)
type:��������(0-ͼƬ��1-��Ƶ��2-��Ƶ)
*/
CREATE TABLE tbl_attachment (
eventid INTEGER,
filename TEXT,
path TEXT,
state INTEGER,
type INTEGER
);

/*
ͷ���
username:�û���
path:ͷ���ļ��洢·��
*/
CREATE TABLE tbl_avatar (
username TEXT,
path TEXT
);

/*
Ԯ����Ϣ��
eventid:�¼�id
username:Ԯ���ߵ��û���
avatar:Ԯ����ͷ���URL��ַ
content:Ԯ����Ϣ����
time:����Ԯ����Ϣ��ʱ��
*/
CREATE TABLE tbl_aid (
eventid INTEGER,
username TEXT,
avatar TEXT,
content TEXT,
time TEXT
);

/*
���ѱ�
id:����id
avatar:ͷ��URL��ַ
username:�û���
info:�û����
group:����(0-��������1-���ˣ�2-���ѣ�3-İ����)
*/
CREATE TABLE tbl_user (
id INTEGER PRIMARY KEY AUTOINCREMENT,
avatar TEXT,
username TEXT,
info TEXT,
group INTEGER
);