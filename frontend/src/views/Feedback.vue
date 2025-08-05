<template>
  <div class="feedback-listening-page">
    <div class="content-wrapper">
      <div class="back-btn-row">
        <button @click="$router.push('/home')" class="main-btn back-btn">⬅️ Về trang chủ</button>
      </div>
      <div class="card">
        <h1 class="title">📝 Góp ý & Phản hồi</h1>
        <form @submit.prevent="submitFeedback">
          <div class="input-row">
            <textarea
              v-model="feedback"
              placeholder="Nhập góp ý hoặc phản hồi của bạn..."
              required
              class="input-box"
              @keydown.enter.exact.prevent="submitFeedback"
            ></textarea>
          </div>
          <div class="btn-group bottom-group">
            <button type="submit" class="main-btn">Gửi phản hồi</button>
          </div>
          <div v-if="message" class="result feedback-message">{{ message }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Feedback",
  data() {
    return {
      feedback: "",
      message: ""
    };
  },
  methods: {
    async submitFeedback() {
      if (!this.feedback.trim()) return;
      // Ưu tiên lấy từ Vuex, nếu không có thì lấy từ localStorage
      let username = this.$store?.state?.user?.username;
      if (!username) {
        username =
          sessionStorage.getItem("sessionUser") ||
          localStorage.getItem("username") ||
          "Ẩn danh";
      }
      try {
        await fetch("http://localhost:8000/api/feedback_discord", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content: this.feedback,
            user: username
          })
        });
        this.message = "Cảm ơn bạn đã gửi phản hồi!";
        this.feedback = "";
      } catch (e) {
        this.message = "Có lỗi khi gửi phản hồi. Vui lòng thử lại!";
      }
    },
    send_feedback_to_discord(content, user) {
      console.log("Gửi feedback tới Discord:", content);
      if (!DISCORD_WEBHOOK_URL) {
        console.log("Không tìm thấy webhook URL");
        return;
      }
      const message = `**Feedback từ ${user}:**\n${content}`;
      fetch(DISCORD_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: message })
      })
        .then(resp => console.log("Discord response:", resp.status, resp.statusText))
        .catch(err => console.error("Error sending to Discord:", err));
    }
  },
  computed: {
    username() {
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      return user.username || "Ẩn danh";
    }
  }
};
</script>

<style scoped>
.feedback-listening-page {
  background: linear-gradient(135deg, #393953 0%, #293453 100%);  min-height: 100vh;
  padding: 40px 0;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.content-wrapper {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  position: relative;
  min-height: 600px;
}
.back-btn-row {
  width: 100%;
  max-width: 480px;
  display: flex;
  justify-content: flex-start;
  margin: 0 auto 32px auto;
}
.back-btn {
  min-width: 160px;
}
.card {
  background: #23234b;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 36px 32px 32px 32px;
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  font-size: 32px;
  font-weight: bold;
  color: #ffd166;
  margin: 0 0 32px 0;
  text-align: center;
}
.input-row {
  width: 100%;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.input-box {
  width: 100%;
  min-height: 140px;      /* tăng chiều cao tối thiểu */
  border-radius: 10px;
  border: 1.5px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  font-size: 18px;        /* tăng cỡ chữ */
  padding: 18px 16px;     /* tăng padding */
  resize: vertical;
  box-sizing: border-box;
  outline: none;
  transition: border 0.2s;
}
.input-box:focus {
  border: 2px solid #ffd166;
}
.btn-group.bottom-group {
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 0;
}
.main-btn {
  padding: 10px 24px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
  min-width: 130px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(76,195,247,0.08);
  transition: background 0.2s, transform 0.2s;
}
.main-btn:hover {
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
  transform: translateY(-2px) scale(1.04);
}
.result.feedback-message {
  margin-top: 18px;
  font-weight: bold;
  font-size: 19px;
  text-align: center;
  min-height: 32px;
  color: #06d6a0;
}
</style>