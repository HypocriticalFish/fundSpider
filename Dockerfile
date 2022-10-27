#pull python3.10.7-spider-baseenv:v1
FROM 10.4.2.100:31204/fund-invest-research/python3.10.7-spider-baseenv:v1

#COPY代码
COPY . /tiantianfund-crawler/
WORKDIR /tiantianfund-crawler/

ENTRYPOINT ["sh", "-c", "start.sh"]

