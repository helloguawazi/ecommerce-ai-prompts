#!/usr/bin/env python
"""生图脚本：调 Grsai API 生成配图，保存到 images/ 目录。
用法：
  python .claude/scripts/generate_image.py --prompt "图片描述" --output "文件名.jpg"
  python .claude/scripts/generate_image.py --prompt "描述" --output "img.jpg" --aspect "1024x1024"

Key 从环境变量 GRSAI_API_KEY 读取。
"""

import json, urllib.request, base64, os, sys, argparse

API_URL = 'https://grsai.dakka.com.cn/v1/api/generate'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--aspect', default='1024x1024')
    args = parser.parse_args()

    api_key = os.environ.get('GRSAI_API_KEY') or ''
    if not api_key:
        # 尝试从文件读取
        for p in ['k.txt', '.tmp_key', os.path.expanduser('~/.grsai_key')]:
            if os.path.exists(p):
                api_key = open(p).read().strip()
                break
    if not api_key:
        print('ERROR: 请设置 GRSAI_API_KEY 环境变量')
        sys.exit(1)

    body = json.dumps({
        'model': 'gpt-image-2',
        'prompt': args.prompt,
        'aspectRatio': args.aspect,
        'replyType': 'json'
    }).encode('utf-8')

    req = urllib.request.Request(API_URL, data=body, headers={
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json',
    })

    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'ERROR: API调用失败: {e}')
        sys.exit(1)

    # 提取图片
    image_url = ''
    b64_data = ''
    if 'results' in data and data['results']:
        item = data['results'][0]
        image_url = item.get('url', '') or ''
        b64_data = item.get('b64_json', '') or ''
    elif 'data' in data and data['data']:
        item = data['data'][0]
        image_url = item.get('url', '') or ''
        b64_data = item.get('b64_json', '') or ''

    if b64_data:
        img_data = base64.b64decode(b64_data)
        with open('images/' + args.output, 'wb') as f:
            f.write(img_data)
        print(f'OK: images/{args.output} (b64, {len(img_data)} bytes)')
    elif image_url:
        urllib.request.urlretrieve(image_url, 'images/' + args.output)
        size = os.path.getsize('images/' + args.output)
        print(f'OK: images/{args.output} (url, {size} bytes)')
    else:
        print(f'ERROR: 未找到图片数据: {json.dumps(data, ensure_ascii=False)[:300]}')
        sys.exit(1)

if __name__ == '__main__':
    main()
