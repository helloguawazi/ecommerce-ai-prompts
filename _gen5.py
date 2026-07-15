import json, urllib.request, os, sys
k = 'sk-55a54f7b4f3b4a4da49af5dfb9507235'
api = 'https://grsaiapi.com/v1/api/generate'
tasks = [
    ('ai-haibao-shengcheng.jpg', 'AI poster generation tool display, professional promotional poster mockup, marketing design, elegant typography'),
    ('ai-xiugai-tupian.jpg', 'AI photo editing demonstration, before and after comparison, image retouching and enhancement, professional editing tools'),
    ('ai-haibao-sheji2.jpg', 'Professional poster design showcase, creative promotional banner, modern layout, premium branding style'),
    ('ai-xiutu-ruanjian.jpg', 'AI photo editing software interface, retouching tools display, professional image processing, before after comparison'),
    ('zuo-haibao-yong-nage-ai.jpg', 'Poster design tool comparison, multiple poster mockups, professional marketing designs, creative templates'),
]
MAX_RETRIES = 3

for fname, prompt in tasks:
    ok = False
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            b = json.dumps({'model':'gpt-image-2','prompt':prompt,'aspectRatio':'1024x1024','replyType':'json'}).encode()
            r = urllib.request.Request(api, data=b, headers={'Authorization':'Bearer '+k,'Content-Type':'application/json'})
            d = json.loads(urllib.request.urlopen(r,timeout=180).read())
            if 'results' in d and d['results'] and d['results'][0].get('url',''):
                urllib.request.urlretrieve(d['results'][0]['url'], 'images/'+fname)
                print(f'OK {fname}')
                ok = True
                break
            else:
                print(f'  {fname} 第{attempt}次无数据，重试...')
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f'  {fname} 第{attempt}次超时，重试...')
            else:
                print(f'FAIL {fname}: {str(e)[:60]}')
    if not ok:
        print(f'FAIL {fname}: {MAX_RETRIES}次均失败')
print('Done!')
