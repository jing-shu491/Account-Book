"""DeepSeek 分析：只发送汇总数据，密钥留在服务端。"""
import os, json, urllib.request, urllib.error
import stats
def analyze(rows):
    key=os.environ.get('DEEPSEEK_API_KEY','').strip()
    if not key: raise ValueError('请设置 DEEPSEEK_API_KEY 环境变量并重启服务。')
    if not rows: raise ValueError('当前范围没有记录，请先记账或调整筛选条件。')
    summary=stats.summarize(rows)
    payload={'model':'deepseek-chat','messages':[{'role':'system','content':'你是个人记账分析助手。金额单位为分。用简洁中文给出：收支概况、支出结构、三条可执行建议。只根据数据分析，不推断未提供的事实，不提供投资建议。'},{'role':'user','content':json.dumps(summary,ensure_ascii=False)}],'max_tokens':900}
    req=urllib.request.Request('https://api.deepseek.com/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=45) as r: return json.load(r)['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        raise ValueError('AI 请求失败（HTTP %s），请检查密钥、余额和服务状态。'%e.code)
    except (urllib.error.URLError,TimeoutError): raise ValueError('AI 连接超时或网络不可用，请稍后重试。')
