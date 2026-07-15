import json, urllib.request, os
k = 'sk-55a54f7b4f3b4a4da49af5dfb9507235'
api = 'https://grsaiapi.com/v1/api/generate'
tasks = [
    ('ai-sheji-haibao.jpg', 'Professional poster design comparison, before after, elegant marketing visual creative layout'),
    ('ai-haibao-zhineng.jpg', 'Smart AI poster generator, professional promotional display, modern design templates'),
    ('image2-tool.jpg', 'AI image generation software interface, creative digital art, modern technology workspace'),
    ('neng-p-tu-ai.jpg', 'AI photo editing tools collage, before and after retouching examples, various editing features'),
    ('dianshang-zhutu-ai.jpg', 'E-commerce product main image on white background, professional product photography, studio lighting'),
    ('ai-tushengtu.jpg', 'Image to image AI conversion, original product photo transforming to different artistic styles'),
    ('tushengtu-ai-tool.jpg', 'AI image transformation demo, side by side original and generated artistic versions'),
    ('shengcheng-haibao-ai2.jpg', 'AI poster generator showcase, multiple poster mockups, professional marketing designs'),
    ('ai-shengtu-zaixian.jpg', 'AI image generation online interface, creative tools on screen, digital artwork creation'),
    ('nano-banana-tool.jpg', 'AI image generation technology concept, digital art creation, modern software interface'),
]
for f, p in tasks:
    try:
        b = json.dumps({'model':'gpt-image-2','prompt':p,'aspectRatio':'1024x1024','replyType':'json'}).encode()
        r = urllib.request.Request(api, data=b, headers={'Authorization':'Bearer '+k,'Content-Type':'application/json'})
        d = json.loads(urllib.request.urlopen(r,timeout=180).read())
        urllib.request.urlretrieve(d['results'][0]['url'], 'images/'+f)
        print(f'OK {f}')
    except Exception as e:
        print(f'FAIL {f}: {str(e)[:60]}')
print('Done!')
