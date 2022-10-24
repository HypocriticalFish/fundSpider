#
#   @Author Hypocritical Fish
#   @Create 2022/10/15 21:51
#   @Description    爬取天天基金投顾产品的数据
import datetime
import sys

import requests
import time

from loggers import get_logger
from urllib3.exceptions import InsecureRequestWarning
from utils import get_headers, get_db_connection

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = get_logger(True)


# 获取投顾产品id列表
def get_partner_id_list():
    url = 'https://universalapi.1234567.com.cn/hxfundtrade/auxiliary/kycPartnerList'
    host = 'universalapi.1234567.com.cn'
    referer = 'https://mpservice.com/b0381a3b634440379d330b69f09d3f8e/release/pages/selectStrategy/index'
    headers = get_headers(host, referer, '')
    params = {
        'headers': '{content-type=application/json}'
    }
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    response.encoding = 'utf-8'
    partner_id_list = response.json().get('data')
    log.info("投顾产品总数：" + str(len(partner_id_list)))
    return partner_id_list


# 根据partnerId获取基本信息
def get_base_info(partner_id):
    url = 'https://uni-fundts.1234567.com.cn/combine/investAdviserInfo/getAgencyConfigInfo'
    host = 'uni-fundts.1234567.com.cn'
    referer = 'https://mpservice.com/funda91a99886abf7e/release/pages/question/index?partnerId=' + partner_id
    headers = get_headers(host, referer, '')
    params = {
        'partnerId': partner_id,
    }
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    response.encoding = 'utf-8'
    data = response.json().get('Data')
    base_item = {
        'partnerId': data['partnerId'],
        'companyId': data['companyId'],
        'companyName': data['provider'],
        'brand': data['appletName'],
        'inRateInfo': data['inRateInfo']
    }
    return base_item


# 获取品牌信息
def get_brand_info(partner_id, strategy_id):
    url = 'https://dataapi.1234567.com.cn/dataapi/IAAGGR/FundIATGInfoAggr'
    host = 'dataapi.1234567.com.cn'
    referer = 'https://mpservice.com/funda91a99886abf7e/release/pages/strategyDetail/index?partnerId=' + partner_id + '&id=' + strategy_id
    headers = get_headers(host, referer, '')
    params = {
        'FIELDS': 'TGNAME,ESTABDATE,RISKLEVEL,BASIC_CAL_FORMULA_REMARK,STGCONCEPT,MINBUY,STRATEGY_RATE,STRATEGY_RATE,STRATEGY_RATE_DISCOUNT,SYL_Z,BENCHSYL_Z,SYL_Y,BENCHSYL_Y,SYL_3Y,BENCHSYL_3Y,SYL_6Y,BENCHSYL_6Y,SYL_1N,BENCHSYL_1N,SYL_2N,BENCHSYL_2N,SYL_3N,BENCHSYL_3N,SYL_JN,BENCHSYL_JN,SYL_LN,BENCHSYL_LN',
        'TGCODE': strategy_id
    }
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    response.encoding = 'utf-8'
    data = response.json().get('data')[0]
    return data


# 获取扩展信息
def get_extend_info(partner_id, strategy_id):
    url = 'https://uni-fundts.1234567.com.cn/combine/investAdviserAggr/tgStgSceneAggrByCodeList'
    host = 'uni-fundts.1234567.com.cn'
    referer = 'https://mpservice.com/funda91a99886abf7e/release/pages/question/index?partnerId=' + partner_id
    headers = get_headers(host, referer, '')
    params = {
        'codeList': strategy_id
    }
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    response.encoding = 'utf-8'
    data = response.json().get('data')
    if data is not None and len(data) != 0:
        data = response.json().get('data')[0]['sceneList'][0]['strategyList'][0]
        data['categoryName'] = response.json().get('data')[0]['sceneList'][0]['categoryName']
        return data
    else:
        return {}


# 获取指定id的投顾产品的策略id集合
def get_strategy_id_set(partner_id):
    url = 'https://universalapi.1234567.com.cn/hxfundtrade/auxiliary/kycQuestionV2'
    host = 'universalapi.1234567.com.cn'
    referer = 'https://mpservice.com/funda91a99886abf7e/release/pages/question/index?partnerId=' + partner_id
    headers = get_headers(host, referer, '')
    params = {
        'partner': partner_id,
    }
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    response.encoding = 'utf-8'
    content = response.json().get('data')
    log.info('开始爬取' + content['investConsultName'] + '的投顾策略...')
    strategy_id_set = set()
    for item in content['ruleList']:
        strategy_id_list = item['strategyId'].replace('*', '').replace('&', ',').split(',')
        for strategy_id in strategy_id_list:
            if strategy_id != '0':
                strategy_id_set.add(strategy_id)
    log.info('爬取' + content['investConsultName'] + '旗下共计' + str(len(strategy_id_set)) + '条投顾策略...')
    return strategy_id_set


