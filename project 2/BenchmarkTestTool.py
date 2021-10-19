#submit test and check the ranking
import json
import requests
import numpy as np

def submit_benchmark_test(submitter, data, dataset, comment='', submit=True):
    '''
    submitter:提交人
    data: 模型输出，格式为:
        [
         [date0, stock0, score0],
         [date1, stock1, score1],
         [date2, stock2, score2],
         ...
        ]
    dataset: 指定benchmark数据集的名字
    '''
    host = "http://localhost:5002"
    params = {
        "submitter":submitter,
        "dataset":dataset,
        "data":data,
        "comment":comment,
        "submit":submit,
    }

    benchmark_test_result = requests.post(url="%s/benchmark_test"%host,json=params)
    print("TEST STATUS:", benchmark_test_result.json()['status'])
    print("*"*60)
    print("COMPLETENESS CHECK")
    print("*"*60)
    for metric in benchmark_test_result.json()["completeness_result"]:
        print("%s: "%metric, benchmark_test_result.json()["completeness_result"][metric])
    print()
    print("*"*60)
    print("SUBMIT SIGNAL PERFORMANCE")
    print("*"*60)
    for metric in benchmark_test_result.json()["result"]:
        if metric in ["rank"]:
            if benchmark_test_result.json()["result"][metric] < 10:
                print("%s: "%metric, str(benchmark_test_result.json()["result"][metric])+ "Awesome!")
        else:      
            print("%s: "%metric, str(benchmark_test_result.json()["result"][metric]))
    print()
    print("*"*60)
    print("MODEL SCORE'S EXPOSURE ON RISKS AND INDUSTRIAL FACTORS (BARRA ANALYSIS)")
    print("*"*60)
    for metric in benchmark_test_result.json()["barra_result"]:
        print("%s: "%metric, benchmark_test_result.json()["barra_result"][metric])
    
        
        
def check_test_rank(rank_by="pearson", topN=100, submitter="all" ,dataset="all"):
    '''
    rank_by: 指定排序的key是什么，默认是pearson
    topN: 指定显示前多少条提交测试记录
    submitter: 指定显示哪个提交人的提交记录
    dataset: 指定显示哪个benchmark数据集的提交测试结果
    '''
    
    
    host = "http://localhost:5002"
    params = {
        "submitter":submitter,
        "rank_by":rank_by,
        "topN":topN,
        "dataset":dataset
    }
    benchmark_rank_result = requests.post(url="%s/check_rank"%host,json=params)
    print(benchmark_rank_result.json()["rank"])
    
