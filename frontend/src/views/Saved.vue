<template>
  <div class="saved-page">
    <button @click="$router.push('/')" class="back-btn">⬅️ Trang chủ</button>
    <h1>📚 Từ đã lưu</h1>
    <div v-if="loading" class="loading">Đang tải...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!loading && savedWords.length === 0" class="empty">Chưa có từ nào được lưu.</div>
    <div v-for="item in savedWords" :key="item.id" class="saved-card">
      <div class="word">{{ item.word }}</div>
      <div class="note" v-if="item.note">Ghi chú: {{ item.note }}</div>
      <button class="delete-btn" @click="deleteWord(item.id)">Xoá</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      savedWords: [],
      loading: false,
      error: "",
      userId: 1, // tuỳ chỉnh theo hệ thống đăng nhập của bạn
    };
  },
  mounted() {
    this.fetchSaved();
  },
  methods: {
    async fetchSaved() {
      this.loading = true;
      this.error = "";
      try {
        const userId = localStorage.getItem("user_id");
        if (!userId) {
          alert("Bạn cần đăng nhập lại!");
          return;
        }
        const res = await fetch(`http://localhost:8000/api/saved_words?user_id=${userId}`);
        if (!res.ok) throw new Error("Không tải được danh sách.");
        this.savedWords = await res.json();
      } catch (e) {
        this.error = e.message;
      } finally {
        this.loading = false;
      }
    },
    async deleteWord(id) {
      if (!confirm("Bạn chắc chắn muốn xoá?")) return;
      try {
        const res = await fetch(`http://localhost:8000/api/saved_word/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error("Xoá thất bại.");
        this.fetchSaved();
      } catch (e) {
        this.error = e.message;
      }
    }
  }
};
</script>

<style scoped>
.saved-page {
  background: #1a1a2e;
  min-height: 100vh;
  color: #fff;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.back-btn {
  background: #ffd166;
  color: #23234b;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: bold;
  margin-bottom: 24px;
  cursor: pointer;
}
h1 {
  color: #ffd166;
  margin-bottom: 24px;
}
.saved-card {
  background: #23234b;
  border-radius: 16px;
  padding: 18px 24px;
  margin-bottom: 18px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.word {
  font-size: 22px;
  color: #4fc3f7;
  font-weight: bold;
}
.note {
  color: #ffd166;
  margin: 8px 0;
}
.delete-btn {
  background: #ef476f;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;
}
.loading, .error, .empty {
  margin: 18px 0;
  font-size: 17px;
}
.error { color: #ef476f; }
.empty { color: #ffd166; }
</style>