# 获取备选基金池
def getStrategyPool(partner_id, strategy_id):
    url = 'https://h5.1234567.com.cn/AggregationStaticService/GetCustomBusinessInterfaceWithSchema/StrategyFundPoolAggr'
    host = 'h5.1234567.com.cn'
    referer = 'https://mpservice.com/funda91a99886abf7e/release/pages/fundLibrary/index?id=' + strategy_id + '&partnerId=' + partner_id
    headers = get_headers(host, referer, 'application/x-www-form-urlencoded')
    data = {
        'p': '1',
        'FIELDS': 'JJGSID,TGCODE,FCODE,FNAME,FTYPE,FTYPENAME',
        'ps': '10000',
        'TGCODE': strategy_id,
    }
    response = requests.post(url=url, data=data, headers=headers, verify=False)
    response.encoding = 'utf-8'
    content = response.json()['data']['StrategyFundPool']
    return content


# 获取策略全部信息
def get_strategy_info(partner_id, company_id, strategy_id):
    url = 'https://h5.1234567.com.cn/AggregationStaticService/chooseCustomRouter/getStrategyDetailAggr'
    host = 'h5.1234567.com.cn'
    referer = 'https://mpservice.com/funda91a99886abf7e/release/pages/strategyDetail/index?partnerId=' + partner_id + '&id=' + strategy_id
    headers = get_headers(host, referer, 'application/x-www-form-urlencoded')
    data = {
        'partner': partner_id,
        'MobileKey': 'e952ac58c6c75cb128a59455b39a0b24||iemi_tluafed_me',
        'UserId': '95c68e3ae0884f828ecedea62eb3e24c',
        'PassportId': '2884496638254532',
        'UToken': 'T2C6uy5YFLoZPtBR-oOL1orUhSKBUIszzKk6vaI6ku7voy6Zf6IfNupjnditqV_RzgSj0Zz4XY0JUdNVbTd5J7EvcDAHmcb2JR9JQHjyIugNb_jj7FOjDbxEe89ErH28dUsxzQFtg92npSVcETB6DGDq9MKWkjcnbjvXs01zAAg.12',
        'tag': '0',
        'displayId': strategy_id,
        'JJGSID': company_id,
        'tgCode': strategy_id,
        'CToken': 'dvPbcblCxG2nGQGU1msJDSQOcDdWmwG9wOJchTPrqhvoOqkWiNShgsapqwdQNVvpZJSMq3KG4hRe94ruyJ2SmDEbJMna8VOdX763fFasdKw1omuMb6DmnKDK1VdI6RFluxzsz-_8rBlb9DSyqj-XrUHRPlSu8eP-Aj60BOuGzAfuO4U5Jmluj7Z0ZRr1J6w_ZtpsGN9skZ-zpZpljuga5mDkSbcBIB3qWzUdB0YPumA.12',
        'TGCODE': strategy_id,
    }
    response = requests.post(url=url, data=data, headers=headers, verify=False)
    response.encoding = 'utf-8'
    content = response.json()['data']
    return content


