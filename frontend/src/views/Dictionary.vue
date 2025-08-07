<template>
  <div class="dictionary-page">
    <button @click="goHome" class="back-btn">⬅ Back to Homepage</button>
    <h1>Tra cứu từ điển</h1>
    <div class="search-row">
      <input
        v-model="searchWord"
        @keydown.enter="lookup"
        placeholder="Nhập từ khoá vào đây..."
        class="input-box"
      />
      <button @click="lookup" class="main-btn">Tra cứu</button>
    </div>
    <div v-if="loading" class="loading">Đang tra cứu...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="result" class="result-block">
      <div v-if="successMessage" class="success-msg">
        {{ successMessage }},
        <span class="go_saved" @click="goSaved">Nhấn để xem</span>
      </div>

      <div class="word-row">
        <h2
          @click="speakWord"
          style="cursor: pointer"
          title="Click để nghe phát âm"
        >
          {{ result.word }}
        </h2>
        <button
          class="heart-btn"
          :class="{ saved: isSaved }"
          @click="toggleSaveWord"
          :title="isSaved ? 'Đã lưu' : 'Lưu từ này'"
        >
          <svg viewBox="0 0 24 24" width="38" height="38">
            <path
              :fill="isSaved ? '#ef476f' : '#232323'"
              d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
            />
          </svg>
        </button>
      </div>
      <div v-if="result.phonetic" class="phonetic">
        / {{ result.phonetic }} /
      </div>
      <div v-if="quickVi" class="vi-meaning">
        <span style="color: #ffd166; font-weight: bold">Nghĩa: </span>
        <span style="color: #fff">{{ quickVi }}</span>
      </div>
      <div
        v-for="(meaning, idx) in result.meanings"
        :key="idx"
        class="meaning-block"
      >
        <div class="part-of-speech">
          {{ getPartOfSpeechVi(meaning.partOfSpeech) }}
        </div>
        <ul>
          <li v-for="(def, i) in meaning.definitions" :key="i">
            <span style="color: #ffd166">{{ viMeanings[idx]?.[i] }}</span>
            <span v-if="def.example" class="example"
              >VD: "{{ def.example }}"</span
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchWord: "",
      result: null,
      loading: false,
      error: "",
      viMeanings: [], // mỗi phần tử là mảng nghĩa tiếng Việt cho 1 meaning
      quickVi: "", // từ gốc tiếng Việt để hiển thị nghĩa nhanh
      translatedSynonyms: [],
      translatedAntonyms: [],
      isSaved: false,
    };
  },
  methods: {
    goHome() {
      this.$router.push("/home");
    },
    goSaved() {
      this.$router.push("/saved");
    },
    async lookup() {
      if (!this.searchWord.trim()) return;
      this.loading = true;
      this.error = "";
      this.result = null;
      this.viMeanings = [];
      this.quickVi = "";
      try {
        let wordToLookup = this.searchWord.trim();
        // Kiểm tra nếu là tiếng Việt thì dịch sang tiếng Anh
        const isVietnamese =
          /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/i.test(
            wordToLookup
          );
        if (isVietnamese) {
          // Dịch sang tiếng Anh bằng Google Translate
          const res = await fetch(
            `https://translate.googleapis.com/translate_a/single?client=gtx&sl=vi&tl=en&dt=t&q=${encodeURIComponent(
              wordToLookup
            )}`
          );
          const data = await res.json();
          wordToLookup =
            data[0]?.map((item) => item[0]).join("") || wordToLookup;
          this.quickVi = this.searchWord.trim(); // giữ lại từ gốc tiếng Việt
        } else {
          // Nếu là tiếng Anh, dịch nghĩa nhanh sang tiếng Việt
          const viRes = await fetch(
            `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=${encodeURIComponent(
              wordToLookup
            )}`
          );
          const viData = await viRes.json();
          this.quickVi = viData[0]?.map((item) => item[0]).join("") || "";
        }

        // 2. Tra cứu sâu bằng dictionaryapi.dev
        const dictRes = await fetch(
          `https://api.dictionaryapi.dev/api/v2/entries/en/${wordToLookup}`
        );
        if (!dictRes.ok) throw new Error("Không tìm thấy từ này!");
        const dictData = await dictRes.json();
        this.result = dictData[0];

        // 3. Dịch từng nghĩa sâu sang tiếng Việt (giống cũ)
        const meanings = this.result.meanings || [];
        this.viMeanings = meanings.map((m) =>
          (m.definitions || []).map((def) => def.definition || "")
        );

        // Luôn dịch từng nghĩa chi tiết sang tiếng Việt (kể cả khi nhập tiếng Việt)
        meanings.forEach((meaning, idx) => {
          (meaning.definitions || []).forEach(async (def, i) => {
            if (def.definition) {
              // Luôn dịch sang tiếng Việt
              const vi = await this.translateToVietnamese(def.definition);
              const arr = [...this.viMeanings[idx]];
              arr[i] = vi;
              this.viMeanings[idx] = arr;
            }
          });
        });
      } catch (e) {
        this.error = e.message || "Lỗi khi tra cứu!";
      } finally {
        this.loading = false;
      }
    },
    async translateToVietnamese(text) {
      try {
        const res = await fetch(
          `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=${encodeURIComponent(
            text
          )}`
        );
        const data = await res.json();
        return data[0]?.map((item) => item[0]).join("") || "";
      } catch (e) {
        return "";
      }
    },
    speakWord() {
      if (!this.result || !this.result.word) return;
      const utter = new window.SpeechSynthesisUtterance(this.result.word);
      utter.lang = "en-US";
      window.speechSynthesis.speak(utter);
    },
    getPartOfSpeechVi(pos) {
      const map = {
        noun: "Danh từ",
        verb: "Động từ",
        adjective: "Tính từ",
        adverb: "Trạng từ",
        pronoun: "Đại từ",
        preposition: "Giới từ",
        conjunction: "Liên từ",
        interjection: "Thán từ",
        determiner: "Từ hạn định",
        exclamation: "Cảm thán",
        article: "Mạo từ",
        modal: "Động từ khuyết thiếu",
      };
      return map[pos?.toLowerCase()] || pos;
    },
    async toggleSaveWord() {
      const userId = Number(localStorage.getItem("user_id"));
      if (!userId || !this.result?.word) return;

      if (this.isSaved) {
        // Tìm id của từ đã lưu để xoá
        try {
          const res = await fetch(
            `http://localhost:8000/api/saved_words?user_id=${userId}`
          );
          if (!res.ok) return;
          const words = await res.json();
          const saved = words.find(
            (w) => w.word?.toLowerCase() === this.result.word.toLowerCase()
          );
          if (saved) {
            await fetch(`http://localhost:8000/api/saved_word/${saved.id}`, {
              method: "DELETE",
            });
            this.isSaved = false;
          }
        } catch (e) {
          alert("Huỷ lưu thất bại!");
        }
        return;
      }
      await this.saveWord();
      this.isSaved = true;
    },
    async saveWord() {
      if (!this.result || !this.result.word) return;
      const userId = Number(localStorage.getItem("user_id"));
      if (!userId) {
        alert("Bạn cần đăng nhập lại!");
        return;
      }
      try {
        await fetch("http://localhost:8000/api/save_word", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: userId,
            word: this.result.word,
            meaning: this.quickVi,
            phonetic: this.result.phonetic || "",
            note: "",
          }),
        });
        this.successMessage = `✅ Đã lưu từ "${this.result.word}" thành công!`;
        setTimeout(() => {
          this.successMessage = "";
        }, 3000); // Ẩn sau 3s
      } catch (e) {
        alert(e.message);
      }
    },
    async checkSaved() {
      // Gọi API lấy danh sách từ đã lưu của user, kiểm tra từ hiện tại đã lưu chưa
      const userId = Number(localStorage.getItem("user_id"));
      if (!userId || !this.result?.word) {
        this.isSaved = false;
        return;
      }
      try {
        const res = await fetch(
          `http://localhost:8000/api/saved_words?user_id=${userId}`
        );
        if (!res.ok) return;
        const words = await res.json();
        this.isSaved = words.some(
          (w) => w.word?.toLowerCase() === this.result.word.toLowerCase()
        );
      } catch {
        this.isSaved = false;
      }
    },
  },
  watch: {
    result() {
      this.checkSaved();
    },
  },
};
</script>

