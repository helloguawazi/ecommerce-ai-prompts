import json, os
d = json.load(open('.claude/keywords/generated.json', encoding='utf-8-sig'))
new = [
    {'id':42,'keyword':'ai海报生成','site':'poster','title':'AI海报生成工具哪个好？','file':'ai海报生成-教程.md','image':'images/ai-haibao-shengcheng.jpg','image_prompt':'AI poster generation','date':'2026-07-15'},
    {'id':43,'keyword':'ai修改图片','site':'image2','title':'AI修改图片用什么工具？','file':'ai修改图片-教程.md','image':'images/ai-xiugai-tupian.jpg','image_prompt':'AI photo editing','date':'2026-07-15'},
    {'id':44,'keyword':'ai海报设计','site':'poster','title':'AI海报设计工具推荐','file':'ai海报设计2-教程.md','image':'images/ai-haibao-sheji2.jpg','image_prompt':'poster design showcase','date':'2026-07-15'},
    {'id':45,'keyword':'ai修图软件','site':'image2','title':'AI修图软件哪个好用？','file':'ai修图软件-推荐.md','image':'','image_prompt':'','date':'2026-07-15'},
    {'id':46,'keyword':'做海报用哪个ai工具','site':'poster','title':'做海报用哪个AI工具？','file':'做海报用哪个ai工具-推荐.md','image':'','image_prompt':'','date':'2026-07-15'},
]
d.extend(new)
json.dump(d, open('.claude/keywords/generated.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'OK, now {len(d)} records')