def init_db():
    # 创建数据库
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS tt_fund DEFAULT CHARACTER SET utf8"
    )
    connection.select_db('tt_fund')

    # 创建基本信息表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS base_info (id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),company_name VARCHAR(20),brand VARCHAR(20),strategy_name VARCHAR(20),class VARCHAR(10),create_date DATE,risk_level INT,basic_remark VARCHAR(200),recommend_hold VARCHAR(10),feature VARCHAR(500),concept VARCHAR(500),min_buy FLOAT,service_rate FLOAT,transfer_in_rate FLOAT, update_time DATETIME DEFAULT NOW())"
    )

    # 创建日收益表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS day_profit(id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),strategy_name VARCHAR(20),date_ DATE,SE FLOAT,BENCH_SE FLOAT)"
    )
    # 清空日收益表，实现覆盖写入
    cursor.execute(
        "TRUNCATE TABLE day_profit"
    )

    # 创建区间收益表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS interval_profit(id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),strategy_name VARCHAR(20),last_date DATE,week_profit FLOAT,week_bench FLOAT,month_profit FLOAT,month_bench FLOAT,thrmonth_profit FLOAT,thrmonth_bench FLOAT,halfyear_profit FLOAT,halfyear_bench FLOAT,year_profit FLOAT,year_bench FLOAT,twoyear_pforit FLOAT,twoyear_bench FLOAT,thryear_profit FLOAT,thryear_bench FLOAT,curyear_profit FLOAT,curyear_bench FLOAT,total_profit FLOAT,total_bench FLOAT,update_time DATETIME DEFAULT NOW())"
    )

    # 创建持仓分布表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS hold_warehouse_info(id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),strategy_name VARCHAR(20),date_ DATE,fund_code VARCHAR(10),fund_name VARCHAR(30),fund_type VARCHAR(10),ratio FLOAT,update_time DATETIME DEFAULT NOW())"
    )

    # 创建调仓记录表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS adjust_warehouse_history(id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),strategy_name VARCHAR(20),date_ DATE,reason VARCHAR(1000))"
    )
    # 清空调仓记录表，实现覆盖写入
    cursor.execute(
        "TRUNCATE TABLE adjust_warehouse_history"
    )

    # 创建调仓详情表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS adjust_warehouse_detail(id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),strategy_name VARCHAR(20),date_ DATE,fund_code VARCHAR(10),fund_name VARCHAR(30),fund_type VARCHAR(10),pre_ratio FLOAT,after_ratio FLOAT)"
    )
    # 清空调仓详情表，实现覆盖写入
    cursor.execute(
        "TRUNCATE TABLE adjust_warehouse_detail"
    )

    # 创建备选基金表
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS strategy_pool(id INT AUTO_INCREMENT PRIMARY KEY,strategy_id VARCHAR(10),strategy_name VARCHAR(20),fund_code VARCHAR(10),fund_name VARCHAR(30),fund_type VARCHAR(10),update_time DATETIME DEFAULT NOW())"
    )


