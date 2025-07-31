<template>
  <div class="whisper-page">
    <template v-if="!selectedTopic">
      <h2 class="whisper-title">🎤 Luyện phát âm IPA</h2>
      <div class="topic-grid">
        <div
          v-for="t in topics"
          :key="t.key"
          class="topic-card"
          @click="selectTopic(t.key)"
        >
          <span class="topic-icon">{{ t.icon || "🔤" }}</span>
          <span class="topic-title">{{ t.title }}</span>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="whisper-card">
        <div class="practice-header">
          <button @click="resetTopic" class="main-btn" style="margin-bottom:12px;">⬅️ Chọn chủ đề khác</button>
          <h2>Chủ đề: {{ getTopicTitle(selectedTopic) }}</h2>
        </div>
        <div class="sentence-block">
          <div class="sentence-main">
            <span class="sentence-english">{{
              currentSentenceObj.english || "Loading..."
            }}</span>
            <span
              class="sentence-ipa"
              v-html="
                `<strong>IPA:</strong> <code>${
                  currentSentenceObj.pronunciation || currentIPA
                }</code>`"
            ></span>
          </div>
          <div class="sentence-vn" v-if="currentSentenceObj.vietnamese">
            <span>🇻🇳 {{ currentSentenceObj.vietnamese }}</span>
          </div>
        </div>
        <div class="practice-actions">
          <button @click="playAudio" class="main-btn">🔊 Nghe</button>
          <button @click="startRecording" class="main-btn">🎙️ Ghi âm</button>
          <button @click="fetchSentences(selectedTopic)" class="main-btn">🔄 Câu khác</button>
        </div>
        <div class="practice-status">{{ status }}</div>
        <div
          class="practice-result"
          v-if="transcriptResult"
          v-html="transcriptResult"
        ></div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "WhisperPractice",
  data() {
    return {
      currentSentenceObj: {},
      currentIPA: "",
      selectedTopic: "",
      topics: [],
      status: "",
      transcriptResult: "",
      mediaRecorder: null,
      audioChunks: [],
    };
  },
  async mounted() {
    await this.fetchTopics();
  },
  methods: {
    async fetchTopics() {
      try {
        const res = await fetch("http://localhost:8000/api/sentences");
        const data = await res.json();
        const all = Array.isArray(data) ? data : data.sentences;
        const topicMap = {};
        all.forEach((s) => {
          if (!topicMap[s.topic]) {
            topicMap[s.topic] = {
              title: s.icon
                ? `${s.icon} ${s.topic.charAt(0).toUpperCase() + s.topic.slice(1)}`
                : s.topic.charAt(0).toUpperCase() + s.topic.slice(1),
              icon: s.icon || "🔤",
            };
          }
        });
        this.topics = Object.keys(topicMap).map((key) => ({
          key,
          title: topicMap[key].title,
          icon: topicMap[key].icon,
        }));
      } catch (e) {
        this.topics = [];
      }
    },
    async fetchSentences(topic = "") {
      try {
        let url = "http://localhost:8000/api/sentences";
        if (topic) url += `?topic=${encodeURIComponent(topic)}`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(`Lỗi HTTP ${res.status}`);
        const data = await res.json();
        const sentences = Array.isArray(data) ? data : data.sentences;
        if (!Array.isArray(sentences) || sentences.length === 0)
          throw new Error("❌ Không có câu hợp lệ");
        const randomSentence =
          sentences[Math.floor(Math.random() * sentences.length)];
        this.currentSentenceObj = randomSentence;

        if (!randomSentence.pronunciation) {
          const ipaRes = await fetch("http://localhost:8000/api/get_ipa", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: randomSentence.english }),
          });
          const ipaData = await ipaRes.json();
          this.currentIPA = ipaData.ipa || "";
        } else {
          this.currentIPA = randomSentence.pronunciation;
        }
      } catch (e) {
        this.currentSentenceObj = { english: "❌ Không tải được câu." };
        console.error(e);
      }
    },
    selectTopic(topic) {
      this.selectedTopic = topic;
      this.fetchSentences(topic);
    },
    resetTopic() {
      this.selectedTopic = "";
      this.currentSentenceObj = {};
      this.currentIPA = "";
      this.status = "";
      this.transcriptResult = "";
    },
    getTopicTitle(topicKey) {
      const found = this.topics.find(t => t.key === topicKey);
      return found ? found.title : topicKey;
    },
    async startRecording() {
      this.status = "🎙️ Đang ghi âm...";
      this.transcriptResult = "";
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        this.mediaRecorder = new MediaRecorder(stream);
        this.audioChunks = [];

        this.mediaRecorder.ondataavailable = (e) =>
          this.audioChunks.push(e.data);
        this.mediaRecorder.onstop = async () => {
          this.status = "⏳ Đang xử lý...";
          const audioBlob = new Blob(this.audioChunks, { type: "audio/webm" });
          const formData = new FormData();
          formData.append("file", audioBlob, "recording.webm");
          formData.append("original_text", this.currentSentenceObj.english);

          try {
            const res = await fetch("http://localhost:8000/api/upload/", {
              method: "POST",
              body: formData,
            });
            if (!res.ok) throw new Error(`Upload lỗi: ${res.status}`);
            const data = await res.json();

            if (!data.transcript) throw new Error("❌ Không có transcript");

            this.transcriptResult = `
              <div class="result-block">
                <div><strong>Câu mẫu đã tô màu:</strong></div>
                <div><code>${
                  data.sentence_colored ||
                  this.highlightText(this.currentSentenceObj.english)
                }</code></div>
                <div><strong>IPA bạn:</strong></div>
                <div><code>${
                  data.user_ipa_colored || "❌ Không nhận diện IPA"
                }</code></div>
                <div><strong>🎯 Điểm chính xác:</strong>
                  <span style="color:${this.getColor(data.ipa_score)}">${
              data.ipa_score
            }%</span>
                </div>
                <div id="feedback" style="margin-top:10px;color:#007bff;font-weight:bold;">⏳ Đang phân tích...</div>
              </div>
            `;
            this.status = "✅ Hoàn tất.";

            this.getFeedback(data.transcript, this.currentSentenceObj.english);
          } catch (err) {
            console.error(err);
            this.status = "❌ Upload thất bại.";
          }
        };

        this.mediaRecorder.start();
        setTimeout(() => this.mediaRecorder.stop(), 4000);
      } catch (err) {
        this.status = "❌ Không thể truy cập microphone.";
        console.error(err);
      }
    },

    async getFeedback(transcript, target) {
      try {
        const res = await fetch("http://localhost:8000/api/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ transcript, target }),
        });
        const data = await res.json();
        document.getElementById("feedback").innerText =
          data.feedback || "⚠️ Không có phản hồi.";
      } catch (err) {
        document.getElementById("feedback").innerText = "⚠️ Lỗi khi phân tích.";
      }
    },

    getColor(score) {
      if (score >= 70) return "green";
      if (score >= 30) return "orange";
      return "red";
    },

    highlightText(text) {
      return text
        .split("")
        .map(
          (c) =>
            `<span style="text-decoration:underline dotted #ccc">${c}</span>`
        )
        .join("");
    },
    playAudio() {
      if (!this.currentSentenceObj.english) return;
      const audio = new Audio(`http://127.0.0.1:8000/audio/${encodeURIComponent(this.currentSentenceObj.english)}`);
      audio.play();
    },
  },
};
</script>

