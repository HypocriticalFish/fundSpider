# Statements
This spider is used to crawl the data of investment strategy from the applet investment manager in the Tiantian Fund app of Dongfang Wealth. 

If no proxy is configured, frequent crawling may result in IP blocking.



# Environment

python 3.10.7+

mysql 5.7.40




# Directory structure
    │  Default_DB_Config.ini    // default database config
    │  Dockerfile               //docker file
    │  fundSpider.py			// core spider file
    │  init.bat					// initialize environment
    │  loggers.py				// log moduler
    │  ReadMe.md				// english documentation
    │  requirements.txt			// dependent packages
    │  start.bat				// start spider on windows
    │  start.sh				// start spider on Linux
    |  utils.py					// utils methods
    │  使用说明.txt				 // chinese documentation
    │  
    │
    ├─.idea			// auto generated					
    │     
    │      
    ├─fundData		// data directory
    │ 
    |
    │          
    ├─venv			
    │  │              
    │  └─Scripts	// virtual environment scripts
    │      
    │              
    └─__pycache__	// python cache files



# Instruction

```
To run the spider on windows, double click 'start.bat'.
The crawled data is saved into the database 'tt_fund'.
Log files could be found in the folder 'log'.
```



# Database structure

```
+--------------------------+
| Tables_in_tt_fund        |
+--------------------------+
| adjust_warehouse_detail  |
| adjust_warehouse_history |
| base_info                |
| day_profit               |
| hold_warehouse_info      |
| interval_profit          |
| strategy_pool            |
+--------------------------+
```



# Tables structure

```mysql
# 投顾策略基本信息表
CREATE TABLE `base_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾策略ID',
  `company_name` varchar(20) DEFAULT NULL COMMENT '公司名称',
  `brand` varchar(20) DEFAULT NULL COMMENT '投顾品牌',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `class` varchar(10) DEFAULT NULL COMMENT '类型',
  `create_date` date DEFAULT NULL COMMENT '成立日期',
  `risk_level` int DEFAULT NULL COMMENT '风险等级，1—5分别对应低风险、中低风险、中风险、中高风险、高风险',
  `basic_remark` varchar(200) DEFAULT NULL COMMENT '基准',
  `recommend_hold` varchar(10) DEFAULT NULL COMMENT '推荐持有时长',
  `feature` varchar(500) DEFAULT NULL COMMENT '特点',
  `concept` varchar(500) DEFAULT NULL COMMENT '策略理念',
  `min_buy` float DEFAULT NULL COMMENT '起投金额，单位元',
  `service_rate` float DEFAULT NULL COMMENT '服务费率',
  `strategy_rate_discount` float DEFAULT NULL COMMENT '产品申购费率折扣',
  `update_date` date NOT NULL COMMENT '日期',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id` (`update_date`,`strategy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 区间收益表
CREATE TABLE `interval_profit` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾策略ID',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `last_date` date DEFAULT NULL COMMENT '最新净值日',
  `week_profit` float DEFAULT NULL COMMENT '近1周涨跌幅',
  `week_bench` float DEFAULT NULL COMMENT '近1周基准涨跌幅',
  `month_profit` float DEFAULT NULL COMMENT '近1月涨跌幅',
  `month_bench` float DEFAULT NULL COMMENT '近1月基准涨跌幅',
  `thrmonth_profit` float DEFAULT NULL COMMENT '近3月涨跌幅',
  `thrmonth_bench` float DEFAULT NULL COMMENT '近3月基准涨跌幅',
  `halfyear_profit` float DEFAULT NULL COMMENT '近6月涨跌幅',
  `halfyear_bench` float DEFAULT NULL COMMENT '近6月基准涨跌幅',
  `year_profit` float DEFAULT NULL COMMENT '近1年涨跌幅',
  `year_bench` float DEFAULT NULL COMMENT '近1年基准涨跌幅',
  `twoyear_pforit` float DEFAULT NULL COMMENT '近2年涨跌幅',
  `twoyear_bench` float DEFAULT NULL COMMENT '近2年基准涨跌幅',
  `thryear_profit` float DEFAULT NULL COMMENT '近3年涨跌幅',
  `thryear_bench` float DEFAULT NULL COMMENT '近3年基准涨跌幅',
  `curyear_profit` float DEFAULT NULL COMMENT '今年涨跌幅',
  `curyear_bench` float DEFAULT NULL COMMENT '今年基准涨跌幅',
  `total_profit` float DEFAULT NULL COMMENT '成立以来涨跌幅',
  `total_bench` float DEFAULT NULL COMMENT '成立以来基准涨跌幅',
  `update_date` date NOT NULL COMMENT '日期',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id` (`update_date`,`strategy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 持仓信息表
CREATE TABLE `hold_warehouse_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾策略ID',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `date_` date DEFAULT NULL COMMENT '日期',
  `fund_code` varchar(10) DEFAULT NULL COMMENT '基金代码',
  `fund_name` varchar(30) DEFAULT NULL COMMENT '基金名称',
  `fund_type` varchar(10) DEFAULT NULL COMMENT '基金类型',
  `ratio` float DEFAULT NULL COMMENT '持仓比例',
  `update_date` date NOT NULL COMMENT '日期',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id_fcode` (`update_date`,`strategy_id`,`fund_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 调仓历史记录表
CREATE TABLE `adjust_warehouse_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾策略ID',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `date_` date DEFAULT NULL COMMENT '调仓日期',
  `reason` varchar(1000) DEFAULT NULL COMMENT '调仓原因',
  `update_date` date NOT NULL COMMENT '日期',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id_date` (`update_date`,`strategy_id`,`date_`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 调仓明细变动表
CREATE TABLE `adjust_warehouse_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾测策略ID',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `date_` date DEFAULT NULL COMMENT '调仓日期',
  `fund_code` varchar(10) DEFAULT NULL COMMENT '基金代码',
  `fund_name` varchar(30) DEFAULT NULL COMMENT '基金名称',
  `fund_type` varchar(10) DEFAULT NULL COMMENT '基金类型',
  `pre_ratio` float DEFAULT NULL COMMENT '调仓前持仓占比',
  `after_ratio` float DEFAULT NULL COMMENT '调仓后持仓占比',
  `update_date` date NOT NULL COMMENT '日期',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id_date_fcode` (`update_date`,`strategy_id`,`date_`,`fund_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 备选基金表
CREATE TABLE `strategy_pool` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾策略ID',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `fund_code` varchar(10) DEFAULT NULL COMMENT '基金代码',
  `fund_name` varchar(30) DEFAULT NULL COMMENT '基金名称',
  `fund_type` varchar(10) DEFAULT NULL COMMENT '基金类型',
  `update_date` date NOT NULL COMMENT '日期',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id_fcode` (`update_date`,`strategy_id`,`fund_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 日收益率表
CREATE TABLE `day_profit` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `strategy_id` varchar(10) DEFAULT NULL COMMENT '投顾策略ID',
  `strategy_name` varchar(20) DEFAULT NULL COMMENT '投顾策略名称',
  `date_` date DEFAULT NULL COMMENT '日期',
  `SE` float DEFAULT NULL COMMENT '组合涨跌幅',
  `BENCH_SE` float DEFAULT NULL COMMENT '基准涨跌幅',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '入库时间戳',
  PRIMARY KEY (`id`),
  KEY `index_udate_id_date` (`update_date`,`strategy_id`,`date_`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