<style scoped>
.dictionary-page {
  background-image: url("../assets/images/background.jpg");
  background-size: cover;
  background-position: center;
  color: #fff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.back-btn {
  background: rgba(255, 255, 255, 0.1);
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
.back-btn:hover {
  background: #97b368;
  color: #fff;
}

h1 {
  margin-bottom: 28px;
  color: #454545;
  font-size: 28px;
  text-align: center;
  font-weight: bold;
}

.search-row {
  display: flex;
  gap: 14px;
  margin-bottom: 28px;
  justify-content: center;
  width: 100%;
  max-width: 500px;
}

.input-box {
  padding: 12px;
  font-size: 17px;
  border-radius: 10px;
  border: 1.5px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  outline: none;
  width: 260px;
  transition: border 0.2s;
}
.input-box:focus {
  border: 2px solid #454545;
}

.main-btn {
  padding: 10px 24px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #97b368, #b6cf75);
  color: #363636;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  font-size: 16px;
}
.main-btn:hover {
  transform: translateY(-2px);
  background: linear-gradient(90deg, #adc682, #cce295);
}

.loading {
  color: #454545;
  margin-bottom: 12px;
  font-weight: bold;
  font-size: 16px;
}

.error {
  color: #ef476f;
  margin-bottom: 12px;
  font-weight: bold;
  font-size: 16px;
}

.result-block {
  background: #23234b;
  border-radius: 18px;
  padding: 28px 24px;
  margin-top: 18px;
  width: 100%;
  max-width: 540px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
}

.result-block h2 {
  color: #4fc3f7;
  font-size: 26px;
  margin-bottom: 8px;
  font-weight: bold;
}

.phonetic {
  color: #06d6a0;
  font-size: 19px;
  margin-bottom: 14px;
  font-family: monospace;
}

.meaning-block {
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 1px solid #333;
}

.part-of-speech {
  color: #ffd166;
  font-weight: bold;
  margin-bottom: 6px;
  font-size: 17px;
}

.meaning-block ul {
  padding-left: 18px;
  margin: 0;
}

.meaning-block li {
  margin-bottom: 6px;
  font-size: 16px;
  line-height: 1.5;
}

.example {
  color: #4fc3f7;
  margin-left: 8px;
  font-style: italic;
  font-size: 15px;
}

.vi-meaning {
  margin: 12px 0 18px 0;
  font-size: 17px;
}

.word-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.save-btn {
  margin-left: 18px;
  white-space: nowrap;
}

.heart-btn {
  background: none;
  border: 2.5px solid #ffd166;
  border-radius: 50%;
  cursor: pointer;
  padding: 6px;
  margin-left: 18px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 54px;
  width: 54px;
  box-sizing: border-box;
}
.heart-btn.saved {
  border-color: #ef476f;
  box-shadow: 0 0 6px #ef476f55;
}
.heart-btn svg {
  display: block;
  margin: auto;
}
.heart-btn svg {
  transition: fill 0.2s;
}
.heart-btn.saved svg path {
  fill: #ef476f !important;
}
.heart-btn:not(.saved):hover svg path {
  fill: #888 !important;
  transition: fill 0.2s;
}

.word-row h2 {
  margin: 0;
  line-height: 1;
  display: flex;
  align-items: center;
}

.success-msg {
  background: #06d6a0;
  color: #fff;
  font-weight: bold;
  padding: 10px 14px;
  border-radius: 8px;
  margin: 10px 0;
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.go_saved {
  text-align: right;
  color: #fffefd;
}
.go_saved:hover {
  text-decoration: underline;
  cursor: pointer;
  color:red
}
</style>
