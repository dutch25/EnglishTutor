<template>
  <div class="feedback-page">
    <h1>Góp ý & Phản hồi</h1>
    <form @submit.prevent="submitFeedback">
      <textarea v-model="feedback" placeholder="Nhập góp ý hoặc phản hồi của bạn..." required></textarea>
      <button type="submit" class="main-btn">Gửi phản hồi</button>
      <div v-if="message" class="feedback-message">{{ message }}</div>
    </form>
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
    submitFeedback() {
      // Ở đây bạn có thể gửi feedback lên server nếu muốn
      this.message = "Cảm ơn bạn đã gửi phản hồi!";
      this.feedback = "";
    }
  }
};
</script>

<style scoped>
.feedback-page {
  max-width: 480px;
  margin: 60px auto 0 auto;
  background: #23234b;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 36px 32px 32px 32px;
  color: #ffd166;
  text-align: center;
}
.feedback-page h1 {
  color: #ffd166;
  margin-bottom: 24px;
}
textarea {
  width: 100%;
  min-height: 100px;
  border-radius: 10px;
  border: 1px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  font-size: 16px;
  padding: 12px;
  margin-bottom: 18px;
  resize: vertical;
  box-sizing: border-box;
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
  margin-bottom: 12px;
}
.feedback-message {
  margin-top: 16px;
  color: #06d6a0;
  font-weight: bold;
}
</style>