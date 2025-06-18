const API_URL = "http://localhost:8000/api"; // 如部署到服务器请改为实际后端地址

const analyzeBtn = document.getElementById('analyzeBtn');
const textArea = document.getElementById('text');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const sentimentLabel = document.getElementById('sentimentLabel');
const sentimentEmoji = document.getElementById('sentimentEmoji');
const audio = document.getElementById('audio');
let chart = null;

const sentimentMap = {
  positive: { label: "积极", emoji: "😃", color: "#52c41a" },
  negative: { label: "消极", emoji: "😢", color: "#f5222d" },
  neutral:  { label: "中性", emoji: "😐", color: "#faad14" }
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

  // 2. 展示情感结果
  loadingDiv.style.display = "none";
  resultDiv.style.display = "block";
  const s = sentimentMap[emotion.sentiment] || sentimentMap.neutral;
  sentimentLabel.innerText = `情感：${s.label}`;
  sentimentEmoji.innerText = s.emoji;

  // 3. 展示置信度饼图
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
        legend: { display: true, position: 'bottom' }
      },
      cutout: '65%',
      animation: { animateRotate: true, duration: 900 }
    }
  });

  // 4. 动态参数
  let speed = 1.0, volume = '+0dB', pitch = 'default';
  if (emotion.sentiment === 'positive') { speed = 1.15; volume = '+2dB'; pitch = '+2st'; }
  else if (emotion.sentiment === 'negative') { speed = 0.9; volume = '-2dB'; pitch = '-2st'; }

  // 5. 合成语音
  loadingDiv.style.display = "block";
  loadingDiv.innerText = "正在合成语音...";
  try {
    const ttsRes = await fetch(`${API_URL}/tts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, speed, volume, pitch, voice: "zh-CN-XiaoxiaoNeural" })
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