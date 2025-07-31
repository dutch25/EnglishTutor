<template>
  <div class="practice-container">
    <div class="practice-header">
      <h2>🎤 Luyện phát âm IPA</h2>
      <div class="topic-select">
        <label for="topic"><strong>Chủ đề:</strong></label>
        <select id="topic" v-model="selectedTopic" @change="changeTopic">
          <option value="">-- Tất cả --</option>
          <option v-for="t in topics" :key="t.key" :value="t.key">
            {{ t.title }}
          </option>
        </select>
      </div>
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
      <button @click="startRecording">🎙️ Ghi âm</button>
      <button @click="fetchSentences(selectedTopic)">🔄 Câu khác</button>
    </div>

    <div class="practice-status">{{ status }}</div>

    <div
      class="practice-result"
      v-if="transcriptResult"
      v-html="transcriptResult"
    ></div>
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
    await this.fetchSentences();
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
            topicMap[s.topic] = s.icon
              ? `${s.icon} ${
                  s.topic.charAt(0).toUpperCase() + s.topic.slice(1)
                }`
              : s.topic.charAt(0).toUpperCase() + s.topic.slice(1);
          }
        });
        this.topics = Object.keys(topicMap).map((key) => ({
          key,
          title: topicMap[key],
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

    changeTopic() {
      this.fetchSentences(this.selectedTopic);
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
  },
};
</script>

<style scoped>
.practice-container {
  background: #fff;
  max-width: 650px;
  margin: 40px auto;
  padding: 30px 24px;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.08);
  font-family: Arial, sans-serif;
}
.practice-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.topic-select label {
  margin-right: 8px;
}
.topic-select select {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.sentence-block {
  margin: 18px 0 10px 0;
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}
.sentence-main {
  font-size: 1.2em;
  margin-bottom: 6px;
}
.sentence-english {
  font-weight: bold;
  margin-right: 12px;
}
.sentence-ipa {
  font-family: monospace;
  color: #555;
}
.sentence-vn {
  margin-top: 6px;
  color: #444;
  font-size: 1em;
}
.practice-actions {
  margin: 18px 0;
}
.practice-actions button {
  margin: 0 8px;
  padding: 8px 18px;
  border-radius: 6px;
  border: none;
  background: #007bff;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.practice-actions button:hover {
  background: #0056b3;
}
.practice-status {
  margin: 10px 0 0 0;
  color: #007bff;
  font-weight: bold;
}
.practice-result {
  background: #f9f9f9;
  padding: 16px;
  border-radius: 8px;
  border-left: 5px solid #007bff;
  margin-top: 22px;
  text-align: left;
  font-size: 1em;
}
.result-block code {
  background: #eef6ff;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}
#feedback {
  background: #eef6ff;
  border: 1px solid #007bff;
  padding: 10px;
  border-radius: 6px;
  margin-top: 15px;
  font-style: italic;
  color: #004085;
}
</style>
