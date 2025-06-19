const API_URL = "http://localhost:8000/api"; // 如部署到服务器请改为实际后端地址

const analyzeBtn = document.getElementById('analyzeBtn');
const textArea = document.getElementById('text');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const sentimentLabel = document.getElementById('sentimentLabel');
const sentimentEmoji = document.getElementById('sentimentEmoji');
const audio = document.getElementById('audio');
const detailedEmotionsDiv = document.getElementById('detailedEmotions');
const sentenceSentimentsDiv = document.getElementById('sentenceSentiments');
const ttsParamsDiv = document.getElementById('ttsParams');
let chart = null;
let emotionChart = null;

const sentimentMap = {
  positive: { label: "积极", emoji: "😃", color: "#52c41a" },
  negative: { label: "消极", emoji: "😢", color: "#f5222d" },
  neutral:  { label: "中性", emoji: "😐", color: "#faad14" }
};

// 情感表情映射
const emotionEmojiMap = {
  "喜悦": "😄", "满足": "😊", "愉快": "🙂", "兴奋": "🤩", "满意": "😌", "轻微积极": "🙂",
  "愤怒": "😡", "悲伤": "😭", "担忧": "😟", "不满": "😒", "轻微不适": "😕", "绝望": "😰", "焦虑": "😨", "困惑": "😕",
  "平静": "😌", "思考": "🤔", "客观": "😐", "冷静": "😶", "理性": "🧐"
};

// TTS样式和角色的友好显示名称
const styleNameMap = {
  "general": "普通",
  "cheerful": "愉快",
  "sad": "悲伤",
  "angry": "愤怒",
  "fearful": "恐惧",
  "disgruntled": "不满",
  "serious": "严肃",
  "calm": "平静",
  "assistant": "助手",
  "friendly": "友好",
  "unfriendly": "不友好",
  "hopeful": "希望",
  "shouting": "喊叫",
  "terrified": "恐慌",
  "whispering": "耳语",
  "customerservice": "客服",
  "chat": "聊天",
  "newscast": "新闻播报",
  "narration-professional": "专业解说",
  "empathetic": "感同身受",
  "documentary-narration": "纪录片解说",
  "gentle": "温柔",
  "affectionate": "亲切",
  "embarrassed": "尴尬",
  "soft": "柔和"
};

const roleNameMap = {
  "YoungAdultFemale": "年轻女性", 
  "YoungAdultMale": "年轻男性",
  "OlderAdultFemale": "年长女性", 
  "OlderAdultMale": "年长男性",
  "SeniorFemale": "老年女性", 
  "SeniorMale": "老年男性",
  "Girl": "女孩", 
  "Boy": "男孩"
};

// 语音模型友好名称映射
const voiceNameMap = {
  // 中文语音模型
  "zh-CN-XiaoxiaoNeural": "晓晓 (年轻女声)",
  "zh-CN-XiaoyiNeural": "晓伊 (温柔女声)",
  "zh-CN-XiaomoNeural": "晓墨 (成熟女声)",
  "zh-CN-XiaoruiNeural": "晓睿 (专业女声)",
  "zh-CN-XiaohanNeural": "晓涵 (活泼女声)",
  "zh-CN-XiaoxuanNeural": "晓萱 (温柔女声)",
  "zh-CN-YunxiNeural": "云希 (年轻男声)",
  "zh-CN-YunyangNeural": "云扬 (成熟男声)",
  "zh-CN-YunyeNeural": "云野 (深沉男声)",
  "zh-CN-YunjianNeural": "云健 (稳重男声)",
  
  // 英文语音模型
  "en-US-AriaNeural": "Aria (自然女声)",
  "en-US-JennyNeural": "Jenny (友好女声)",
  "en-US-EmmaNeural": "Emma (专业女声)",
  "en-US-SaraNeural": "Sara (助手女声)",
  "en-US-MichelleNeural": "Michelle (温暖女声)",
  "en-US-GuyNeural": "Guy (自然男声)",
  "en-US-DavisNeural": "Davis (活力男声)",
  "en-US-TonyNeural": "Tony (成熟男声)",
  "en-US-BrianNeural": "Brian (友好男声)",
  "en-US-RogerNeural": "Roger (深沉男声)"
};

// 新增：复制TTS参数到剪贴板
function copyTTSParams(params) {
  const text = JSON.stringify(params, null, 2);
  navigator.clipboard.writeText(text).then(() => {
    alert("TTS参数已复制到剪贴板！");
  });
}

