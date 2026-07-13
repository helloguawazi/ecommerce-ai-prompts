export const meta = {
  name: 'content-publish',
  description: 'Claude写文 + Grsai生图 -> 写入文件停住审核',
  phases: [
    { title: '分析', detail: 'Claude判断站点归属，生成标题和生图提示词' },
    { title: '写文', detail: 'Claude生成SEO优化文章' },
    { title: '生图', detail: '调Grsai API生成配图' },
    { title: '整合', detail: '写入文件，git add，停住等审核' },
  ],
}

const keyword = args?.keyword
if (!keyword) {
  log('请提供 keyword 参数')
  return { success: false, error: 'missing keyword' }
}
log('关键词: ' + keyword)

// Phase 1: 分析
phase('分析')
log('正在分析关键词归属站点...')
// 注意：image_prompt 要生成"效果展示型"图片，不是工具界面截图
// poster站 → 海报成品图 | aishop站 → 商品图/详情页 | image2站 → 前后对比图

const analysis = await agent({
  prompt: '你是内容策略专家。分析关键词「' + keyword + '」判断站点归属。\n\n规则：\n- poster站 - 含海报/banner/促销/节日，网站功能是一键AI生成海报\n- aishop站 - 含详情页/主图/白底图/电商图，网站功能是AI生成电商商品图和详情页\n- image2站 - 含image2/ai修图/ai生图/ai制图/nanobanana，网站功能是AI修图和图片处理\n- 其他含ai的归image2站\n\n生成 image_prompt 时注意：要生成"效果展示型"图片，不是工具界面截图。\n- poster站：一张精美的海报成品（促销海报/节日海报，有产品图+文案排版+设计感）\n- aishop站：一张专业的电商商品图（白底图或场景图，商业摄影级光影质感）\n- image2站：一张AI修图前后对比图（左右对比，左模糊原图右修复后效果）\n\n返回JSON：{"site":"站点","domain":"域名","category":"分类","suggested_title":"有场景的SEO标题15-30字","meta_description":"描述","tags":[],"image_prompt":"英文生图prompt，描述成品效果/对比效果，含光线构图风格细节","image_aspect":"1024x1024"}',
  label: '分析: ' + keyword,
  phase: '分析',
  schema: {
    type: 'object',
    properties: {
      site: { type: 'string', enum: ['poster', 'aishop', 'image2'] },
      domain: { type: 'string' },
      category: { type: 'string' },
      suggested_title: { type: 'string', minLength: 8, maxLength: 50 },
      meta_description: { type: 'string' },
      tags: { type: 'array', items: { type: 'string' }, minItems: 3, maxItems: 5 },
      image_prompt: { type: 'string', minLength: 20 },
      image_aspect: { type: 'string' },
    },
    required: ['site', 'domain', 'category', 'suggested_title', 'tags', 'image_prompt'],
  },
})
if (!analysis) { return { success: false, error: 'analysis failed' } }
log('站点: ' + analysis.site + ' -> ' + analysis.domain)
log('标题: ' + analysis.suggested_title)

// Phase 2: 写文
phase('写文')
log('正在生成SEO文章...')

const linkRules = {
  aishop: '- 植入海报站链接: https://poster.anyachina.cn',
  poster: '- 植入电商图站链接: https://aishop.anyachina.cn',
  image2: '- 植入 https://aishop.anyachina.cn 和 https://poster.anyachina.cn',
}

const article = await agent({
  prompt: '写800-1500字中文教程。标题: ' + analysis.suggested_title + ' 站点: ' + analysis.site + ' 分类: ' + analysis.category + ' 标签: ' + analysis.tags.join(', ') + ' 外链: ' + linkRules[analysis.site] + ' 要求：H1+H2/H3，痛点-主体-结语含外链，SEO自然分布。输出--- 正文开始 ---\\n正文\\n--- 正文结束 ---',
  label: '写文: ' + analysis.suggested_title,
  phase: '写文',
})
if (!article) { return { success: false, error: 'article failed' } }
log('文章生成完成')

// Phase 3: 生图
phase('生图')
log('正在调Grsai API生图...')
log('请在bash中先执行: export GRSAI_API_KEY=你的Key')

const img = await agent({
  prompt: '用bash调Grsai API生图。用环境变量$GRSAI_API_KEY做认证。\n\ncurl -s ENDPOINT -H "Authorization: Bearer $GRSAI_API_KEY" -H "Content-Type: application/json" -d \'{"model":"gpt-image-2","prompt":"' + analysis.image_prompt + '","aspectRatio":"' + (analysis.image_aspect || '1024x1024') + '","replyType":"json"}\' \n\n将上面的ENDPOINT替换为 https://grsaiapi.com/v1/api/generate\n取image_url或b64_json，下载到images/目录，确认保存路径。',
  label: '生图: ' + analysis.suggested_title,
  phase: '生图',
})
log('生图完成')

// Phase 4: 整合
phase('整合')
log('正在写入文件并git add...')

const writeResult = await agent({
  prompt: '写入内容到仓库并记录日志。\n标题: ' + analysis.suggested_title + ' 描述: ' + analysis.meta_description + ' 标签: ' + analysis.tags.join(', ') + ' 站点: ' + analysis.site + ' 域名: ' + analysis.domain + '\\n正文:\\n' + article + '\\n外链: ' + linkRules[analysis.site] + '\\n\\n操作：1. 检查prompts/编号 2. 创建prompts/{编号}-{关键词}.md含H1/正文/配图/外链/页尾未来图链接 3. 更新README.md目录 4. 更新 .claude/keywords/generated.json 追加新记录（id递增，含keyword/site/title/file/image/image_prompt/date） 5. git add . 6. git status --short 7. 不要commit不要push',
  label: '整合: ' + analysis.suggested_title,
  phase: '整合',
})

log('全部完成！文件已git add，等待你审核')
return { success: true, keyword: keyword, site: analysis.site, title: analysis.suggested_title }