# 组装投顾策略的基本信息，并添加到列表中
def get_all_info(strategy_id, base_item):
    partner_id = base_item['partnerId']
    # 获取详细信息
    detail_info = get_strategy_info(partner_id, base_item['companyId'], strategy_id)
    # 基本数据
    base_data = detail_info['baseData']['data']
    # 基本数据为空则不解析
    if base_data is None or len(base_data) == 0:
        global skip_count
        skip_count = skip_count + 1
        log.warning(base_item['companyName'] + "旗下的" + base_item[
            'brand'] + "中id为" + strategy_id + "的投顾策略基本信息缺失，无法解析!即将解析下一条投顾策略...")
        return None
    # 获取品牌信息
    brand_info = get_brand_info(partner_id, strategy_id)
    # 获取拓展信息
    extend_info = get_extend_info(partner_id, strategy_id)
    # 获取备选基金信息
    strategy_pool_info = getStrategyPool(partner_id, strategy_id)

    # 推荐持有
    recommend_hold_time = detail_info['baseData']['data'].get('recommendHoldTime', '')

    create_date = datetime.datetime.strptime(detail_info['targetProfitInfo']['data'][0]['ESTABDATE'],
                                             '%Y-%m-%d %H:%M:%S').date()

    # 基本信息入库
    base_info_values = (
        strategy_id,
        base_item['companyName'],
        base_item['brand'],
        brand_info['TGNAME'],
        extend_info.get('categoryName', ''),
        create_date,
        int(brand_info['RISKLEVEL']),
        brand_info['BASIC_CAL_FORMULA_REMARK'],
        recommend_hold_time,
        extend_info.get('resume', ''),
        brand_info['STGCONCEPT'],
        float(brand_info['MINBUY']),
        float(brand_info['STRATEGY_RATE_DISCOUNT']),
        float(brand_info['STRATEGY_RATE'])
    )

    basic_item_list.append(base_info_values)
    log.info('\t' + brand_info['TGNAME'] + '基本信息爬取成功')

    # 收集区间收益信息：
    # 最新净值日期
    last_date = datetime.datetime.strptime(detail_info['targetProfitInfo']['data'][0]['SYRQ'], '%Y-%m-%d').date()

    week_profit = brand_info.get('SYL_Z', None)
    week_bench = brand_info.get('BENCHSYL_Z', None)
    month_profit = brand_info.get('SYL_Y', None)
    month_bench = brand_info.get('BENCHSYL_Y', None)
    thrmonth_profit = brand_info.get('SYL_3Y', None)
    thrmonth_bench = brand_info.get('BENCHSYL_3Y', None)
    halfyear_profit = brand_info.get('SYL_6Y', None)
    halfyear_bench = brand_info.get('BENCHSYL_6Y', None)
    year_profit = brand_info.get('SYL_1N', None)
    year_bench = brand_info.get('BENCHSYL_1N', None)
    twoyear_profit = brand_info.get('SYL_2N', None)
    twoyear_bench = brand_info.get('BENCHSYL_2N', None)
    thryear_profit = brand_info.get('SYL_3N', None)
    thryear_bench = brand_info.get('BENCHSYL_3N', None)
    thisyear_profit = brand_info.get('SYL_JN', None)
    thisyear_bench = brand_info.get('BENCHSYL_JN', None)
    total_profit = brand_info.get('SYL_LN', None)
    total_bench = brand_info.get('BENCHSYL_LN', None)

    interval_profit_values = (
        strategy_id,
        brand_info['TGNAME'],
        last_date,
        None if week_profit == '' else float(week_profit),
        None if week_bench == '' else float(week_bench),
        None if month_profit == '' else float(month_profit),
        None if month_bench == '' else float(month_bench),
        None if thrmonth_profit == '' else float(thrmonth_profit),
        None if thrmonth_bench == '' else float(thrmonth_bench),
        None if halfyear_profit == '' else float(halfyear_profit),
        None if halfyear_bench == '' else float(halfyear_bench),
        None if year_profit == '' else float(year_profit),
        None if year_bench == '' else float(year_bench),
        None if twoyear_profit == '' else float(twoyear_profit),
        None if twoyear_bench == '' else float(twoyear_bench),
        None if thryear_profit == '' else float(thryear_profit),
        None if thryear_bench == '' else float(thryear_bench),
        None if thisyear_profit == '' else float(thisyear_profit),
        None if thisyear_bench == '' else float(thisyear_bench),
        None if total_profit == '' else float(total_profit),
        None if total_bench == '' else float(total_bench),
    )
    interval_profit_list.append(interval_profit_values)
    log.info('\t' + brand_info['TGNAME'] + '区间收益信息爬取成功')

    # 持仓信息
    hold_warehouse_info = detail_info['getHoldWarehouseInfo'].get('data', {})
    # 持仓基金类型列表
    fund_type_map = ("QDII", "股票型", "货币型", "混合型", "", "", "债券型", "", "指数型")
    hold_type_list = hold_warehouse_info.get('holdTypeList', [])

    # 收集持仓信息
    if hold_type_list is None or len(hold_type_list) == 0:
        log.warning(brand_info['TGNAME'] + '无持仓分布详细信息')
    else:
        date = datetime.datetime.strptime(hold_warehouse_info.get('date'), '%Y-%m-%d').date()
        for holdType in hold_type_list:
            for fund in holdType['fundsList']:
                # 计算类型
                t = fund['type']
                if t == 'a':
                    t = '0'
                fund_type = fund_type_map[int(t)]
                hold_warehouse_values = (
                    strategy_id,
                    brand_info['TGNAME'],
                    date,
                    fund.get("fundCode", None),
                    fund.get("fundName", None),
                    fund_type,
                    float(fund['ratio']) / 100
                )
                hold_warehouse_list.append(hold_warehouse_values)
        log.info('\t' + brand_info['TGNAME'] + '持仓分布信息爬取成功')

    # 收集调仓历史及详细信息
    adjust_history_list = detail_info['getAdjustWarehouse_1']['data']['adjustHistory']
    for adjust_history in adjust_history_list:
        adjust_date = datetime.datetime.strptime(adjust_history['dateStr'], '%Y-%m-%d').date(),
        adjust_info = (
            strategy_id,
            brand_info['TGNAME'],
            adjust_date,
            adjust_history['reason']
        )
        adjust_warehouse_list.append(adjust_info)
        for adjust_detail in adjust_history['adjustList']:
            for detail in adjust_detail['fundList']:
                # 计算类型
                t = detail['type']
                if t == 'a':
                    t = '0'
                fund_type = fund_type_map[int(t)]
                adjust_detail_values = (
                    strategy_id,
                    brand_info['TGNAME'],
                    adjust_date,
                    detail['fundCode'],
                    detail.get('fundName', ''),
                    fund_type,
                    float(detail['preRatio']) / 100,
                    float(detail['afterRatio']) / 100,
                )
                adjust_detail_list.append(adjust_detail_values)
    log.info('\t' + brand_info['TGNAME'] + '调仓历史信息爬取成功')

    # 备选基金信息入库
    fund_list = strategy_pool_info['data']
    fund_info_list = []
    if fund_list is None:
        log.warning(brand_info['TGNAME'] + '备选基金信息缺失')
    else:
        for fund in fund_list:
            fund_info_values = (
                strategy_id,
                brand_info['TGNAME'],
                fund['FCODE'],
                fund['FNAME'],
                fund['FTYPENAME']
            )
            fund_info_list.append(fund_info_values)
        connection.cursor().executemany(
            "INSERT INTO `strategy_pool`(strategy_id,strategy_name,fund_code,fund_name,fund_type) value(%s,%s,%s,%s,%s)",
            fund_info_list)
        connection.commit()
        log.info('\t' + brand_info['TGNAME'] + '备选基金信息入库成功')

    # 日收益信息入库
    day_profit_list = []
    total_performance = detail_info['strategyProfitChart_ln'].get('data', {})

    for profit in total_performance:
        date = datetime.datetime.strptime(profit['PDATE'], '%Y-%m-%d').date()
        day_profit_list.append((
            strategy_id,
            brand_info['TGNAME'],
            date,
            float(profit['SE']) / 100,
            float(profit['BENCH_SE']) / 100
        ))
    connection.cursor().executemany(
        "INSERT INTO `day_profit`(strategy_id,strategy_name,date_,SE,BENCH_SE) value (%s,%s,%s,%s,%s)",
        day_profit_list)
    connection.commit()
    log.info('\t' + brand_info['TGNAME'] + '日收益信息入库成功\n')


