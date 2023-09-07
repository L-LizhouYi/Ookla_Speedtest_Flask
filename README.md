# Ookla Speedtest for Flask

## 介绍
> Ookla Speedtest（也称为Speedtest.net）是一个广受欢迎的网络测速工具，用于测量互联网连接的速度和性能。它由Ookla公司开发，是全球范围内最广泛使用的网络测速工具之一。
> 
> 1. 测量互联网速度： Speedtest允许用户快速、准确地测量其互联网连接的速度，包括下载速度、上传速度和延迟（ping时间）。这对于评估互联网服务提供商（ISP）提供的服务质量非常有用。
> 2. 用户友好的界面： Speedtest提供了一个简单直观的用户界面，用户只需点击“开始测试”按钮，工具会自动测量速度并显示结果。这种用户友好性使得任何人都可以轻松使用它，无需深入了解网络技术。
> 3. 全球测试服务器： Speedtest拥有遍布世界各地的测试服务器，用户可以选择最接近他们的服务器进行测试，以获得最准确的测速结果。这意味着无论你位于世界的哪个地方，都可以使用Speedtest来评估你的互联网连接速度。
> 4. 历史记录和图表： Speedtest还提供了测速历史记录和图表功能，用户可以跟踪他们的连接速度随时间的变化。这对于监控ISP提供的服务以及识别潜在问题非常有用。
> 5. 移动应用和网站版本： Speedtest提供了移动应用和网站版本，适用于各种平台，包括iOS、Android和Web浏览器。这使得用户可以在各种设备上进行测速测试。
> 6. 商业和家庭用户： Speedtest服务既适用于普通家庭用户，也适用于商业和企业用户。企业用户可以使用Speedtest进行网络性能测试，以确保其业务运行顺畅。
> 
> 总之，Ookla Speedtest是一个方便易用的工具，用于测量和监控互联网连接的速度和性能。它帮助用户评估他们的互联网服务提供商提供的服务质量，并提供有关网络性能的有用数据，以帮助解决潜在的连接问题。



## 效果图
![image.png](https://cdn.nlark.com/yuque/0/2023/png/28988047/1694080900878-605f352f-d86e-4f92-8c31-7345016c8c90.png#averageHue=%23fefefe&clientId=u26744b90-b7a7-4&from=paste&height=976&id=u6dfdff53&originHeight=976&originWidth=1789&originalType=binary&ratio=1&rotation=0&showTitle=false&size=73316&status=done&style=none&taskId=ua3cb5334-0ee2-4465-aebb-9cdc4050bb7&title=&width=1789)![image.png](https://cdn.nlark.com/yuque/0/2023/png/28988047/1694080937058-6c303b7e-9082-48e8-8cf4-f41093c74f0d.png#averageHue=%23b1a68f&clientId=u26744b90-b7a7-4&from=paste&height=980&id=uc47f6b3c&originHeight=980&originWidth=1432&originalType=binary&ratio=1&rotation=0&showTitle=false&size=203922&status=done&style=none&taskId=uffb52799-a93b-4d72-ad63-bedf6189f19&title=&width=1432)


## 部署

```bash
git clone https://github.com/L-LizhouYi/Ookla_Speedtest_Flask.git
python3 -m pip install -r requirements.txt
python3 mian.py
```


## Speedtest Server
[Speedtest 官方文档](https://support.ookla.com/hc/en-us/categories/204419868-Speedtest-Servers) 点开这个链接 照着说明安装即可，服务默认占用 8080 和 5060 这两个端口.<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/28988047/1694081715138-3657a621-f3bc-4a8c-b014-7652f3214240.png#averageHue=%23fefefd&clientId=u26744b90-b7a7-4&from=paste&height=956&id=ubf50a9ae&originHeight=956&originWidth=1433&originalType=binary&ratio=1&rotation=0&showTitle=false&size=57811&status=done&style=none&taskId=u78951512-26c0-44e8-ba2c-bcf0b073eae&title=&width=1433)把服务器添加到 speedtest_server.py 中的列表，重启前端，url 和 host 必填<br />有DNS的话可以配置域名，没有就直接写IP

## 常见错误

### 0x01 添加服务器后不显示
在内网部署的话有个痛点，Speedtest Server必须是https否则在测速服务器列表中不显示，解决办法有两个<br />第一个就是自签SSL，手动添加CA信任证书 这样做每个设备都需要添加，不太现实。<br />第二个办法就是，使用泛域名证书 配合DNS解析 (推荐)


## 写在最后
没啥好写的 Email liulang@eeho.cn 
