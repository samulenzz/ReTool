# _*_coding:utf-8_*_
import grpc
from Proto import Requirement_pb2, Requirement_pb2_grpc
import json


ReFilePath = { 'id' : 1, 'description' : ''' 1　范围
1.1　标识
a)	本文档是仿真想定监控工具项目需求分析阶段的需求规格说明文档，标识号：；
b)	标题：仿真想定监控工具项目软件需求规格说明；
c)	本文档适用的计算机软件配置项（CSCI）为仿真想定监控工具软件；
d)	本文档适用于仿真想定监控工具设计过程。
a)	装备模型：特指联合作战仿真(JTS)对平台、传感器、武器等硬件设备的模拟模型，在系统中以软件类的形式出现，如“半主动空空导弹模型”。
b)	认知模型：特指JTS中对人的决策、判断、评估行为的模拟模型，在系统中以软件类和名称字典的形式出现，如“对地攻击认知模型”。
c)	设备：使用装备模型装订参数后，形成的具备特定型号背景的模型实例，如“AIM－120C”。
d)	行为模型：一系列认知模型的组合，形成具备某类型作战能力的综合模型，如“对空作战”。
e)	作战单元：对应平台型号，是搭载了特定设备和行为模型的实体模版，如“054A”
f)	兵力：由作战单元生成，对应现实的平台级实体，如“112舰”。
g)	固定设施：地理位置固定，具备特定的几何特征和行为能力，能和实体进行交互的设施，如“桃园机场”、“基隆港”。
h)	编队：特指舰艇编队，由舰艇类兵力组成，具有队形属性，如“第二反潜群”。
i)	中队：特指飞机编队，属性包含飞机型号和数量，可以为中队内成员分别指定任务,如“舰载攻击机第1中队”。
j)	任务：赋予某兵力的作战使命，由使用兵力、事件序列等要素组成，如“对海突击”。
k)	事件：从属于某任务，是某特定兵力执行的有明确目的的行动，如“攻击XX目标”。

仿真想定监控工具是一套完整的支持仿真想定制作、仿真模型管理、仿真运行及作战效能评估的工具，为开展XXX舰艇平台防空反导技术研究和实验验证工作提供技术和仿真手段支撑。本项目目标是基于Flames仿真平台和现有仿真模型库及效能评估算法，开发一个仿真想定监控工具，以方便用户使用，提供想定剧情的制作与管理，仿真过程的可视化监控，并集成效能评估算法，实现评估结果的可视化。
本文档是“仿真想定监控工具”项目的软件系统需求的分析和总结，以作为设计的依据。
本文档主要描述了上述软件的功能需求、非功能性要求、质量属性、约束、接口要求等内容。
2　引用文档
a)	《想定监控工具技术任务书》
仿真想定监控工具可分为仿真模型库的管理，想定剧情的编辑与生成，作战仿真过程，运行监视，作战效能评估与展示五个部分。
本项目通过改造现有仿真模型库实现对仿真模型的管理，支持想定剧情的编辑与生成；基于Flames仿真平台对想定剧情仿真过程的支撑，完成对仿真过程的可视化、仿真过程的控制、以及兵力干预；在仿真结束后，通过调用已有的效能评估模型完成对作战过程的仲裁以及仲裁结果的可视化展示。
3.1.2　系统语境图
为界定系统边境，本小节给出了系统语境图，如图 1示，与仿真想定监控工具交互的外部工具包括集成设计平台，仿真模型库，FLAMES仿真引擎和FLAMES数据库。集成设计平台负责对仿真想定监控工具各子工具的调度；仿真想定监控工具从仿真模型库中读取作战单元信息来编辑想定剧情；在想定剧情编辑完毕后，仿真想定监控工具负责想定生成，将想定剧情的模型信息写至FLAMES仿真数据库中以支持仿真过程；仿真想定监控工具调度仿真引擎控制仿真过程，在仿真过程中调用仿真引擎接口控制兵力要素；仿真过程中FLAMES仿真引擎将仿真过程数据返回仿真想定监控工具以支持仿真想定监控工具的实时监视和监控功能以及仿真结束以后的数据分析和效能评估。 效能评估完成以后向集成设计平台发送消息，通过集成设计平台可以调度展示效能评估结果。

图 1 系统语境图
3.1.3　用例图
在本小节中给出仿真想定监控工具项目软件需求的用例模型，该模型中用例类型属于系统用例。为避免图例过于复杂，只在总图中描述出一二级用例，进一步的用例分解可参看各节详细说明。

图 2 仿真想定监控工具系统用例图
3.1.4　业务流程图
图3给出了仿真想定监控工具的整体工作流程：
1.	仿真模型管理人员通过集成设计平台管理仿真模型库，并向集成设计平台推送模型相关信息；
2.	想定制作人员在仿真模型库的基础上设置想定剧情，设置完成后可以进行想定推演；调用仿真引擎，在仿真过程中可以控制仿真进度以及干预兵力；
3.	在仿真运行过程中，仿真运行监视人员利用仿真过程数据，以二维/三维的形式展示态势发展，控制仿真进度以及兵力要素，同时监视作战流程；
4.	仿真完成后，仿真数据分析人员可以利用仿真过程数据做数据分析并展示分析结果，同时可以基于仿真过程数据调用效能评估函数实现对作战过程的仲裁以及仲裁结果的展示；

图3　仿真想定监控工具总流程图
3.2　接口需求
 图 4仿真想定监控工具接口示意图
仿真想定监控工具的内外部接口如图4示，其中外部系统包括集成设计平台、仿真引擎和效能评估模型；外部接口包括集成设计平台对想定生成客户端的调用接口、集成设计平台对仿真模型库的调用接口、仿真模型库对集成设计平台推送知识的接口、集成设计平台对效能评估工具客户端的调用接口、集成设计平台对想定监视工具的调用接口、想定生成服务端对仿真引擎的调用接口、效能评估工具服务端对效能评估模型的调用接口、效能评估工具服务端向集成设计平台发送效能评估完毕的消息接口；内部接口包括想定生成客户端与想定生成服务端的想定配置信息传输接口、想定生成工具服务端向想定生成工具客户端推送仿真过程数据的接口、效能评估工具客户端对效能评估工具服务端的调用接口，想定生成服务端向想定监视工具推送仿真过程数据的接口。
3.2.1　外部接口要求
仿真想定监控工具的外部接口包括与集成设计平台、与仿真引擎以及与效能评估模型之间的接口，详细信息如表 1示。
表 1 仿真想定监控工具外部接口信息统计表
接口标识	信息流向	接口类型	接口功能说明
I/F-JCPT-FZMXK	集成设计平台→仿真模型库	软件接口	集成设计平台
对仿真模型库的调用
	仿真模型库→集成设计平台	软件接口	仿真模型库向集成设计平台推送模型知识
I/F-JCPT-XDKU	集成设计平台→想定生成客户端	软件接口	集成设计平台对想定生成客户端的调用
I/F-JCPT-XNPGC	集成设计平台
→效能评估工具客户端	软件接口	集成设计平台对效能评估工具客户端的调用
I/F-JCPT-XDJS	集成设计平台→想定监视工具	软件接口	集成设计平台对运行监视工具的调用
I/F-XDSCS-FZYQ	想定生成服务端→JTS仿真引擎	软件接口	想定生成服务端对JTS仿真引擎的调用及控制
I/F-XNPGS-PGMX	效能评估工具服务端
→效能评估模型	软件接口	效能评估工具服务端对效能评估模型的调用
I/F-XNPGS-JCPT	效能评估工具服务端
→集成设计平台	软件接口	效能评估工具服务端向集成设计平台发送评估完毕的消息
3.2.2　内部接口要求
仿真想定监控工具的内部接口主要包括想定生成客户端与想定生成服务端之间，想定生成服务端与运行监视工具之间，想定生成服务端与效能评估工具服务端，效能评估工具客户端与效能评估工具服务端之间，想定生成服务端与模型库之间的接口，详细信息见表 2所示。
表 2 仿真想定监控工具内部接口信息统计表
接口标识	信息流向	接口类型	接口功能说明
I/F-XDSCC-XDSCS	想定生成工具客户端
→想定生成工具服务器	软件接口	传输想定剧情信息
I/F-XDSCS-XDSCC	想定生成工具服务端
→想定生成工具客户端	软件接口	传输仿真过程数据
I/F-XNPGC-XNPGS	效能评估工具客户端
→效能评估工具服务端	软件接口	效能评估工具客户端
对服务端的调用
I/F-MXK-XDSCS	仿真模型库
→想定生成工具服务端	软件接口	想定生成工具服务端从模型库中读取模型信息
I/F-XDSCS-XDJS	想定生成工具服务端
→想定监视工具	软件接口	想定生成工具服务端将仿真过程数据推送给想定监视工具
3.3　功能需求
按照项目的功能划分，本节详细介绍想定剧情制作，仿真想定监控，仿真运行监视以及作战效能评估几个部分。
3.3.1　想定生成工具
3.3.1.1　想定剧情制作
想定剧情的制作包括战场环境的设置，固定设施的设置，参战兵力的设置，初始态势的设置，指挥关系的设置，通信网络的设置，任务的设置以及完成想定剧情设置后的想定预推演功能。

图 5设定想定剧情用例图
表3　设定想定剧情用例描述表
用例名称：设定想定剧情
用例编号：
最近一次修改者： 	时间：
主参与者	想定制作人员
功能描述	用户设置想定要素，包括战场环境设置、固定设施设定、设置参战兵力、编队编成、设置初始态势、设置通信网络、指挥关系、设置任务
前置条件	具备可用的作战单元
后置条件	设定好的想定剧情已存储
触发条件	用户选择设定想定剧情功能
优先级	高
主成功场景	1.	用户设置自然环境
2.	用户设置固定设施
3.	用户设置参战兵力；
4.	用户设置编队编成，进行编队成员管理和队形管理
5.	用户设置任务，规划实体和编队的航路
6.	用户在海图上部署兵力
7.	用户设置指挥关系
8.	用户设置通信网络
9.	用户设置初始态势
10.	用户结束想定设定
11.	存储想定
12.	想定推演
子流程	1	设置战场环境,参见3.3.2.1
2	设置固定设施,参见3.3.2.2
3	设置参战兵力,参见3.3.2.3
4	编队成员设置和队形设置,参见3.3.2.4.1和3.3.2.4.2
5	设置任务,参见3.3.2.8
6	部署兵力,参见3.3.2.5.1
7	规划航路,参见3.3.2.5.2
8   设置指挥关系，参见3.3.2.6
9   设置通信网络, 参见3.3.2.7
3.3.1.2　设置战场环境
表4　设置战场环境用例描述表
用例名称：设置战场环境
用例编号：
参与者（角色）	想定制作人员
功能描述	通过选择海图，卫星图片等设置战场环境
后置条件	用户设置完成战场环境
优先级	中
主成功场景	1.	用户选择战场环境设置功能
2.	用户选择海图文件，卫星图片文件
3.	系统存储设定的战场环境信息
输入信息	海图，卫星图片
输出信息	当前用户设置的战场环境信息
3.3.1.3　设置固定设施
表5　设置固定设施用例描述表
用例名称：设置固定设施
用例编号：
最近一次修改者： 	时间：
参与者（角色）	想定制作人员
功能描述	对固定设施如机场、港口进行添加和编辑
后置条件	设置固定设施信息
优先级	中
主成功场景	1.	用户选择添加机场或港口
2.	设定机场或港口名称
3.	设定机场或港口参数，包括机场跑道数据，机场停机坪数据以及机场设备数
4.	保存机场或港口设定
输入信息	机场或港口参数
输出信息	保存机场或港口设定
非功能需求	设定机场或港口数据使用图形化操作
待解决的问题	机场的位置指定使用兵力部署部分功能，港口参数影响兵力部署

图6　设置固定设施用例活动图

图 7 机场添加界面图
3.3.1.4　设置参战兵力
表6　设置参战兵力用例描述表
用例名称：设置参战兵力
用例编号：
最近一次修改者：	时间：
参与者（角色）	仿真想定制作人员
功能描述	添加和删除使用的兵力
前置条件	完成配置后的作战单元
后置条件	提供了部署和编队的来源
优先级	高
主成功场景	1.	用户选择设置兵力功能
2.	系统读取作战单元库
3.	用户选择作战单元，添加到某方
4.	用户对某方兵力进行编辑
5.	系统保存兵力设定
扩展流程	4.a选中某兵力，删除
4.b 选择某兵力，重命名
子流程	3.a用户输入兵力数量
3.a.1用户通过兵力设置界面输入兵力数
3.a.2系统根据作战单元的信息，确定兵力的图标和显示
3.a.3生成输入个数的兵力
输入信息	作战单元
输出信息	可选的兵力
非功能需求	树状显示兵力

图8　设置参战兵力用例活动图

图 9 参战兵力设置界面
3.3.1.5　设置编队编成
3.3.1.5.1　设置编队成员
表7　设置编队成员用例描述表
用例名称：管理编队成员
用例编号：
最近一次修改者： 	时间：
参与者（角色）	想定制作人员
功能描述	可以组织编队，加入、移除编队成员，为编队重命名
前置条件	完成兵力设置
后置条件	可以对编队进行相关设置
优先级	高
主成功场景	1.	用户选择管理编队成员功能
2.	系统显示兵力树
3.	用户添加编队
4.	用户从兵力树中选择兵力放在编队下
5.	用户编辑编队
6.	用户结束管理编队成员
7.	保存编队成员设置
扩展流程	5.a删除编队成员
5.a.1检查是否已安排了队形位置
5.a.1.a安排了，则提示是否删除
5.a.1.a.a 确认，到5.a.1.b
5.a.1.a.a 取消，到5
5.a.1.b删除此成员在编队中的信息

5.b删除编队
5.b.1编队是否已部署
5.b.1.a已部署，给出提示
5.b.1.a.a确认，到6.b.1.b
5.b.1.a.b 取消，到6
5.b.1.b 删除编队

5.c重命名编队
输入信息	编队成员
输出信息	编队成员集合
非功能需求	树状显示

图10　管理编队成员用例活动图
3.3.1.5.2　设置编队队形
表8　设置编队队形用例描述表
用例名称：设置编队队形
用例编号：
最近一次修改者： 	时间：
参与者（角色）	想定制作人员
功能描述	为实际编队指定队形模板，通过拖拽操作为每个实体指定编队中所在的位置，并可以调整；或者按照队形模板自动生成编队，不可调整
指定编队指挥舰（机）
前置条件	完成管理编队成员
后置条件	编队具有了队形，可以完成编队部署
优先级	高
主成功场景	1.	用户选择编队进行队形设置
2.	系统读取编队成员、队形模板信息
3.	系统显示编队组成、编队队形界面
4.	用户选择队形模板
5.	设置编队队形
6.	保存编队队形设置
扩展流程	4.a 用户选择编辑模板，参见用例3.3.2.4.3

5.a 用户拖动完成编队队形设置
5.a.1参考队形模板，用户拖动完成编队队形设置
5.a.2设置完毕，检查是否设置指挥舰

5.b 用户输入完成编队队形设置
5.b.1 用户指定指挥舰（机）
5.b.2按照队形模板，系统自动生成编队队形设置
业务规则	队形模板参照海军作战条令设定

图11　管理编队队形用例活动图

图 12 航船编队队形设置界面
3.3.1.5.3　管理队形模板
表9　管理队形模版用例描述表
用例名称：管理队形模板
用例编号：
参与者（角色）	想定制作人员
功能描述	基于图形化操作新建、编辑编队队形，包括舰艇和飞机编队的队形，这里编辑的是队形模板。
后置条件	设定了队形模板
优先级	高
主成功场景	1.	用户选择设定队形模板功能
2.	系统读取已有队形模板信息，显示队形管理界面
3.	用户新建队形模板
4.	用户通过拖拽各位置或输入角度和距离进行设定
5.	系统更新队形编辑视图
6.	用户结束队形模板编辑
7.	系统保存设定的队形模板
扩展流程	3.a 用户删除队形模板
3.b 用户修改已有队形模版

4.a 用户通过输入指定队形模板
4.a.1 用户输入指定队形模板中的指挥位置
4.a.2 用户通过弹出框输入队形中成员到指挥位置的角度与距离
非功能需求	图形化显示编队队形，以拖动或手动输入角度和距离的方式编辑队形

图13　管理队形模版用例活动图

图 14 队形模板管理界面
3.3.1.6　设置初始态势
初始态势的设置包括部署兵力和路径规划两部分。其中部署兵力主要是将兵力布置于战场环境中，而路径规划则是对作战双方中兵力的路径进行设置，主要包括路径点位置的规划以及路径点到达时间的规划。
3.3.1.6.1　部署兵力
表10　部署兵力用例描述表
用例名称：部署兵力
用例编号：
参与者（角色）	想定制作人员
功能描述	通过在兵力树上拖放兵力到态势图上的方式，设置红蓝方兵力初始位置，并指定初始方向。设置完成后，以二维形式展示设置效果。
前置条件	1.	完成设置的兵力
2.	完成设置的编队
后置条件	兵力和编队被部署到地图上
优先级	高
主成功场景	1.	用户选择兵力部署功能
2.	系统显示兵力树和态势图
3.	用户从作战编队中选择兵力，拖动兵力到态势图上
4.	用户选择已部署的兵力
5.	通过拖动或输入位置来修改部署位置
6.	用户停止兵力部署
7.	系统保存所做的兵力部署情况
扩展流程	*.a可以取消拖动的兵力或编队

3.a选择编队
3.a.1编队是否已完成队形设置
3.a.1.a没有，则提示
3.a.1.b完成，拖动兵力到态势图上
3.a.2放置编队
3.a.3系统以放置位置为中心计算各成员位置
3.a.4显示编队各成员位置

3.b 输入兵力数量
3.b.1 用户将兵力拖动到态势图上，双击鼠标，弹出兵力数量对话框，用户可以增、减以及输入兵力数量
3.b.2 系统根据用户输入的兵力数量，显示对应的兵力在态势图上

5.a 拖动编队
5.a.1 拖动编队重新放置
5.a.2 系统以放置位置为中心计算各成员位置
5.a.3 系统显示编队各成员位置
5.b 输入编队位置
5.b.1 输入编队位置
5.b.2 以输入位置为指挥位置计算各成员位置
5.b.3 显示编队各成员位置

5.b.1.a用户选择输入绝对位置或相对某一实体的位置
5.b.1.a.1 相对某实体的位置输入
5.b.1.a.1.a 用户选择参考实体
5.b.1.a.1.b 用户输入相对参考实体的方向，距离，高度信息

6.a  用户继续操作，回到2
输入信息	兵力或编队的位置信息
输出信息	兵力或编队的位置
非功能需求	拖动和输入两种方式部署

图15　部署兵力总用例活动图

图 16 兵力部署之位置设置活动图

图 17 兵力部署界面

图 18输入兵力位置对话框
3.3.1.6.2　规划路径
表11　规划路径用例描述表
用例名称：规划路径
用例编号：
参与者（角色）	想定制作人员
功能描述	通过在海图上选取航路点的方式为实体和编队规划航路，可以设定航路点的速度、时间等参量，支持为航路点命名。规划完成后，支持切换到三维视图，观察路径规划结果。
前置条件	待规划兵力已部署
后置条件	兵力和编队设置了仿真运行时的初始行动路线
优先级	高
主成功场景	1.	用户从地图上选择实体或编队
2.	系统读取实体或编队的路径信息
3.	用户添加新的路径点
4.	系统在海图上更新路径显示
5.	用户选择完成路径规划
6.	系统计算路径起点和第二点的方向，作为实体/编队的初始航向
7.	系统计算路径各点时间，在海图上显示
8.	保存所规划的路径
扩展流程	3.a修改路径点
3.a.1.a.1拖动点
3.a.1.a.2放置点
3.a.1.b输入点的位置和速度
3.a.2 在海图上显示新点 ，转到4

3.b.删除路径点，完成转到4

3.c插入点
3.c.1 用户在已有路径上选择插入
3.c.2系统计算一个在选中点位置的点
3.c.3在海图上显示新点 ，转到4

3.d命名此路径点名称,转到4

3.e 路径高度视图设定
3.e.1 用户选择高度视图设置
3.e.2 用户通过在竖直方向上拖拽路径点来改变高度
3.e.3 系统更新高度视图
3.e.4 用户结束高度视图操作，回到4

5.a 待用户结束某实体的路径规划时，系统弹出对话框，确认是否形成闭合回路
5.a.1 是，系统自动连接最后点与起始点
5.a.2 否
5.b 继续规划，返回3
子流程	3 添加路径点
3.1 用户在地图上点击
3.2 系统计算点击位置，作为路径点
3.3 在海图上显示新点 ，转到4

4系统推算路径各点时间
4.1读取仿真开始时间
4.2计算各点时间
4.3在海图上显示各点时间
输入信息	兵力或编队的路径信息
输出信息	兵力或编队的路径，兵力或编队的初始方向
非功能需求	以拖动的方式设置点的位置

图19　规划路径用例活动图

3.3.1.7　设置指挥关系
表12　设置指挥关系用例描述表
用例名称：设置指挥关系
用例编号：
参与者（角色）	想定制作人员
功能描述	通过图形化的操作来设置多级指挥关系（树型或网型），设置完成后可以在海图上和单独的界面上显示
前置条件	完成了兵力部署
后置条件	确定实体间的指挥关系
优先级	中
主成功场景	1.	用户选择设置指挥关系功能
2.	系统以树状视图显示部署的全部兵力，在指挥关系视图中显示当前的指挥关系拓扑
3.	用户拖动兵力到指挥关系视图中，在指挥关系视图上设置指挥关系
4.	用户停止指挥关系设定
5.	系统保存设定的指挥关系
输入信息	兵力信息
输出信息	兵力间指挥关系
非功能需求	用图形化的方式显示树形或网型指挥关系

图20　设置指挥关系用例活动图
3.3.1.8　设置通信网络
表13　设置通信网络用例描述表
用例名称：设置通信网络
用例编号：
参与者（角色）	想定制作人员
功能描述	1.	通过图形化的操作来设置通信网络拓扑关系和设定通信参数，设置完成后可以在海图上显示各信道连接和在单独的界面上显示通信拓扑图。
2.	要能设定不同的信道类型、组网节点、信道参数，设定的结果自动反映到通信模型中去
前置条件	完成兵力部署
后置条件	确定了兵力间的通信关系，
优先级	中
主成功场景	1.	系统读取实体的通信设备的类型和数量，并在界面显示
2.	用户选择网络拓扑结构类型
3.	用户设置通信设备和网络的对应关系
4.	系统更新拓扑图显示和在海图上显示信道
5.	用户完成通信设置
6.	系统保存通信设定
扩展流程	5.a 用户继续设置通信网络，回到1
输入信息	实体信息
输出信息	实体间的通信关系
非功能需求	用图形化的方式显示通信拓扑图


图 21通信网络设置界面

图22　设置通信网络用例活动图
3.3.1.9　设置任务
表14　设置任务用例描述表
用例名称：设置任务
用例编号：
参与者（角色）	想定制作人员
功能描述	可以为编队、飞机中队、单个实体设置任务。任务可以在仿真开始前或开始后设置。
目前设定各方（红蓝）以下任务
1)	空中兵力弹药配置使命
2)	警戒使命
3)	远程打击使命
4)	护航使命
5)	巡逻使命
6)	空中电子战使命
7)	海上巡逻使命
8)	执勤使命
如果红蓝双方在仿真过程中从外部设置任务，需要能动态加载执行
前置条件	完成兵力部署
后置条件	仿真中任务设置完成
优先级	高
主成功场景	1.	选择任务规划
2.	显示任务列表及序列
3.	选择添加任务
4.	设置任务名称
5.	设置任务开始结束时间
6.	选择执行的一个或多个实体
7.	选择任务执行事件及序列
8.	添加此任务
9.	选择编辑任务
10.	任务设置完毕后，可选择任务组合性能分析
11.	保存任务的设置
扩展流程	9.a 编辑任务
9.a.1 任务重命名
9.a.2 修改任务的执行的顺序
9.a.3 修改任务的起始时间
9.a.4 修改任务的执行实体
9.a.4.1 修改任务执行实体的个数
9.a.4.2 修改任务执行实体的配置
9.a.5 编辑任务事件
9.b 删除任务
10.a 总的起止时间
10.b 涉及兵力
子流程	5若飞机需要挂载，设置挂载方案，见3.3.2.8.1
9.编辑任务事件，见3.3.2.8.2
输入信息	实体信息
输出信息	兵力被赋予了任务
待解决的问题	任务甘特图，
 图23　设置任务用例活动图

图 24 任务设置界面
3.3.1.9.1　设置挂载方案
表15　设置挂载方案用例描述表
用例名称：设置挂载方案
用例编号：
参与者（角色）	想定制作人员
功能描述	可以为飞机设置挂载方案，设置好的方案可以保存
前置条件	选择了飞机执行任务
后置条件	为飞机选择了挂载方案
优先级	中
主成功场景	1.	用户选择飞机型号
2.	系统显示飞机正视图（从机首），及可用挂架
3.	系统显示可挂载的武器、干扰机
4.	用户将挂载物拖上挂架
5.	系统验证挂载物与飞机型号匹配
6.	用户为挂载方案命名，并选择保存
7.	系统保存挂载方案
扩展流程1
（步骤5）	1.	系统验证挂载物与飞机型号不匹配
2.	系统给出不匹配提示
3.	返回步骤3
扩展流程2（步骤7）	1.	用户不选择保存按钮
2.	系统不保存挂载方案
3.	返回步骤3
业务规则	系统显示可用武器时，只出现能在空中发射的
输入信息	飞机信息
输出信息	飞机配备挂载
待解决的问题	挂载物是否包括副油箱

图 25 设置挂载方案用例活动图

图 26 挂载方案设置界面
3.3.1.9.2　编辑任务事件
表16　编辑任务事件用例描述表
用例名称：编辑任务事件
用例编号：
参与者（角色）	想定制作人员
功能描述	对任务中各事件进行编辑
前置条件	对应任务已创建
后置条件	为任务设置了事件
优先级	高
主成功场景	1.	用户选择任务类型
2.	用户在对应可用事件列表中选择事件
3.	用户将事件添加到任务序列中
4.	用户通过地图操作等编辑事件属性
5.	系统更新任务序列表和任务视图
6.	用户停止添加事件
7.	系统计算各事件预计执行时间
8.	用户调整事件次序
9.	用户停止编辑任务事件
扩展流程	6.a 用户继续添加事件，回到2
9.a 用户继续编辑任务事件，回到5

图27　编辑任务事件用例活动图
3.3.1.10　想定文件生成
将设置完成的想定剧情信息存储为MSDL格式的想定文件。
表 17 想定文件生成用例表
用例名称：想定文件生成
用例编号：
最近一次修改者： 	时间：
参与者（角色）	想定制作人员
功能描述	想定剧情设置完成以后，将想定剧情信息存储到文件中
前置条件	想定剧情设置完成
后置条件	想定文件生成
优先级	中
主成功场景	1.	用户从想定生成工具客户端选择想定文件生成功能
2.	想定生成工具客户端读取想定剧情信息
3.	想定文件保存
输入信息	无
输出信息	MSDL格式的想定文件
3.3.1.11　想定推演
这里想定推演是指在仿真引擎不启动的情况下，对各实体运行轨迹的静态分析，包括将实体的运行轨迹展示在海图上，并且计算任务的时间偏差。
表 18想定推演用例表
用例名称：想定推演
用例编号：
最近一次修改者： 	时间：
参与者（角色）	想定制作人员
功能描述	想定剧情设置完成以后，根据设置的参数，做仿真前预推演
前置条件	想定剧情设置完成
后置条件	根据路径规划及时间参数，完成推演
优先级	高
主成功场景	4.	用户从想定生成工具客户端选择剧情推演功能
5.	想定生成工具客户端读取各实体的轨迹信息，展示于海图上
6.	想定生成工具客户端计算实体执行各任务的时间与预设时间的偏差
7.	用户将鼠标置于海图中实体某位置时，显示分析的时间偏差结果
输入信息	兵力的路径规划参数
输出信息	海图上展示各实体路径轨迹，及实体执行任务的时间偏差
3.3.1.12　仿真想定监控
表19　仿真想定监控用例描述表
用例名称：仿真想定监控用例
用例编号：
主参与者（角色）	仿真想定制作人员
其它参与者、相邻系统	JTS仿真引擎，集成设计平台
功能描述	在仿真引擎仿真作战态势的过程中，从想定生成工具客户端可以监视作战态势。监视可以从作战双方的视角，以及白方视角进行。在监视过程中，用户可以干预兵力行为，以及控制仿真过程。
前置条件	仿真引擎仿真作战过程
后置条件	按照用户的设置，想定生成工具客户端从红方视角，蓝方视角或白方视角以二维的形式展示作战态势
优先级	高
主成功场景	1.	想定生成工具客户端从仿真引擎实时获取仿真过程数据
2.	根据用户选择的监控视角，将态势数据显示于二维海图上
3.	监视过程中，用户可以进行仿真过程控制
4.	监控过程中，用户可以进行干预兵力行为
子流程	3.1仿真想定控制，见3.3.3.1用例“仿真过程控制”
4.1干预兵力行为，见3.3.3.2用例“干预兵力行为”
输入信息	海图信息，作战仿真过程数据
输出信息	想定监控

图 28 仿真想定监控用例活动图
3.3.1.13　仿真过程控制
表 20 仿真想定控制用例描述表
用例名称：仿真过程控制
用例编号：
最近一次修改者： 	时间：
主参与者（角色）	想定制作人员
其它参与者、相邻系统
功能描述	想定制作人员在监视态势运行的过程中，可以控制仿真过程，包括加速，减速，暂停，停止，恢复
前置条件	想定设置完毕，仿真运行中
后置条件	想定制作人员控制仿真进度
优先级	高
主成功场景	1.	想定制作人员监视态势运行
2.	想定制作人员控制仿真过程
3.	JTS仿真引擎响应仿真操作
4.	二维态势监视界面响应仿真控制操作
扩展流程	2.a 控制内容包括加速，减速，暂停，停止，恢复
输入信息	仿真控制操作
输出信息	相应的仿真进度
3.3.1.14　干预兵力行为
表 21 干预兵力行为用例描述表
用例名称：干预兵力行为
用例编号：
最近一次修改者： 	时间：
主参与者（角色）	想定制作人员
其它参与者、相邻系统	JTS仿真引擎
功能描述	想定制作人员在监视态势运行中，干预兵力行动，控制兵力要素，包括实体运动参数，传感器控制参数，武器发射参数，实体消亡，新实体的添加
前置条件	想定设置完毕，仿真运行中
后置条件	修改后的兵力设置
优先级	高
主成功场景	1.	想定制作人员监视二维态势发展
2.	想定制作人员修改兵力要素
3.	想定生成服务端调用仿真引擎接口，改变本次仿真剧情
4.	Flames仿真引擎继续仿真过程
5.	仿真过程数据传入仿真想定监控工具，展示态势界面
扩展流程	无
输入信息	原始兵力参数
输出信息	修改后的兵力参数

图 29 干预兵力行为用例活动图
3.3.2　作战效能评估
作战效能评估主要包括数据筛选及分析、效能评估及展示、评估模型管理三个主要功能。数据筛选及分析功能是对仿真结果数据进行筛选，并对筛选后的数据进行初步分析如轨迹方差分析等；效能评估及展示功能是调用效能评估模型对仿真剧情的仿真数据进行评估、展示及保存效能评估结果，评估模型管理功能是对效能评估模型的扩展功能，允许仿真评估人员能够导入新的评估模型。

图 30作战效能评估用例图
3.3.2.1　数据筛选及分析
仿真评估人员通过界面给出的过滤条件进行数据的筛选，筛选的条件包括时间段、实体号（实体名称）、关键字段比较（可以进行的操作可以为 >,<,=,!=）。然后对筛选后的数据进行典型分析，包括实体轨迹方差分析、态势信息处理精读分析、信息响应时间统计、信息更新率，并把分析结果展示给用户。
表 22数据筛选用例描述表
用例名称：数据筛选
用例编号：
编写者：李艳	时间：2013-01-22
最近一次修改者： 	时间：
主参与者	仿真评估人员（以下简称用户）
其他参与者、相邻系统	集成设计平台
功能描述	用户通过作战效能评估客户端界面输入想定剧情名称、设置筛选条件，由客户端把设置好的信息传送给作战效能评估服务端，服务端从本地数据库读取满足条件的实体，传递给作战效能评估客户端，客户端显示实体列表的信息。用户从实体列表中选择实体，由服务端对实体分析，并把分析结果保存到本地数据库并传递给客户端显示在界面上。
前置条件	用户选择数据筛选及分析功能
后置条件	用户选择实体及分析类型
触发条件	保存分析结果，并在作战效能评估客户端显示
优先级	中
主成功场景	1.	用户输入待分析的想定剧情和输入筛选条件
2.	作战效能评估客户端将筛选条件发送给效能评估服务端
3.	作战效能评估服务端从本地数据库获取满足条件的实体
4.	作战效能评估服务端把实体数据发送给客户端，由其显示实体列表
5.	用户选择实体及分析的类型
6.	作战效能评估客户端把分析的类型传递给服务端
7.	作战效能评估服务端对实体进行所选择的分析
8.	服务端把分析结果保存到本地数据库
9.	服务端把分析结果传递给给客户端由其显示。
输入信息	想定剧情（从界面），分析类型（从界面）
输出信息	分析结果数据（到界面，到数据库）
异常处理情况	从本地数据库读取信息失败，给出提示


图 31数据筛选及分析活动图

图 32数据筛选界面

图 33 数据分析界面

图 34 数据分析结果界面
3.3.2.2　效能评估及展示
本用例从仿真模型库调用作战效能评估模型对想定剧情进行效能评估，保存并展示评估结果。
表 23 调用作战效能评估模型评估用例描述表
用例名称：作战效能评估及展示
用例编号：
编写者：李艳	时间：2012-10-17
最近一次修改者： 	时间：
主参与者	仿真评估人员（以下简称用户）
其他参与者、相邻系统	集成设计平台、模型库
功能描述	用户通过效能评估客户端输入想查看评估结果的想定剧情，服务端从本地数据库查找，若未评估则调用评估模型进行评估，把评估结果保存到本地数据库并向集成设计平台发生评估完成消息，若已评估则从本地数据库读取评估结果传递给客户端，客户端收到后显示评估结果。
前置条件	存在输入的想定剧情
后置条件	作战效能评估结果已存储
触发条件	用户选择效能评估功能
优先级	中
主成功场景	1.	用户输入想定剧情
2.	作战效能评估服务端判断该剧情是否已存在评估结果，若已评估则转向6
3.	从数据库中读取选择的评估模型
4.	调用模型库效能评估模型进行效能评估（要根据评估模型库的调用形式来具体）
5.	把评估结果存储到本地数据库,并向集成设计平台发送评估完成消息。
6.	作战效能评估服务端把效能评估结果传给作战效能客户端进行展示。
输入信息	效能评估算法（从模型库）
输出信息	效能评估结果（到界面、到本地数据库）
异常处理情况	从模型库读取信息失败，给出提示

图 35 效能评估及展示活动图

图 36 效能评估及展示界面
3.3.2.3　评估模型管理
表 24评估模型管理用例描述表
用例名称：评估模型管理
用例编号：
编写者：李艳	时间：2013-01-22
主参与者	仿真评估人员（以下简称用户）
功能描述	用户可以修改已有的评估模型信息，或者删除评估模型信息，或者添加：用户通过效能评估客户端导入新的评估模型文件，并输入该模型的参数描述，并把模型文件数据和参数描述传递给服务端，服务端负责把模型文件保存到本地，并把模型的信息保存到本地数据库。
前置条件	用户选择评估模型管理功能
后置条件	保存编辑、修改或者插入的评估模型信息
优先级	中
主成功场景	1.	用户选择评估模型管理功能中的编辑，转入6
2.	用户选择评估模型删除功能，转入4
3.	用户选择编辑评估模型功能，转入7
4.	删除评估模型的数据库中的信息
5.	删除评估模型的模型文件，结束
6.	用户输入新的评估模型信息：
a)	输入评估模型名称
b)	用户选择导入的评估模型文件
c)	用户输入评估模型参数设置
d)	效能评估客户端把评估模型文件及参数设置信息传送给效能评估服务端
e)	效能评估服务端把评估模型文件保存到本地磁盘
f)	效能评估服务端把评估模型信息保存到数据库
7.	用户编辑评估模型信息：a）-c）至少操作一个
a)	修改评估模型名称
b)	用户重新导入的评估模型文件
c)	用户修改评估模型参数设置
d)	效能评估客户端把评估模型文件及参数设置信息传送给效能评估服务端
e)	效能评估服务端把评估模型文件保存到本地磁盘
f)	效能评估服务端把评估模型信息保存到数据库
8.	客户端显示成功
输入信息	效能评估模型说明信息
异常处理情况	网络传递失败，给出提示

图 37 效能评估模型管理活动图
3.3.3　想定监视工具
想定监视工具主要包括二维态势监视、三维态势监视、流程监视三个主要功能。二维态势监视解析想定生成工具服务端推送来的仿真过程数据，实现战场二维交战态势展示；三维态势解析想定生成工具服务端推送来的仿真过程数据，实现战场三维交战态势展示；流程监视首先从想定数据库中读取任务事件列表，然后解析想定生成工具服务端推送来的数据，完成对想定剧情进度的动态显示。

图 38想定监视工具用例图
3.3.3.1　二维态势监视
仿真过程中想定监视工具解析想定生成工具服务端推送来的数据，实现战场二维交战态势展示。
表25　二维态势监视用例描述表
用例名称：二维态势监视
用例编号：
参与者（角色）	想定监视人员
其它参与者，相邻系统	想定生成工具服务端,想定数据库,仿真模型库
功能描述	仿真运行时态势的二维态势监视
前置条件	仿真正常运行
后置条件	二维交战态势展现
优先级	中
主成功场景	1.	监视界面默认以二维图的方式显示战场环境
2.	用户选择监视视角
3.	加载初始态势部署
4.	用户点击仿真开始按键
5.	在海图上动态显示作战双方的兵力运行轨迹及交战状况
6.	仿真结束
扩展流程	2-5 点击右上方小地图，切换二维/三维监视场景

2.a 点击菜单栏，选择监视视角
2.a.1 选择白方视角，对交战过程中的所有场景可见
2.a.2 选择红方或蓝方视角，显示战场黑幕观察模式，仅在己方实体侦测范围之内的实体可见，侦测范围之外的实体不可见，可见视野随实体的运动而变化，用户可拖动时间条显示侦测视野的可见持续时间

5.a 用户右键选择海图上的展示内容，弹出子菜单。选项包括通信拓扑，探测范围，运行轨迹，指挥关系，图标切换等，用户的选项可叠加在海图上显示
5.a.1 用户选择图标切换选项，弹出子菜单。可选图标选项包括简标，军标
5.a.1.a 用户选择简标，海图上所有的实体图标切换成简标
5.a.1.b 用户选择军标，海图上所有的实体图标切换成军标

5.b 用户鼠标移动到兵力时，显示该兵力的属性，移开时属性消失，属性包括该兵力的名称，编队所属，指挥关系

5.c 按住鼠标左键，拖动地图可将待观察的地点放入视野中心

5.d 鼠标左键双击某地点，放大视图

5.e 拖动放大缩小坐标轴，选择放大或缩小视图

5.f 二维态势监视过程中关键事件的处理
5.f.1.a 仿真运行至武器发射，导弹拦截，飞机起飞，飞机降落等关键事件时海图左下角弹出小窗口
5.f.1.a.1 想定监视工具接收由想定生成服务端推送过来的关键事件实体运行信息
5.f.1.a.2 在小窗口中将该实体的运行信息以动画的形式展现出来
5.f.1.b 用户点击关闭小窗口
5.f.2.a 仿真运行至事件结点时，系统从海图右下角弹出通知小窗口，小窗口的显示内容包括事件的所属任务，事件的时间参数设置，兵力设置以及实际执行参数与预期设置的偏差,显示内容包括时间偏差，位置偏差，航向偏差，航速偏差等
5.f.2.b 3s之内用户不点击弹出窗口，窗口自动消失。3s之内用户点击弹出窗口，则窗口位置可拖动
5.f.2.c 用户点击关闭弹出小窗口

5.g 用户右键选择海图上的实体，弹出子菜单。选项包括实体轨迹，实体姿态参数，时间偏差/位置偏差，实体参数监视图等
5.g.1.a 用户选择实体轨迹选项，在子菜单中选择展示实体轨迹，海图中显示该实体的运动轨迹
5.g.1.b 用户选择实体轨迹选项，在子菜单中选择关闭实体轨迹，海图中隐藏该实体的运动轨迹

5.g.2.a 用户选择实体姿态参数选项，海图中弹出小窗口，小窗口的显示内容包括该实体的俯仰角，横滚角，偏航角
5.g.2.b 用户点击关闭弹出小窗口
5.g.3.a 用户选择时间偏差/位置偏差选项，海图中弹出小窗口，小窗口的显示内容包括该实体的时间偏差和位置偏差
5.g.3.b 用户点击关闭弹出小窗口

5.g.4 用户选择实体参数监视图选项，弹出子菜单。选项包括速度参数图，位置参数图，高度参数图
5.g.4.a 用户选择速度参数图，海图中弹出小窗口，小窗口显示
该实体30min内的速度变化
5.g.4.b 用户选择位置参数图，海图中弹出小窗口，小窗口显示
该实体30min内的位置变化
5.g.4.c 用户选择高度参数图，海图中弹出小窗口，小窗口显示
该实体30min内的高度变化

5.g.5.a 用户选择实体图标切换选项，在子菜单中选择简标，海图上所有的实体图标切换成简标
6.g.5.b 用户选择实体图标切换选项，在子菜单中选择军标，海图上所有的实体图标切换成军标
5.g.5.c 用户选择实体图标切换选项，在子菜单中选择自定义图标，海图上所有的实体图标切换成自定义图标

图 39 二维态势监视用例活动图

 图 40 二维态势监视界面
3.3.3.2　三维态势监视
仿真过程中想定监视工具解析想定生成工具服务端推送来的数据，实现战场三维交战态势展示。
表26　三维态势监视用例描述表
用例名称：三维态势监视
用例编号：
参与者（角色）	想定监视人员
功能描述	仿真运行时三维态势监视
其它参与者，相邻系统	想定生成工具服务端,想定数据库,仿真模型库
前置条件	仿真正常运行
后置条件	交战态势以三维形式展示
优先级	中
主成功场景	1.	监视界面以三维的方式显示战场设置
2.	加载初始态势部署
3.	用户点击仿真开始按键
4.	在海图上动态显示作战双方的兵力运行轨迹及交战状况
5.	仿真过程中，关键事件视图展示事件参数
6.	仿真结束
扩展流程	2-5 点击右上方小地图，切换二维/三维监控场景

3.a 点击菜单栏，选择自由监视，用户可以自由移动视角监视海图
3.b点击菜单栏，选择跟随监视，用户可以选择某个实体，视角随着该实体运动而改变

5.a用户右键选择海图上的展示内容，弹出子菜单。选项包括通信拓扑，探测范围，运行轨迹，指挥关系，图标切换等，用户的选项可叠加在海图上显示
5.a.1 用户选择图标切换选项，弹出子菜单。选项包括简标，军标和自定义图标
5.a.1.a 用户选择简标，海图上所有的实体图标切换成简标
5.a.1.b 用户选择军标，海图上所有的实体图标切换成军标

5.b用户鼠标移动到兵力上显示该兵力的属性，移开时属性消失,属性包括该兵力的名称，编队所属，指挥关系

5.c 长按鼠标左键，拖动地图至待观察的地点

5.d 鼠标左键双击某地点或某实体，选择放大视图

5.e 拖动放大缩小坐标轴，选择放大或缩小视图

5.f 鼠标右键单击实体，选择跟踪实体

5.g 长按键盘Ctrl键的同时滚动鼠标，旋转视角

5.h 关键事件视图
5.h.1.a 仿真运行至任务的事件结点时，系统从海图右下角弹出通知小窗口，小窗口的显示内容包括事件的所属任务，事件的时间参数设置，兵力设置以及实际执行参数与预期设置的偏差,显示内容包括时间偏差，位置偏差，航向偏差，航速偏差等
5.h.1.b 3s之内用户不点击弹出窗口，窗口自动消失。3s之内用户点击弹出窗口，则窗口位置可拖动
5.h.1.c 用户点击关闭弹出小窗口

图41　三维态势监视用例活动图

图 42 三维态势监视界面
3.3.3.3　流程监视
仿真过程中想定监视工具首先从想定数据库中读取任务事件列表，然后解析想定生成工具服务端推送来的数据，完成对想定剧情进度的动态显示。
表27　流程监视用例描述表
用例名称：流程监视
用例编号：
参与者（角色）	想定监视人员
其它参与者，相邻系统	想定生成工具服务端,想定数据库,仿真模型库
功能描述	仿真开始后，动态分析与显示作战流程进度
前置条件	完成想定剧情设定
后置条件	以任务事件为单元的流程进度的动态显示
优先级	高
主成功场景	1.	用户选择流程监视界面
2.	用户选择监视视角：红方，蓝方，白方
3.	系统读取监视视角下对应的任务名称，任务参数等信息，分别以空白进度条的形式部署到界面上
4.	系统解析想定生成工具服务端推送的数据
5.	在仿真运行过程中，根据任务进展，滚动进度条
输入信息	选择监视视角
输出信息	监视视角下任务的进展
非功能需求	动态读取任务执行进度的周期应该在用户可接受的范围之内
图43　流程监视用例活动图


图 44 流程监视界面
3.4　运行环境需求
3.4.1　硬件运行环境需求
主机CPU：2.4GHz以上
硬盘容量：80G或以上
内存：1G或以上
屏幕分辨率：1024*768或更高
网络带宽：10M - 100M
3.4.2　软件运行环境需求
操作系统：Windows XP或更高
数据库：oracle 8i 或更高版本
Flames
Visual Studio2010
ArcGIS 10.0
3.5　适应性要求
详细说明CSCI适应现场具体条件和系统环境改变的各种要求。
3.5.1　依赖安装的数据
描述每次安装所需现场的具体数据，例如：场地的纬度、经度、雷达的范围和有效区以及规定的安全限制等。此外，还需说明使用这些数据的CSCI的功能。
3.5.2　操作参数
描述CSCI所需的、根据操作要求可在指定范围内变化的参数。例如：允许的弹道偏差、导航定位模型数目等。
3.6　时间要求
   各工具之间的数据传输时间不超过1秒。
3.7　人的特性/人的工程需求
详细说明CSCI对人员因素的工程需求，包括：
a)	用户熟悉设备模型，认知模型，作战单元信息等，会设定想定剧情；
b)	若想定剧情设置不完整，无法开始仿真过程；
c)	数据库连接不成功，会导致系统无法正常运转。
3.8　质量因素要求
细化对CSCI质量因素的要求，包括：易用性、可维护性、可扩展性以及实时性等。
易用性要求：
界面设计尽可能与导演台软件一致，以用户熟悉的方式展示软件功能。
可维护性要求一般有：
e)	文档采用标准模板；程序采用易于理解的统一命名方式；想定生成文件采用统一标准军事想定描述语言MSDL传输想定剧情数据；各子工具通过实现统一组件的接口访问数据库;
f)	若仿真引擎改变时，只需要修改想定生成部分写入代码部分，其它部分均无需关心；
可扩展性要求支持接口的动态生成技术，作战效能评估部分支持效能评估模型的扩展等。
实时性要求：
为保证想定监视工具以及想定生成工具客户端对大量的仿真过程数据实时展示，想定生成工具服务端从共享内存中获取到仿真过程数据后，直接以FLAMES发送的报文格式推送给想定监视工具和想定生成工具客户端。
4　合格性需求
分节规定合格性方法，以及证实该CSCI满足本文档第3章的需求所必需的特殊合格性需求。
5　合格性方法和级别
a)	合格性方法包括：
1)	演示：对CSCI（或部分CSCI）的进行直接可观察的功能操作，不需要使用复杂或专用的测试设备。
2)	检查：对CSCI的编码、文档等的直观检查等。
b)	合格性级别划分如下：
1)	配置项：在CSCI中发现的质量问题；
2)	系统集成：在系统集成时发现的问题；
3)	系统：在系统中发现的质量问题；
4)	系统安装：在系统安装时发现的质量问题。
''', 'keyword' : ['包括'] }
ReFileJson = json.dumps(ReFilePath,ensure_ascii=False)