// 渲染TTS参数区块
function renderTTSParams(ttsParams) {
  if (!ttsParams) {
    ttsParamsDiv.innerHTML = '<b>本次AI推荐朗读参数：</b><div class="tts-params-grid"><div class="tts-param">-</div></div>';
    return;
  }
  let html = '<b>本次AI推荐朗读参数：</b>';
  html += '<button id="copyTTSBtn" class="copy-btn">复制参数</button>';
  html += '<div class="tts-params-grid">';
  const voiceInfo = ttsParams.voice_info || {};
  // voice
  html += `<div class="tts-param"><div class="param-label">语音模型</div><div class="param-value">${voiceNameMap[ttsParams.voice] || ttsParams.voice} <span class="param-id">(${ttsParams.voice})</span></div>${voiceInfo.description ? `<div class="param-desc">${voiceInfo.description}</div>` : ''}</div>`;
  // style
  html += `<div class="tts-param"><div class="param-label">语音风格</div><div class="param-value">${styleNameMap[ttsParams.style] || ttsParams.style} <span class="param-id">(${ttsParams.style})</span></div></div>`;
  // role
  if (ttsParams.role) {
    html += `<div class="tts-param"><div class="param-label">角色</div><div class="param-value">${roleNameMap[ttsParams.role] || ttsParams.role} <span class="param-id">(${ttsParams.role})</span></div></div>`;
  }
  // rate
  html += `<div class="tts-param"><div class="param-label">语速调整</div><div class="param-value">${ttsParams.rate}</div></div>`;
  // pitch
  html += `<div class="tts-param"><div class="param-label">音调调整</div><div class="param-value">${ttsParams.pitch}</div></div>`;
  // styledegree
  html += `<div class="tts-param"><div class="param-label">风格强度</div><div class="param-value"><div class="styledegree-bar"><div class="styledegree-inner" style="width:${Math.min(100, Math.round(parseFloat(ttsParams.styledegree)*50))}%"></div></div>${ttsParams.styledegree}</div></div>`;
  html += '</div>';
  ttsParamsDiv.innerHTML = html;
  // 绑定复制按钮
  document.getElementById('copyTTSBtn').onclick = () => copyTTSParams(ttsParams);
}

