# import json
#
#
# jsonpath = 'data1.json'
# with open(jsonpath, 'r') as f:
#     data = f.read()
#     res = json.loads(data)
#
# a = list()
# b = list()
#
# for k, v in res.items():
#
#     temp_max = max(zip(v.values(), v.keys()))
#     a.append(k)
#     b.append(temp_max[0])
#
#
# zipped = zip(a,b)
#
# # print()
# zz = sorted(list(zipped), key=lambda x: int(float(x[1])))
# print(zz[-1][1])

# import asyncio
# from threading import Thread
#
#
# async def production_task():
#     i = 0
#     while True:
#         # 将consumption这个协程每秒注册一个到运行在线程中的循环，thread_loop每秒会获得一个一直打印i的无限循环任务
#         asyncio.run_coroutine_threadsafe(consumption(i),
#                                          thread_loop)  # 注意：run_coroutine_threadsafe 这个方法只能用在运行在线程中的循环事件使用
#         await asyncio.sleep(1)  # 必须加await
#         i += 1
#
#
# async def consumption(i):
#     while True:
#         print('-----------------')
#         print("我是第{}任务".format(i))
#         print('-----------------')
#         await asyncio.sleep(1)
#
#
# def start_loop(loop):
#     #  运行事件循环， loop以参数的形式传递进来运行
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
#
#
# thread_loop = asyncio.new_event_loop()  # 获取一个事件循环
# run_loop_thread = Thread(target=start_loop, args=(thread_loop,))  # 将次事件循环运行在一个线程中，防止阻塞当前主线程
# run_loop_thread.start()  # 运行线程，同时协程事件循环也会运行
#
# advocate_loop = asyncio.get_event_loop()  # 将生产任务的协程注册到这个循环中
# advocate_loop.run_until_complete(production_task())  # 运行次循环
# import pandas as pd
#
#
# temp_list = ['Test_Int[11]', 'Test_Int[9]', 'Test_Int[21]', 'Test_Int[39]']
# temp_dic = [{'Test_Int[9]': 187}, {'Test_Int[11]': 187}, {'Test_Int[21]': 187}, {'Test_Int[28]': 187}, {'Test_Int[39]': 187}, {'Test_Int[16]': 187}, {'Test_Int[12]': 187}, {'Test_Int[25]': 187}, {'Test_Int[14]': 187}, {'Test_Int[13]': 187}, {'Test_Int[30]': 187}, {'Test_Int[17]': 187}, {'Test_Int[33]': 187}, {'Test_Int[1]': 187}, {'Test_Int[5]': 187}, {'Test_Int[22]': 187}, {'Test_Int[2]': 187}, {'Test_Int[27]': 187}, {'Test_Int[18]': 187}]
#
# article = pd.DataFrame({"tagname": uu})
# tagnameid = pd.DataFrame({"tagname":[s[0] for s in temp_dic.items()],"value":[s[1] for s in temp_dic.items()]})
# tagnameid.set_index("tagname")
#
# df_inner = pd.merge(article,tagnameid,how="inner")
# print(list(df_inner["value"]))
