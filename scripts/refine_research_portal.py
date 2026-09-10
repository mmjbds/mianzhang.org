"""Idempotent edits to existing research entry pages; does not generate papers."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
START='<!-- research-paths-20260910 -->'
END='<!-- /research-paths-20260910 -->'

def pathways(zh=False):
    rows=[
        (('Can an answer change the situation it describes?','回答会改变它所描述的局面吗？'),
         ('ReflexBench compares observer-participant reasoning across four observer-depth levels. The public browser contains 20 scenarios; its orientation receipt is not an automated benchmark score.','ReflexBench 比较四个观察者深度层级中的观察者—参与者推理。公开浏览器包含 20 个情景；它的引导记录不是自动基准分数。'),
         '/ai-agent-reliability/','/papers/kdd-2026/','/demos/reflexbench-observer-depth/','https://github.com/mmjbds/reflexbench'),
        (('Does feedback reduce repeated mistakes?','反馈能减少重复犯错吗？'),
         ('WisdomBench examines failure and feedback over repeated episodes. Check the released task protocol, scoring and run evidence before interpreting improvement as general learning.','WisdomBench 在重复回合中检查失败与反馈。应结合公开任务协议、评分与运行证据，判断改进是否支持更广泛的学习结论。'),
         '/benchmarks/wisdombench-failure-learning/','/papers/','/evidence/','https://github.com/mmjbds/wisdombench'),
        (('What must be checked before an agent acts?','智能体行动之前需要检查什么？'),
         ('Proof-Carrying Action separates evidence and permission from fluent answers. The mini gate illustrates ACT, WAIT, QUERY and REFUSE; passing it does not certify a deployed system.','Proof-Carrying Action 将证据与行动权限同流畅回答分开。小型门控演示展示 ACT、WAIT、QUERY 与 REFUSE；通过演示不代表部署系统已获得可靠性认证。'),
         '/concepts/proof-carrying-action.html','/evidence/','/demos/proof-action-mini/','https://github.com/mmjbds/proof-carrying-action')]
    choose=lambda x:x[int(zh)]
    body=START+'<section class="section research-paths"><div class="section-head"><p class="kicker">'+choose(('Research paths','研究路径'))+'</p><h2>'+choose(('A question, a method, something you can inspect.','从问题到方法，再到可以检查的材料。'))+'</h2></div>'
    for question,summary,method,paper,demo,code in rows:
        body+='<article><h3>'+choose(question)+'</h3><p>'+choose(summary)+'</p><div class="hero-actions">'+''.join('<a class="text-link" href="'+url+'">'+choose(label)+'</a>' for url,label in [(method,('Method','方法')),(paper,('Papers & evidence','论文与证据')),(demo,('Inspect the public example','查看公开示例')),(code,('Code & version history','代码与版本记录'))])+'</div></article>'
    body+='<p>'+choose(('Read the linked artifact version and claim scope together. Public archives and our own repositories provide inspectable material, not independent validation of commercial products.','请同时阅读所链接材料的版本与结论范围。公开归档和自有代码仓库提供可检查材料，不代表商业产品已获得独立验证。'))+'</p></section>'+END
    return body

def main():
    entries=['index.html','zh/index.html','guides/index.html','evidence/index.html','demos/index.html','technology/index.html']
    for name in entries:
        p=ROOT/name;s=p.read_text(encoding='utf-8');zh=name.startswith('zh/')
        s=re.sub(re.escape(START)+'.*?'+re.escape(END),'',s,flags=re.S)
        if name=='index.html':
            s=s.replace('Start from the question readers actually search.','What makes an AI agent reliable enough to act?')
            s=s.replace('These pages connect the research to questions people already ask: how to build reliable AI agents, ground hallucination claims, evaluate benchmarks, block unproven trades, and govern evidence in robotics.','Explore evidence before action, repeated failure, observer effects and embodied feedback. Follow each question to its method, public material and limits.')
            s=s.replace('Premium black-gold visualization of residual failure scoring and closed-loop evidence.','Conceptual illustration of residual failure scoring and evidence feedback; not a measurement plot.')
        if zh:
            s=s.replace('中文入口：用同一套证据边界解释可靠 AI 行动。','Mian Zhang：研究 AI 如何从失败中学习、在行动前检查证据。')
            s=s.replace('先回答中文读者能听懂的问题。','AI 怎样学习、判断并安全地行动？')
            s=s.replace('人体式系统架构视觉图。','人体式系统架构概念示意图，并非运行数据。')
        s=s.replace('</main>',pathways(zh)+'\n</main>')
        if name in ('index.html','zh/index.html'):
            relation=('<section class="section"><h2>研究档案与产品门户</h2><p>本站是 Mian Zhang 与 Ouroboros Project 的研究档案。<a href="https://aitoolshow.com/zh/">AI Tool Show</a> 是相关商业产品门户；Ouroboros Check 是同名但不同用途的金融研究产品。研究论文与演示不自动证明商业产品的有效性。</p></section>' if zh else '<section class="section"><h2>Research archive and product portal</h2><p>This site is the research archive of Mian Zhang and the Ouroboros Project. <a href="https://aitoolshow.com/">AI Tool Show</a> is the related commercial product portal; Ouroboros Check is a distinct financial research product sharing the name. Research papers and demonstrations do not automatically validate commercial products.</p></section>')
            marker='<!-- entity-relationship-20260910 -->'
            s=re.sub(re.escape(marker)+'.*?<!-- /entity-relationship-20260910 -->','',s,flags=re.S)
            s=s.replace('</main>',marker+relation+'<!-- /entity-relationship-20260910 -->\n</main>')
        p.write_text(s,encoding='utf-8')

if __name__=='__main__':main()