# 记录入库
def save_to_db():
    cursor.executemany(
        "INSERT INTO `base_info`(strategy_id,company_name,brand,strategy_name,class,create_date,risk_level,basic_remark,recommend_hold,feature,concept,min_buy,service_rate,transfer_in_rate) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        basic_item_list)
    cursor.executemany(
        "INSERT INTO `interval_profit`(strategy_id,strategy_name ,last_date,week_profit,week_bench,month_profit,month_bench,thrmonth_profit,thrmonth_bench,halfyear_profit,halfyear_bench,year_profit,year_bench,twoyear_pforit,twoyear_bench,thryear_profit,thryear_bench,curyear_profit,curyear_bench,total_profit,total_bench) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        interval_profit_list)
    cursor.executemany(
        "INSERT INTO `hold_warehouse_info`(strategy_id,strategy_name,date_,fund_code,fund_name,fund_type,ratio) value (%s,%s,%s,%s,%s,%s,%s)",
        hold_warehouse_list)
    cursor.executemany(
        "INSERT INTO `adjust_warehouse_history`(strategy_id,strategy_name,date_,reason) value (%s,%s,%s,%s)",
        adjust_warehouse_list)
    cursor.executemany(
        "INSERT INTO `adjust_warehouse_detail`(strategy_id, strategy_name, date_, fund_code, fund_name, fund_type, pre_ratio, after_ratio) value (%s,%s,%s,%s,%s,%s,%s,%s) ",
        adjust_detail_list)
    connection.commit()
    log.info("爬取的数据入库成功！")


if __name__ == '__main__':
    # 接收命令行的数据库信息
    host = '#'
    port = '#'
    user = '#'
    password = '#'
    if len(sys.argv) != 5:
        log.error("数据库配置信息缺失！")
        log.info("输入'#'使用默认数据库配置信息，输入其他退出程序:")
        select = input()
        if select != '#':
            exit(-1)
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        user = sys.argv[3]
        password = sys.argv[4]

    start = time.time()
    # 获取数据库连接
    connection = get_db_connection(host, port, user, password)
    cursor = connection.cursor()

    # 初始化数据库
    init_db()
    log.info("【数据库初始化完成，开始爬取投顾策略信息】")

    # 统计基本数据缺失的投顾策略
    skip_count = 0
    # 统计成功入库的投顾策略
    parse_count = 0
    # 投顾品牌id列表
    partnerIdList = get_partner_id_list()
    # 基本信息的列表
    basic_item_list = list()
    # 区间收益信息的列表
    interval_profit_list = list()
    # 持仓分布信息的列表
    hold_warehouse_list = list()
    # 调仓历史记录的列表
    adjust_warehouse_list = list()
    # 调仓详情的列表
    adjust_detail_list = list()
    for partnerId in partnerIdList:
        # 所有投顾策略的代码集合
        strategyIdSet = get_strategy_id_set(partnerId)
        baseInfo = get_base_info(partnerId)
        for strategyId in strategyIdSet:
            get_all_info(strategyId, baseInfo)
        parse_count += len(strategyIdSet)

    # 数据入库
    save_to_db()
    connection.close()
    log.info("【爬取完毕】：成功爬取" + str(parse_count) + "条投顾策略")
    log.warning("其中" + str(skip_count) + "条投顾策略的基本数据为空，无法解析")
    log.info("共计爬取" + str(parse_count + skip_count) + "条投顾策略")
    log.info("耗时：" + str(round(time.time() - start, 3)) + "秒。")
