<template>
  <div class="whisper-page">
    <button class="back-button" @click="goHome">
    ← Quay về trang chủ
    </button>
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
          <button @click="resetTopic" class="main-btn">
            ⬅️ Chọn chủ đề khác
          </button>
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
                }</code>`
              "
            ></span>
          </div>
          <div class="sentence-vn" v-if="currentSentenceObj.vietnamese">
            <span>🇻🇳 {{ currentSentenceObj.vietnamese }}</span>
          </div>
        </div>
        <div class="practice-actions">
          <button @click="playAudio" class="main-btn">🔊 Nghe</button>
          <button @click="startRecording" class="main-btn">🎙️ Ghi âm</button>
          <button @click="fetchSentences(selectedTopic)" class="main-btn">
            🔄 Câu khác
          </button>
        </div>
        <div class="practice-status">
          <div v-if="status === '⏳ Đang xử lý...'" class="loader"></div>
          <span v-else>{{ status }}</span>
        </div>
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
              title: s.topic.charAt(0).toUpperCase() + s.topic.slice(1),
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
      const found = this.topics.find((t) => t.key === topicKey);
      return found ? found.title : topicKey;
    },
    goHome() {
      this.$router.push("/home");
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

            const highlightedSentence = this.highlightText(
              this.currentSentenceObj.english,
              data.transcript
            );

            this.transcriptResult = `
              <div class="result-block">
                <div><strong>Câu mẫu đã tô màu:</strong></div>
                <div class="big-sentence"><code>${highlightedSentence}</code></div>
                <div style="margin:8px 0 0 0;">
                  <strong>IPA bạn vừa nói:</strong>
                </div>
                <div class="big-sentence">
                  <code>${data.user_ipa_raw || "(không có)"}</code>
                </div>
                <div><strong>🎯 Điểm chính xác:</strong>
                  <span class="score-text" style="color:${this.getColor(data.ipa_score)}">${data.ipa_score}%</span>
                </div>
                <div id="feedback" style="margin-top:10px;font-weight:bold;">⏳ Đang phân tích...</div>
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
    highlightText(original, user) {
      if (!original || !user) return this.highlightFallback(original);
      const originalWords = original.toLowerCase().split(/\s+/);
      const userWords = user.toLowerCase().split(/\s+/);
      let result = [];

      for (let i = 0; i < originalWords.length; i++) {
        const origWord = originalWords[i] || "";
        const userWord = userWords[i] || "";
        let wordHtml = "";

        if (userWord === origWord) {
          wordHtml = `<span style="color:#06d6a0">${origWord}</span>`;
        } else if (
          userWord &&
          origWord &&
          this.isPartialMatch(origWord, userWord)
        ) {
          wordHtml = `<span style="color:#ffd166">${origWord}</span>`;
        } else {
          wordHtml = `<span style="color:#ef476f">${origWord}</span>`;
        }
        result.push(wordHtml);
      }
      return result.join(" ");
    },
    isPartialMatch(origWord, userWord) {
      const minLength = Math.min(origWord.length, userWord.length);
      let matches = 0;
      for (let i = 0; i < minLength; i++) {
        if (origWord[i] === userWord[i]) matches++;
      }
      return matches / origWord.length >= 0.5;
    },
    highlightFallback(text) {
      return text
        .split("")
        .map((c) => `<span style="color:#ef476f">${c}</span>`)
        .join("");
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
      if (score >= 70) return "#06d6a0";
      if (score >= 30) return "#ffd166";
      return "#ef476f";
    },
    playAudio() {
      if (!this.currentSentenceObj.english) return;
      const audio = new Audio(
        `http://127.0.0.1:8000/audio/${encodeURIComponent(
          this.currentSentenceObj.english
        )}`
      );
      audio.play();
    },
  },
};
</script>

<style scoped>
.whisper-page {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #fff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Inter", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: background 0.5s ease;
}

.whisper-title {
  font-size: 32px;
  color: #ffd166;
  margin-bottom: 40px;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.topic-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(200px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 48px;
}

.topic-card {
  background: #23234b;
  border-radius: 20px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.topic-card:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  background: #2a2a5a;
}

.topic-icon {
  font-size: 48px;
  margin-bottom: 16px;
  transition: transform 0.3s ease;
}

.topic-card:hover .topic-icon {
  transform: scale(1.2);
}

.topic-title {
  font-size: 22px;
  font-weight: 600;
  color: #4fc3f7;
}

.whisper-card {
  background: #23234b;
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
  padding: 40px;
  width: 100%;
  max-width: 700px;
  text-align: center;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.practice-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.sentence-block {
  margin: 24px 0;
  padding: 20px 0;
  border-bottom: 2px solid #4fc3f7;
}

.sentence-main {
  font-size: 1.3em;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sentence-english {
  font-weight: 700;
  color: #4fc3f7;
  margin-bottom: 10px;
  font-size: 24px;
}

.sentence-ipa {
  font-family: "Courier New", monospace;
  color: #06d6a0;
  font-size: 18px;
}

.sentence-vn {
  margin-top: 10px;
  color: #ffd166;
  font-size: 20px;
}

.practice-actions {
  margin: 24px 0;
  display: flex;
  gap: 20px;
  justify-content: center;
}

.main-btn {
  padding: 12px 24px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
}

.main-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
}

.practice-status {
  margin: 12px 0;
  color: #ffd166;
  font-weight: 600;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 35px; /* Ensure consistent height for loader */
}

.loader {
  width: 85px;
  height: 35px;
  --g1: conic-gradient(from 90deg at 3px 3px, #0000 90deg, #ffd166 0);
  --g2: conic-gradient(from -90deg at 22px 22px, #0000 90deg, #ffd166 0);
  background: var(--g1), var(--g1), var(--g1), var(--g2), var(--g2), var(--g2);
  background-size: 25px 25px;
  background-repeat: no-repeat;
  animation: l6 1s infinite alternate;
}

@keyframes l6 {
  0% {
    background-position: 0 50%, 50% 50%, 100% 50%;
  }
  20% {
    background-position: 0 0, 50% 50%, 100% 50%;
  }
  40% {
    background-position: 0 100%, 50% 0, 100% 50%;
  }
  60% {
    background-position: 0 50%, 50% 100%, 100% 0;
  }
  80% {
    background-position: 0 50%, 50% 50%, 100% 100%;
  }
  100% {
    background-position: 0 50%, 50% 50%, 100% 50%;
  }
}

.practice-result {
  background: #1a1a2e;
  padding: 20px;
  border-radius: 12px;
  border-left: 6px solid #06d6a0;
  margin-top: 24px;
  text-align: left;
  font-size: 1.1em;
  color: #fff;
}

.result-block code {
  background: #23234b;
  padding: 4px 8px;
  border-radius: 6px;
  font-family: "Courier New", monospace;
  color: #ffd166;
}

#feedback {
  background: #23234b;
  border: 2px solid #4fc3f7;
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
  font-style: italic;
  color: #4fc3f7;
}

.big-sentence {
  font-size: 22px;
  color: #4fc3f7;
  margin: 8px 0 12px 0;
  font-weight: 600;
  word-break: break-word;
}

.score-text {
  font-size: 22px;
  font-weight: 700;
  color: #06d6a0; /* hoặc #ffd166 nếu bạn thích tông vàng */
  text-shadow: 0 2px 8px #16213e;
}

.back-button {
  background-color: #ffd166;
  color: #23234b;
  font-size: 14px;
  padding: 8px 16px;
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}
.back-button:hover {
  background-color: #ef476f;
  color: #fff;
}
</style>