# ReFilePath1 = [{'id':1,'description':['文档采用标准模板；程序采用易于理解的统一命名方式；想定生成文件采用统一标准军事想定描述语言MSDL传输想定剧情数据；各子工具通过实现统一组件的接口访问数据库','分节规定合格性方法，以及证实该CSCI满足本文档第3章的需求所必需的特殊合格性需求。']}]
# SuggFilePath = [{'id':2,'description':['建议补充仿真模型管理人员向集成设计平台推送相关信息的类型，格式等细节。','建议补充想定制作人员在设置完成想定剧情后的调用仿真引擎中添加想定剧情预测功能。']}]
# ReFilePath1 = {'items':[{'itemid':15,'name' : '文件生成功能','description':'文档采用标准模板；程序采用易于理解的统一命名方式；想定生成文件采用统一标准军事想定描述语言MSDL传输想定剧情数据；各子工具通过实现统一组件的接口访问数据库','type':'FR'},
#                         {'itemid':25,'name' : '文件读取功能','description':'分节规定合格性方法，以及证实该CSCI满足本文档第3章的需求所必需的特殊合格性需求。','type':'FR'},
#                         {'itemid':3,'name' : '文件修改功能','description':'...','type':'FR'}]}
# SuggFilePath = {'items':[{'sugesid':4,'description':'建议补充仿真模型管理人员向集成设计平台推送相关信息的类型，格式等细节。'},
#                         {'sugesid':5,'description':'建议补充想定制作人员在设置完成想定剧情后的调用仿真引擎中添加想定剧情预测功能。'},
#                         {'sugesid':6,'description':'建议将需求1.1和需求1.3进行合并。'},
#                         {'sugesid':7,'description':'将条目1.1删除并用设置完成想定剧情后的调用仿真引擎中添加想定剧情预测功能来替代。'}]}

