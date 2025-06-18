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
  "喜悦": "😄", "满足": "😊", "愉快": "🙂",
  "愤怒": "😡", "悲伤": "😭", "担忧": "😟", 
  "不满": "😒", "轻微不适": "😕",
  "平静": "😌", "思考": "🤔"
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
  "documentary-narration": "纪录片解说"
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
  sentimentLabel.innerText = `主情感：${s.label} (强度: ${emotion.emotion_intensity || 0}%)`;
  sentimentEmoji.innerText = s.emoji;
  
  // 根据情感强度改变emoji的大小
  const intensity = emotion.emotion_intensity || 50;
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

  // 5. 展示句子级情感
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

  // 6. 展示TTS参数
  ttsParamsDiv.innerHTML = '';
  if (emotion.tts_params) {
    const params = emotion.tts_params;
    
    // 获取友好名称
    const styleName = styleNameMap[params.style] || params.style;
    const roleName = params.role ? (roleNameMap[params.role] || params.role) : "无";
    
    // 创建可视化的TTS参数面板
    ttsParamsDiv.innerHTML = `
      <b>语音合成参数：</b>
      <div class="tts-params-grid">
        <div class="tts-param">
          <span class="param-label">语音:</span> 
          <span class="param-value">${params.voice}</span>
        </div>
        <div class="tts-param">
          <span class="param-label">风格:</span> 
          <span class="param-value">${styleName} (${params.style})</span>
        </div>
        <div class="tts-param">
          <span class="param-label">风格强度:</span> 
          <span class="param-value">${params.styledegree || "1.0"}</span>
        </div>
        <div class="tts-param">
          <span class="param-label">角色:</span> 
          <span class="param-value">${roleName}</span>
        </div>
        <div class="tts-param">
          <span class="param-label">语速:</span> 
          <span class="param-value">${params.rate}</span>
        </div>
        <div class="tts-param">
          <span class="param-label">音调:</span> 
          <span class="param-value">${params.pitch}</span>
        </div>
      </div>
    `;
  }

  // 7. 合成语音
  loadingDiv.style.display = "block";
  loadingDiv.innerText = "正在合成语音...";
  try {
    const ttsRes = await fetch(`${API_URL}/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        voice: emotion.tts_params.voice,
        style: emotion.tts_params.style,
        rate: emotion.tts_params.rate,
        pitch: emotion.tts_params.pitch,
        role: emotion.tts_params.role,
        styledegree: emotion.tts_params.styledegree
      })
    });
    if (!ttsRes.ok) throw new Error("TTS error");
    const audioBlob = await ttsRes.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    audio.src = audioUrl;
    audio.style.display = "";
    audio.play();
    loadingDiv.style.display = "none";
  } catch (e) {
    loadingDiv.innerText = "语音合成失败，请检查后端服务";
  }
}; 