<style scoped>
.whisper-page {
  background-color: #1a1a2e;
  color: #fff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Segoe UI", Arial, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.whisper-title {
  font-size: 28px;
  color: #ffd166;
  margin-bottom: 32px;
  text-align: center;
}

.topic-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 40px;
}

.topic-card {
  background-color: #23234b;
  border-radius: 16px;
  padding: 32px 0 24px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  box-shadow: 0 4px 12px rgba(255,255,255,0.05);
  font-size: 20px;
}

.topic-card:hover {
  box-shadow: 0 8px 24px rgba(255,255,255,0.12);
  transform: translateY(-6px) scale(1.03);
  background-color: #2a2a3d;
}

.topic-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.topic-title {
  font-size: 20px;
  font-weight: bold;
  color: #4fc3f7;
}

.whisper-card {
  background: #23234b;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 32px;
  width: 100%;
  max-width: 600px;
  text-align: center;
}

.practice-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 18px;
}

.sentence-block {
  margin: 18px 0 10px 0;
  padding: 16px 0;
  border-bottom: 1px solid #4fc3f7;
}

.sentence-main {
  font-size: 1.2em;
  margin-bottom: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sentence-english {
  font-weight: bold;
  color: #4fc3f7;
  margin-bottom: 8px;
  font-size: 22px;
}

.sentence-ipa {
  font-family: monospace;
  color: #06d6a0;
  margin-bottom: 6px;
  font-size: 17px;
}

.sentence-vn {
  margin-top: 6px;
  color: #ffd166;
  font-size: 18px;
}

.practice-actions {
  margin: 18px 0;
  display: flex;
  gap: 16px;
  justify-content: center;
}

.main-btn {
  padding: 10px 20px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 15px;
}

.main-btn:hover {
  transform: translateY(-2px);
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
}

.practice-status {
  margin: 10px 0 0 0;
  color: #ffd166;
  font-weight: bold;
  font-size: 16px;
}

.practice-result {
  background: #23234b;
  padding: 16px;
  border-radius: 8px;
  border-left: 5px solid #06d6a0;
  margin-top: 22px;
  text-align: left;
  font-size: 1em;
  color: #fff;
}

.result-block code {
  background: #1a1a2e;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: #ffd166;
}

#feedback {
  background: #23234b;
  border: 1px solid #4fc3f7;
  padding: 10px;
  border-radius: 6px;
  margin-top: 15px;
  font-style: italic;
  color: #4fc3f7;
}
</style>
