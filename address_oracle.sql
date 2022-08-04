alter session set "_oracle_script"=true;
create user spring identified by java;
grant connect, resource, unlimited tablespace to spring;
conn spring/java;


drop table ADDRESS;
drop sequence ADDRESS_SEQ;

create table ADDRESS(
   SEQ number constraint ADDRESS_PK primary key, 
   NAME varchar2(10), 
   ADDR varchar2(20), 
   RDATE date
); 
create sequence ADDRESS_SEQ increment by 1 start with 1 nocache;

insert into ADDRESS values(ADDRESS_SEQ.nextval, 'ȫ�浿', '�����', SYSDATE);
insert into ADDRESS values(ADDRESS_SEQ.nextval, '�̼���', '�λ��', SYSDATE);
insert into ADDRESS values(ADDRESS_SEQ.nextval, '������', '��õ��', SYSDATE);
insert into ADDRESS values(ADDRESS_SEQ.nextval, '������', '���ֽ�', SYSDATE);

commit;

select CONSTRAINT_NAME, CONSTRAINT_TYPE from user_constraints where TABLE_NAME='ADDRESS';
select * from ADDRESS;



Record �߰�
1.from django.utils import timezone
address = Address(name = 'ȫ�浿', addr='�����', rdate=timezone.now())
address.save()

Address.objects.all().values()

2.import datetime  
from pytz import timezone
now = datetime.datetime.now(timezone('Asia/Seoul'))
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
address = Address(name = '������', addr='��õ��', rdate = nowDatetime)
address.save()

Address.objects.all().values()

3.N��

Record ����

1.address = address.object.get(id = 2)
address.delete()
2.