FilePath = {'items':[{'itemid':15,'name' : '文件生成功能','description':'具有较强的连续不间断运行能力。根据全军业务信息系统总体及通用服务总体技术方案中硬件质量特性设计中的可靠性设计，正常负载情况下，系统需要具有足够的容错性、健壮性。除非发生磁盘故障，否则业务通用服务软件不应出现丢失数据的现象。','type':'FR'},
                     {'itemid':25,'name' : '文件读取功能','description':'具有较强的容错能力。不能因用户误操作而导致系统崩溃、异常退出、死机等致命错误，应通过给出提示信息，尽量减少工作损失。若由于外在原因而导致上述致命错误，只要重新启动计算机，即可恢复工作。','type':'FR'},
                     {'itemid':3,'name' : '文件修改功能','description':'具有较强的适应能力。能够适应各种异常环境或者异常情况，应通过提醒功能，减少异常环境或者异常情况带来的损失。','type':'FR'},
                     {'itemid': 123, 'name': '文件修改功能','description': '对输入的数据进行合理性和有效性检验，在输入数据违法的情况下，软件具有容错性可维持运行，并能正确的提示用户。', 'type': 'FR'},
                     {'itemid': 23, 'name': '文件修改功能','description': '正常负载情况下或用户误操作后系统正常运行超过24小时的概率大于99.9 %。', 'type': 'FR'},
                     {'itemid': 24, 'name': '文件修改功能', 'description': '系统崩溃后恢复正常的时间小于10分钟的概率等于100.00%。。','type': 'FR'},
                     {'itemid': 25, 'name': '文件修改功能', 'description': '人机界面应具备界面友好性和一致性，采用合理的窗口布局，窗口层次最多不超过4层，同一个组件中的不同的窗口界面风格保持一致等；。', 'type': 'FR'},
                     {'itemid': 26, 'name': '文件修改功能', 'description': '操作命令及参数应有明确的定义，操作次数应合理；', 'type': 'FR'},
                     {'itemid': 27, 'name': '文件修改功能', 'description': '应提供正确详细的用户手册；', 'type': 'FR'},
                     {'itemid': 28, 'name': '文件修改功能', 'description': '对用户的错误操作应有提示，当软件运行发生错误时，软件内部错误的信息提示应明确，使用户明白发生了什么错误；', 'type': 'FR'}],
            'suggestions':[{'sugesid':4,'description':'提供评估指标体系可视化构建及多样化展示功能，支持以评估算子组合的方式构建评估计算模型，评估算子包括基础运算算子、数据映射算子、归一化算子、基本流程算子、统计算子等，支持对评估算子进行扩展；'},
                           {'sugesid':5,'description':'需要补充部署终端服务器或客户端，不存在不同状态下具有不同功能需求的情况。'},
                            {'sugesid':6,'description':'应删除3.14.2可靠性中的“具有较强的适应能力。能够适应各种异常环境或者异常情况，应通过提醒功能，减少异常环境或者异常情况带来的损失。”'},
                           {'sugesid':7,'description':'应将3.14.2可靠性中的正常负载情况和用户误操作两种情况分开来写。'}]}


# ReFileJson1 = json.dumps(ReFilePath1)
# SuggFileJson = json.dumps(SuggFilePath)
FileJson = json.dumps(FilePath, ensure_ascii=False)

# 打开 gRPC channel，连接到 localhost:50051
channel = grpc.insecure_channel('localhost:50051')
# 创建一个 stub (gRPC client)
stub = Requirement_pb2_grpc.RequirementStub(channel)
# 创建一个有效的请求消息 value
revalue = Requirement_pb2.ReSplitValue(value=ReFileJson)
# value = Code15_pb2.ReValue(value=str(ReFileJson1),value1=str(SuggFileJson))
value = Requirement_pb2.ReValue(value=str(FileJson))
# synValue = Code15_pb2.synValue(value=ReFilePath)

# 带着 Number 去调用 Itemized
response = stub.Itemized(revalue)
print(str(response.value1))
response = stub.Relate_Re_Sugg(value)
print(response.value1)
# response = stub.GetChSyn(synValue)
# print(response.value1)