analyzeBtn.onclick = async function() {
  const text = textArea.value.trim();
  if (!text) {
    alert("请输入文本！");
    return;
  }
  resultDiv.style.display = "none";
  audio.style.display = "none";
  loadingDiv.style.display = "block";
  loadingDiv.innerText = "分析中...";

  // 1. 情感分析
  let emotion;
  try {
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    emotion = await res.json();
  } catch (e) {
    loadingDiv.innerText = "情感分析失败，请检查后端服务";
    return;
  }

  // 2. 展示主情感
  loadingDiv.style.display = "none";
  resultDiv.style.display = "block";
  const s = sentimentMap[emotion.overall_sentiment] || sentimentMap.neutral;
  const intensity = emotion.intensity_analysis?.overall_intensity || emotion.emotion_intensity || 50;
  sentimentLabel.innerText = `主情感：${s.label} (强度: ${intensity}%)`;
  sentimentEmoji.innerText = s.emoji;
  
  // 根据情感强度改变emoji的大小
  const emojiSize = Math.max(40, Math.min(80, 40 + intensity/2)); // 40px-80px
  sentimentEmoji.style.fontSize = `${emojiSize}px`;

  // 3. 展示置信度环形图
  const conf = emotion.confidence_scores || { positive: 0, negative: 0, neutral: 0 };
  if (chart) chart.destroy();
  chart = new Chart(document.getElementById('confidenceChart'), {
    type: 'doughnut',
    data: {
      labels: ['积极', '消极', '中性'],
      datasets: [{
        data: [conf.positive, conf.negative, conf.neutral],
        backgroundColor: ['#52c41a', '#f5222d', '#faad14'],
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        legend: { display: true, position: 'bottom' },
        tooltip: {
          callbacks: {
            label: function(context) {
              const value = context.raw;
              return `${context.label}: ${(value * 100).toFixed(1)}%`;
            }
          }
        }
      },
      cutout: '65%',
      animation: { animateRotate: true, duration: 900 }
    }
  });

  // 4. 展示详细情感（如有）
  detailedEmotionsDiv.innerHTML = '';
  if (emotion.detailed_emotions && Object.keys(emotion.detailed_emotions).length > 0) {
    detailedEmotionsDiv.innerHTML = '<b>详细情感分析：</b><div class="emotion-grid"></div>';
    
    // 创建情感条形图
    const emotionData = Object.entries(emotion.detailed_emotions)
      .sort((a, b) => b[1] - a[1]);
      
    // 创建情感可视化卡片
    const emotionGrid = detailedEmotionsDiv.querySelector('.emotion-grid');
    emotionData.forEach(([emotion, value]) => {
      const emoji = emotionEmojiMap[emotion] || '😶';
      const percentage = Math.round(value * 100);
      const card = document.createElement('div');
      card.className = 'emotion-card';
      
      // 根据情感强度调整卡片样式
      if (percentage > 70) {
        card.classList.add('strong-emotion');
      } else if (percentage > 40) {
        card.classList.add('medium-emotion');
      }
      
      card.innerHTML = `
        <div class="emotion-emoji">${emoji}</div>
        <div class="emotion-info">
          <div class="emotion-name">${emotion}</div>
          <div class="emotion-bar-container">
            <div class="emotion-bar" style="width: ${percentage}%"></div>
          </div>
          <div class="emotion-percentage">${percentage}%</div>
        </div>
      `;
      emotionGrid.appendChild(card);
    });
  }

  // 5. 展示情感强度分析
  if (emotion.intensity_analysis) {
    const intensityDiv = document.createElement('div');
    intensityDiv.className = 'section';
    intensityDiv.innerHTML = `
      <b>情感强度分析：</b>
      <div class="intensity-grid">
        <div class="intensity-item">
          <span class="intensity-label">整体强度</span>
          <span class="intensity-value">${emotion.intensity_analysis.overall_intensity}%</span>
        </div>
        <div class="intensity-item">
          <span class="intensity-label">波动性</span>
          <span class="intensity-value">${emotion.intensity_analysis.volatility}%</span>
        </div>
        <div class="intensity-item">
          <span class="intensity-label">确定性</span>
          <span class="intensity-value">${emotion.intensity_analysis.certainty}%</span>
        </div>
        <div class="intensity-item">
          <span class="intensity-label">复杂度</span>
          <span class="intensity-value">${emotion.intensity_analysis.complexity}%</span>
        </div>
        <div class="intensity-item">
          <span class="intensity-label">主导情感</span>
          <span class="intensity-value">${emotion.intensity_analysis.dominant_emotion}</span>
        </div>
      </div>
    `;
    resultDiv.insertBefore(intensityDiv, sentenceSentimentsDiv);
  }

  // 6. 展示文本特征
  if (emotion.text_features) {
    const featuresDiv = document.createElement('div');
    featuresDiv.className = 'section';
    featuresDiv.innerHTML = `
      <b>文本特征：</b>
      <div class="features-grid">
        <div class="feature-item">
          <span class="feature-label">文本长度</span>
          <span class="feature-value">${emotion.text_features.length} 字符</span>
        </div>
        <div class="feature-item">
          <span class="feature-label">句子数量</span>
          <span class="feature-value">${emotion.text_features.sentence_count} 句</span>
        </div>
        <div class="feature-item">
          <span class="feature-label">感叹号</span>
          <span class="feature-value">${emotion.text_features.has_exclamation ? '有' : '无'}</span>
        </div>
        <div class="feature-item">
          <span class="feature-label">问号</span>
          <span class="feature-value">${emotion.text_features.has_question ? '有' : '无'}</span>
        </div>
        <div class="feature-item">
          <span class="feature-label">省略号</span>
          <span class="feature-value">${emotion.text_features.has_ellipsis ? '有' : '无'}</span>
        </div>
        <div class="feature-item">
          <span class="feature-label">大写比例</span>
          <span class="feature-value">${(emotion.text_features.capitalization_ratio * 100).toFixed(1)}%</span>
        </div>
      </div>
    `;
    resultDiv.insertBefore(featuresDiv, sentenceSentimentsDiv);
  }

  // 7. 展示情感关键词
  if (emotion.sentiment_keywords && emotion.sentiment_keywords.length > 0) {
    const keywordsDiv = document.createElement('div');
    keywordsDiv.className = 'section';
    keywordsDiv.innerHTML = `
      <b>情感关键词：</b>
      <div class="keywords-grid">
        ${emotion.sentiment_keywords.map(keyword => `
          <div class="keyword-item ${keyword.sentiment}">
            <span class="keyword-text">${keyword.word}</span>
            <span class="keyword-sentiment">${keyword.sentiment}</span>
            <span class="keyword-confidence">${(keyword.confidence * 100).toFixed(0)}%</span>
            ${keyword.is_negated ? '<span class="keyword-negated">否定</span>' : ''}
          </div>
        `).join('')}
      </div>
    `;
    resultDiv.insertBefore(keywordsDiv, sentenceSentimentsDiv);
  }

  // 8. 展示观点挖掘数据
  if (emotion.opinion_mining && (emotion.opinion_mining.aspects.length > 0 || emotion.opinion_mining.opinions.length > 0)) {
    const opinionDiv = document.createElement('div');
    opinionDiv.className = 'section';
    
    let opinionHtml = '<b>观点挖掘：</b>';
    
    if (emotion.opinion_mining.aspects.length > 0) {
      opinionHtml += '<div class="opinion-section"><h4>情感对象：</h4><div class="aspects-grid">';
      emotion.opinion_mining.aspects.forEach(aspect => {
        const confidence = (aspect.confidence_scores[aspect.sentiment] * 100).toFixed(0);
        opinionHtml += `
          <div class="aspect-item ${aspect.sentiment}">
            <span class="aspect-text">${aspect.text}</span>
            <span class="aspect-sentiment">${aspect.sentiment}</span>
            <span class="aspect-confidence">${confidence}%</span>
            ${aspect.is_negated ? '<span class="aspect-negated">否定</span>' : ''}
          </div>
        `;
      });
      opinionHtml += '</div></div>';
    }
    
    if (emotion.opinion_mining.opinions.length > 0) {
      opinionHtml += '<div class="opinion-section"><h4>具体观点：</h4><div class="opinions-grid">';
      emotion.opinion_mining.opinions.forEach(opinion => {
        const confidence = (opinion.confidence_scores[opinion.sentiment] * 100).toFixed(0);
        opinionHtml += `
          <div class="opinion-item ${opinion.sentiment}">
            <span class="opinion-text">${opinion.text}</span>
            <span class="opinion-sentiment">${opinion.sentiment}</span>
            <span class="opinion-confidence">${confidence}%</span>
            <span class="opinion-aspect">关于: ${opinion.related_aspect}</span>
            ${opinion.is_negated ? '<span class="opinion-negated">否定</span>' : ''}
          </div>
        `;
      });
      opinionHtml += '</div></div>';
    }
    
    opinionDiv.innerHTML = opinionHtml;
    resultDiv.insertBefore(opinionDiv, sentenceSentimentsDiv);
  }

  // 9. 展示句子级情感
  sentenceSentimentsDiv.innerHTML = '';
  if (emotion.sentence_sentiments && emotion.sentence_sentiments.length > 0) {
    sentenceSentimentsDiv.innerHTML = '<b>句子级情感分析：</b><ul>';
    
    emotion.sentence_sentiments.forEach(sen => {
      const ss = sentimentMap[sen.sentiment] || sentimentMap.neutral;
      const dominantEmotion = Object.entries(sen.confidence_scores)
        .sort((a, b) => b[1] - a[1])[0];
      const percentage = Math.round(dominantEmotion[1] * 100);
      
      const sentenceItem = document.createElement('li');
      sentenceItem.innerHTML = `
        <div class="sentence-item">
          <span class="sentence-sentiment" style="color:${ss.color}">
            ${ss.label} (${percentage}%)
          </span>
          <div class="sentence-bar-container">
            <div class="sentence-bar positive" style="width:${sen.confidence_scores.positive * 100}%"></div>
            <div class="sentence-bar negative" style="width:${sen.confidence_scores.negative * 100}%"></div>
            <div class="sentence-bar neutral" style="width:${sen.confidence_scores.neutral * 100}%"></div>
          </div>
          <div class="sentence-text">${sen.text}</div>
        </div>
      `;
      sentenceSentimentsDiv.querySelector('ul').appendChild(sentenceItem);
    });
    
    sentenceSentimentsDiv.innerHTML += '</ul>';
  }

  // 7. 展示TTS参数
  renderTTSParams(emotion.tts_params);

  // 10. 语音合成
  if (emotion.tts_params) {
    try {
      const ttsRes = await fetch(`${API_URL}/tts`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          ...emotion.tts_params
        })
      });
      
      if (ttsRes.ok) {
        const audioBlob = await ttsRes.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        audio.src = audioUrl;
        audio.style.display = "block";
      } else {
        const errText = await ttsRes.text();
        alert("TTS合成失败！\n" + errText);
        console.error("TTS failed:", ttsRes.status, errText);
      }
    } catch (e) {
      console.error("TTS error:", e);
    }
  }
}; 