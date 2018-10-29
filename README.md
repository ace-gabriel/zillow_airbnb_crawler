
# generate python file 
  protoc --proto_path=./ --python_out=../python_proto PropertyImageResults.proto

# decode raw protobuf 
  protoc --decode_raw < bulf_stream.bin

# decode protobuf with .proto file
  protoc --proto_path=./zillow_protobulf_processed --decode GetZRectResults.Results ./zillow_protobulf_processed/GetZRectResults.proto <./GetZRectResults2.bin


# 说明：
- zillow_upgrade/zillow为scrapy爬虫的主运行入口，也就是说cd都这个位置执行scrapy命令
- scrapy list 查看当前写好的爬虫列表， 目前有三个爬虫，有的是从网站搜索页中取数据，有的是从数据库中取数据填充price_histroy字段
- scrapy crawl xxx 启动某一个爬虫
- 日志文件在哪里？ zillow/logs/yyy.log
- 爬虫运行最好使用代理，代理配置文件：zillow/config.yml, 配置参数abuyun_proxy的proxyUser，proxyPass
  https://www.abuyun.com/ 你可以去这个网站注册购买一下，根据需要买个日套餐应该就够了 
- zillow_upgrade文件夹中除了zillow文件夹外，其他都是干什么的？ 因为我们爬的是app，需要做一些准备工作和测试工作呢。
- 爬回来的数据写到了那里？ 见配置文件zillow/config.yml，mongo_rooms参数，也就是说写到了mongo里边
